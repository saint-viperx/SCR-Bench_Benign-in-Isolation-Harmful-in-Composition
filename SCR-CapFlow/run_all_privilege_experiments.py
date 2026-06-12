#!/usr/bin/env python3
"""Run all privilege-amplification experiment_case*.py scripts.

Default task settings: --trials 5 and --parallel 30.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
LOG_DIR = ROOT / "experiment_logs" / "privilege_amplification"
PROGRESS = ROOT / "target-progress.md"
DEFAULT_TRIALS = 5
DEFAULT_PARALLEL = 30


def case_num_from_path(path: Path) -> int:
    match = re.search(r"experiment_case(\d+)$", path.stem)
    if not match:
        raise ValueError(f"Cannot parse case number from {path.name}")
    return int(match.group(1))


def list_scripts(case_filter: set[int] | None = None) -> list[Path]:
    scripts = sorted(SCRIPTS_DIR.glob("experiment_case*.py"), key=case_num_from_path)
    if case_filter is None:
        return scripts
    return [script for script in scripts if case_num_from_path(script) in case_filter]


def parse_case_selection(raw: str | None) -> set[int] | None:
    if not raw:
        return None
    selected: set[int] = set()
    for part in raw.split(","):
        item = part.strip()
        if not item:
            continue
        if "-" in item:
            start, end = item.split("-", 1)
            selected.update(range(int(start), int(end) + 1))
        else:
            selected.add(int(item))
    return selected


def latest_result_file(case_num: int) -> Path | None:
    candidates: list[Path] = []
    result_dir = ROOT / "cases" / f"case{case_num}" / "results"
    if result_dir.exists():
        candidates.extend(result_dir.glob("*.json"))
    legacy_dir = SCRIPTS_DIR / "results"
    if legacy_dir.exists():
        candidates.extend(legacy_dir.glob(f"experiment_case{case_num}*.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def choose_git_bash(env: dict[str, str]) -> None:
    if env.get("CLAUDE_CODE_GIT_BASH_PATH"):
        return
    candidates = [
        "D:/software/Git/bin/bash.exe",
        "D:/software/Git/usr/bin/bash.exe",
        "D:/Git/usr/bin/bash.exe",
        "D:/Git/bin/bash.exe",
        "C:/Program Files/Git/bin/bash.exe",
        "C:/Program Files/Git/usr/bin/bash.exe",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            env["CLAUDE_CODE_GIT_BASH_PATH"] = str(path)
            return


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def write_progress(statuses: dict[int, dict[str, str]], scripts: list[Path], started_at: str, finished_at: str | None = None) -> None:
    counts = {"pending": 0, "running": 0, "done": 0, "failed": 0}
    for script in scripts:
        status = statuses.get(case_num_from_path(script), {}).get("status", "pending")
        counts[status] = counts.get(status, 0) + 1

    all_done = counts.get("done", 0) == len(scripts) and counts.get("failed", 0) == 0
    lines = [
        "# Target Progress",
        "",
        f"Started: {started_at}",
    ]
    if finished_at:
        lines.append(f"Finished: {finished_at}")
    lines.extend([
        f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Task checklist",
        "",
        "- [x] Inspect privilege amplification experiment setup",
        f"- [{'x' if all_done else ' '}] Run `scripts/experiment_case*.py` with `--trials 5`, up to 30 scripts in parallel",
        "- [ ] Create `case_success_rate_summary.md`",
        "- [ ] Create `case_success_rate_summary.xlsx`",
        "",
        "## Overall status",
        "",
        f"- Total scripts: {len(scripts)}",
        f"- Done: {counts.get('done', 0)}",
        f"- Running: {counts.get('running', 0)}",
        f"- Failed: {counts.get('failed', 0)}",
        f"- Pending: {counts.get('pending', 0)}",
        "",
        "## Notes",
        "",
        "- Runner defaults match the requested privilege-amplification task: trials=5 and parallel=30.",
        "- Each case script writes JSON results under `cases/case*/results/`; stdout/stderr logs are under `experiment_logs/privilege_amplification/`.",
        "- `generate_privilege_case_success_rate_summary.py` reads the latest result per case and creates the root summary files.",
        "",
        "## Case status",
        "",
        "| Case | Script | Status | Output/Notes |",
        "|---:|---|---|---|",
    ])

    for script in scripts:
        case_num = case_num_from_path(script)
        item = statuses.get(case_num, {"status": "pending", "note": ""})
        status = item.get("status", "pending")
        note = item.get("note", "")
        if status == "done":
            latest = latest_result_file(case_num)
            if latest:
                note = rel(latest)
        safe_note = note.replace("|", "\\|")
        lines.append(f"| {case_num} | `{rel(script)}` | {status} | {safe_note} |")

    PROGRESS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_one(script: Path, trials: int, condition: str, timeout: int | None) -> tuple[int, int, float, Path]:
    case_num = case_num_from_path(script)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"case{case_num}.log"
    cmd = [sys.executable, str(script), "--trials", str(trials)]
    if condition != "all":
        cmd.extend(["--condition", condition])

    env = os.environ.copy()
    choose_git_bash(env)
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t0 = time.time()
    with log_path.open("w", encoding="utf-8", errors="replace") as log:
        log.write(f"Command: {' '.join(cmd)}\n")
        log.write(f"Started: {started}\n")
        if env.get("CLAUDE_CODE_GIT_BASH_PATH"):
            log.write(f"CLAUDE_CODE_GIT_BASH_PATH={env['CLAUDE_CODE_GIT_BASH_PATH']}\n")
        log.write("\n")
        log.flush()
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(ROOT),
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                timeout=timeout,
            )
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            log.write(f"\nTimed out after {timeout}s\n")
            rc = 124
        log.write(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Return code: {rc}\n")
    return case_num, rc, time.time() - t0, log_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS, help="Trials per condition; default: 5")
    parser.add_argument("--parallel", type=int, default=DEFAULT_PARALLEL, help="Number of experiment scripts to run concurrently; default: 30")
    parser.add_argument("--cases", default=None, help="Optional case list/ranges, e.g. '1,3,10-20'")
    parser.add_argument("--condition", default="all", help="Optional condition passed to every case script; default: all")
    parser.add_argument("--timeout", type=int, default=None, help="Optional per-case timeout in seconds")
    args = parser.parse_args()

    case_filter = parse_case_selection(args.cases)
    scripts = list_scripts(case_filter)
    if not scripts:
        print(json.dumps({"error": "no experiment scripts found", "cases": args.cases}, ensure_ascii=False))
        return 1

    statuses = {case_num_from_path(script): {"status": "pending", "note": ""} for script in scripts}
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_progress(statuses, scripts, started_at)

    pending = list(scripts)
    max_workers = max(1, args.parallel)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_script: dict[concurrent.futures.Future, Path] = {}

        def submit_next() -> None:
            if not pending:
                return
            script = pending.pop(0)
            case_num = case_num_from_path(script)
            statuses[case_num] = {"status": "running", "note": "started"}
            future_to_script[executor.submit(run_one, script, args.trials, args.condition, args.timeout)] = script

        for _ in range(min(max_workers, len(pending))):
            submit_next()
        write_progress(statuses, scripts, started_at)

        while future_to_script:
            done, _ = concurrent.futures.wait(future_to_script, return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                script = future_to_script.pop(future)
                case_num = case_num_from_path(script)
                try:
                    _, rc, duration, log_path = future.result()
                    log_rel = rel(log_path)
                    if rc == 0:
                        statuses[case_num] = {"status": "done", "note": f"{duration:.1f}s; {log_rel}"}
                    else:
                        statuses[case_num] = {"status": "failed", "note": f"rc={rc}; {duration:.1f}s; {log_rel}"}
                except Exception as exc:
                    statuses[case_num] = {"status": "failed", "note": repr(exc)}
                submit_next()
            write_progress(statuses, scripts, started_at)

    finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_progress(statuses, scripts, started_at, finished_at)
    failed = [case for case, item in statuses.items() if item.get("status") == "failed"]
    print(json.dumps({"total": len(scripts), "trials": args.trials, "parallel": max_workers, "failed": failed}, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
