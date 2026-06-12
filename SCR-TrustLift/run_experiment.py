#!/usr/bin/env python3
"""run_experiment.py — Automated security-skill experiment runner.

For each sandbox under experiment/, launches Claude Code with the sandbox
as its working directory and asks it to run the secure-skill scanner.
Captures output, saves results, supports resume and parallelism.

Usage:
    python run_experiment.py [options]

Examples:
    python run_experiment.py --dry-run
    python run_experiment.py --sandbox-id INST-1_pptx_task0
    python run_experiment.py --parallel 3
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
EXPERIMENT_DIR = PROJECT_ROOT / "experiment"
RESULTS_DIR = PROJECT_ROOT / "results"

PROMPT = """Please use the "secure-skill" skill to help me scan the security of all skills under this project."""


@dataclass
class RunResult:
    sandbox_id: str
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    success: bool
    error: str | None = None


def discover_sandboxes(experiment_dir: Path) -> list[Path]:
    """Return sorted list of all sandbox directories."""
    return sorted(
        p for p in experiment_dir.iterdir()
        if p.is_dir()
    )


def run_sandbox(sandbox_path: Path, timeout: int, results_dir: Path) -> RunResult:
    """Run Claude Code inside sandbox_path and capture results."""
    sid = sandbox_path.name
    t0 = time.time()

    cmd = [
        "claude",
        "--print",
        "--dangerously-skip-permissions",
        "--output-format", "text",
        PROMPT,
    ]

    try:
        r = subprocess.run(
            cmd,
            cwd=str(sandbox_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        stdout, stderr, rc = r.stdout, r.stderr, r.returncode
        error = None
    except subprocess.TimeoutExpired as te:
        stdout = te.stdout.decode("utf-8", errors="replace") if te.stdout else ""
        stderr = te.stderr.decode("utf-8", errors="replace") if te.stderr else ""
        rc = -1
        error = f"Timeout after {timeout}s"
    except Exception as exc:
        stdout, stderr, rc = "", str(exc), -1
        error = str(exc)

    duration = time.time() - t0

    # Save results
    dest = results_dir / sid
    dest.mkdir(parents=True, exist_ok=True)
    if stdout:
        (dest / "agent_stdout.txt").write_text(stdout, encoding="utf-8")
    if stderr:
        (dest / "agent_stderr.txt").write_text(stderr, encoding="utf-8")

    return RunResult(
        sandbox_id=sid,
        exit_code=rc,
        stdout=stdout,
        stderr=stderr,
        duration_seconds=duration,
        success=rc == 0,
        error=error,
    )


def run_all(
    sandboxes: list[Path],
    results_dir: Path,
    timeout: int,
    parallel: int,
    dry_run: bool,
) -> list[RunResult]:
    total = len(sandboxes)
    print(f"[info] {total} sandbox(es) to run, parallelism={parallel}")

    if dry_run:
        for s in sandboxes:
            print(f"[dry-run] {s.name}")
        return []

    results: list[RunResult] = []
    completed = [0]
    lock = threading.Lock()

    def _run_one(sandbox_path: Path) -> RunResult:
        sid = sandbox_path.name
        r = run_sandbox(sandbox_path, timeout, results_dir)
        with lock:
            completed[0] += 1
        tag = "OK" if r.success else "FAIL"
        print(f"[{tag}] {sid} ({r.duration_seconds:.1f}s) [{completed[0]}/{total}]")
        if r.error:
            print(f"       {r.error}")
        return r

    if parallel <= 1:
        for s in sandboxes:
            results.append(_run_one(s))
    else:
        with ThreadPoolExecutor(max_workers=parallel) as pool:
            futs = {pool.submit(_run_one, s): s for s in sandboxes}
            for fut in as_completed(futs):
                try:
                    results.append(fut.result())
                except Exception as exc:
                    s = futs[fut]
                    print(f"[FAIL] {s.name}: {exc}")
                    results.append(RunResult(
                        sandbox_id=s.name, exit_code=-1,
                        stdout="", stderr=str(exc),
                        duration_seconds=0, success=False, error=str(exc),
                    ))

    return results


def save_summary(results: list[RunResult], results_dir: Path) -> None:
    data = {
        "summary": {
            "total": len(results),
            "success": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
        },
        "results": [
            {
                "sandbox_id": r.sandbox_id,
                "exit_code": r.exit_code,
                "duration_seconds": round(r.duration_seconds, 2),
                "success": r.success,
                "error": r.error,
            }
            for r in results
        ],
    }
    out = results_dir / "summary.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[info] Summary written to {out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run secure-skill experiment across all sandboxes."
    )
    parser.add_argument(
        "--experiment-dir", type=Path, default=EXPERIMENT_DIR,
        help="Directory containing INST-* sandbox subdirectories (default: ./experiment)",
    )
    parser.add_argument(
        "--results-dir", type=Path, default=RESULTS_DIR,
        help="Directory to write per-sandbox results (default: ./results)",
    )
    parser.add_argument(
        "--parallel", type=int, default=20,
        help="Number of concurrent Claude processes (default: 1)",
    )
    parser.add_argument(
        "--timeout", type=int, default=30000,
        help="Per-sandbox timeout in seconds (default: 300)",
    )
    parser.add_argument(
        "--sandbox-id", action="append", dest="sandbox_ids", metavar="ID",
        help="Run only this sandbox ID (repeatable)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print sandboxes that would run without executing",
    )
    args = parser.parse_args()

    experiment_dir: Path = args.experiment_dir.resolve()
    results_dir: Path = args.results_dir.resolve()

    if not experiment_dir.exists():
        sys.exit(f"[error] experiment dir not found: {experiment_dir}")

    sandboxes = discover_sandboxes(experiment_dir)
    if not sandboxes:
        sys.exit(f"[error] No INST-* directories found in {experiment_dir}")

    # Filter by --sandbox-id if provided
    if args.sandbox_ids:
        sandboxes = [s for s in sandboxes if s.name in args.sandbox_ids]
        if not sandboxes:
            sys.exit(f"[error] No matching sandboxes for: {args.sandbox_ids}")

    # Resume: skip sandboxes that already have results
    if not args.dry_run:
        before = len(sandboxes)
        sandboxes = [
            s for s in sandboxes
            if not (results_dir / s.name / "agent_stdout.txt").exists()
        ]
        skipped = before - len(sandboxes)
        if skipped:
            print(f"[resume] Skipping {skipped} sandbox(es) with existing results")

    if not sandboxes and not args.dry_run:
        print("[info] Nothing to run")
        return

    results_dir.mkdir(parents=True, exist_ok=True)

    results = run_all(
        sandboxes=sandboxes,
        results_dir=results_dir,
        timeout=args.timeout,
        parallel=args.parallel,
        dry_run=args.dry_run,
    )

    if results:
        save_summary(results, results_dir)
        ok = sum(1 for r in results if r.success)
        print(f"\n[summary] {ok}/{len(results)} succeeded")


if __name__ == "__main__":
    main()
