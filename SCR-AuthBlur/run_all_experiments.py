#!/usr/bin/env python3
import concurrent.futures
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "experiment_scripts"
LOG_DIR = ROOT / "experiment_logs"
PROGRESS = ROOT / "target-progress.md"
MAX_WORKERS = 20
TRIALS = 5


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--max-workers", type=int, default=20)
    return parser.parse_args()


def script_num(path: Path) -> int:
    return int(path.stem.split("_")[-1])


def list_scripts():
    return sorted(SCRIPTS_DIR.glob("run_experiment_levels_*.py"), key=script_num)


def result_files(case_num: int):
    result_dir = ROOT / "cases" / f"case{case_num}" / "results"
    if not result_dir.exists():
        return []
    return sorted(result_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)


def write_progress(statuses, started_at, finished_at=None):
    scripts = list_scripts()
    counts = {"pending": 0, "running": 0, "done": 0, "failed": 0}
    for s in scripts:
        st = statuses.get(script_num(s), {}).get("status", "pending")
        counts[st] = counts.get(st, 0) + 1
    lines = []
    lines.append("# Target Progress")
    lines.append("")
    lines.append(f"Started: {started_at}")
    if finished_at:
        lines.append(f"Finished: {finished_at}")
    lines.append(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Task checklist")
    lines.append("")
    lines.append("- [x] Inspect experiment setup")
    all_done = counts.get("done", 0) == len(scripts) and counts.get("failed", 0) == 0
    lines.append(f"- [{'x' if all_done else ' '}] Run all `experiment_scripts/run_experiment_levels_*.py` scripts with `--trials 5`, up to 20 scripts in parallel")
    lines.append("- [ ] Create `case_success_rate_summary.md`")
    lines.append("- [ ] Create `case_success_rate_summary.xlsx`")
    lines.append("")
    lines.append("## Overall status")
    lines.append("")
    lines.append(f"- Total scripts: {len(scripts)}")
    lines.append(f"- Done: {counts.get('done', 0)}")
    lines.append(f"- Running: {counts.get('running', 0)}")
    lines.append(f"- Failed: {counts.get('failed', 0)}")
    lines.append(f"- Pending: {counts.get('pending', 0)}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- `target.md` requests all experiments under `experiment_scripts/` with trials=5 and parallel=20.")
    lines.append("- The experiment scripts accept `--trials`; no script-level `--parallel` argument was found, so this runner executes up to 20 scripts concurrently.")
    lines.append("- Each script writes its own JSON results under `cases/case*/results/`; stdout/stderr are under `experiment_logs/`.")
    lines.append("- First full run at 11:21 was invalid because subprocesses used a missing Git Bash path and produced `[WinError 2]`; scripts were patched to use `D:\\Git\\usr\\bin\\bash.exe` and case-local skill contexts before rerun.")
    lines.append("")
    lines.append("## Case status")
    lines.append("")
    lines.append("| Case | Script | Status | Output/Notes |")
    lines.append("|---:|---|---|---|")
    for s in scripts:
        n = script_num(s)
        item = statuses.get(n, {"status": "pending", "note": ""})
        st = item.get("status", "pending")
        note = item.get("note", "")
        if st == "done":
            files = result_files(n)
            if files:
                note = str(files[0].relative_to(ROOT)).replace("\\", "/")
        lines.append(f"| {n} | `{s.name}` | {st} | {note} |")
    PROGRESS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_one(script: Path):
    n = script_num(script)
    log_path = LOG_DIR / f"case{n}.log"
    cmd = [sys.executable, str(script), "--trials", str(TRIALS)]
    start = time.time()
    env = os.environ.copy()
    env.setdefault("CLAUDE_CODE_GIT_BASH_PATH", "D:\\Git\\usr\\bin\\bash.exe")
    with log_path.open("w", encoding="utf-8", errors="replace") as log:
        log.write(f"Command: {' '.join(cmd)}\n")
        log.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        log.flush()
        proc = subprocess.run(cmd, cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT, text=True, env=env)
        log.write(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Return code: {proc.returncode}\n")
    dur = time.time() - start
    return n, proc.returncode, dur, log_path


def main():
    args = parse_args()
    global MAX_WORKERS, TRIALS
    MAX_WORKERS = args.max_workers
    TRIALS = args.trials

    LOG_DIR.mkdir(exist_ok=True)
    scripts = list_scripts()
    statuses = {script_num(s): {"status": "pending", "note": ""} for s in scripts}
    started_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_progress(statuses, started_at)
    pending_scripts = list(scripts)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_script = {}

        def submit_next():
            if not pending_scripts:
                return
            script = pending_scripts.pop(0)
            n = script_num(script)
            statuses[n] = {"status": "running", "note": "started"}
            future_to_script[executor.submit(run_one, script)] = script

        for _ in range(min(MAX_WORKERS, len(pending_scripts))):
            submit_next()
        write_progress(statuses, started_at)

        while future_to_script:
            done, _ = concurrent.futures.wait(
                future_to_script, return_when=concurrent.futures.FIRST_COMPLETED
            )
            for future in done:
                script = future_to_script.pop(future)
                n = script_num(script)
                try:
                    case_num, rc, dur, log_path = future.result()
                    rel_log = str(log_path.relative_to(ROOT)).replace('\\', '/')
                    if rc == 0:
                        statuses[n] = {"status": "done", "note": f"{dur:.1f}s; {rel_log}"}
                    else:
                        statuses[n] = {"status": "failed", "note": f"rc={rc}; {dur:.1f}s; {rel_log}"}
                except Exception as exc:
                    statuses[n] = {"status": "failed", "note": repr(exc).replace('|', '\\|')}
                submit_next()
            write_progress(statuses, started_at)
    finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_progress(statuses, started_at, finished_at)
    failed = [n for n, v in statuses.items() if v.get("status") == "failed"]
    print(json.dumps({"total": len(scripts), "failed": failed}, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
