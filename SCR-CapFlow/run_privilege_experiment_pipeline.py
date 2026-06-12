#!/usr/bin/env python3
"""Run the full privilege-amplification experiment pipeline.

Runs all scripts with trials=5 and parallel=30 by default, then generates
case_success_rate_summary.md and case_success_rate_summary.xlsx.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNNER = ROOT / "run_all_privilege_experiments.py"
SUMMARY = ROOT / "generate_privilege_case_success_rate_summary.py"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--parallel", type=int, default=30)
    parser.add_argument("--cases", default=None)
    parser.add_argument("--condition", default="all")
    parser.add_argument("--timeout", type=int, default=None)
    parser.add_argument("--allow-summary-missing", action="store_true")
    args = parser.parse_args()

    run_cmd = [sys.executable, str(RUNNER), "--trials", str(args.trials), "--parallel", str(args.parallel), "--condition", args.condition]
    if args.cases:
        run_cmd.extend(["--cases", args.cases])
    if args.timeout:
        run_cmd.extend(["--timeout", str(args.timeout)])
    run_proc = subprocess.run(run_cmd, cwd=str(ROOT), text=True)

    summary_cmd = [sys.executable, str(SUMMARY)]
    if args.allow_summary_missing:
        summary_cmd.append("--allow-missing")
    summary_proc = subprocess.run(summary_cmd, cwd=str(ROOT), text=True)

    result = {"run_rc": run_proc.returncode, "summary_rc": summary_proc.returncode}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if run_proc.returncode == 0 and summary_proc.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
