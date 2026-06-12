#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Initialize experiment environment from cases-env template.

Functions:
1. Copy cases-env/ to cases/ (cases-env remains unchanged).
2. Replace CLAUDE_CODE_GIT_BASH_PATH in run_all_privilege_experiments.py
   (prepend user-specified path to candidates list).
3. Replace CLAUDE_CODE_GIT_BASH_PATH in scripts/experiment_case*.py
   (replace the path in setdefault calls).
4. Rename cases/case*/cli_skills to target directory based on --cli.

Usage examples:

Windows:
    python init_env.py --claude_code_git_bash_path "D:\software\Git\bin\bash.exe" --cli ClaudeCode

Linux:
    python init_env.py --claude_code_git_bash_path /usr/bin/bash --cli GeminiCLI
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CASES_ENV_DIR = ROOT / "cases-env"
CASES_DIR = ROOT / "cases"

RUN_ALL = ROOT / "run_all_privilege_experiments.py"
SCRIPTS_DIR = ROOT / "scripts"

ENV_KEY = "CLAUDE_CODE_GIT_BASH_PATH"

DEFAULT_BASH_VALUE = r"D:\Git\usr\bin\bash.exe"

SOURCE_SKILLS_DIR_NAME = "cli_skills"

CLI_DIR_MAP = {
    "ClaudeCode": ".claude",
    "CodeX": ".agents",
    "GeminiCLI": ".gemini",
    "OpenCode": ".opencode",
}


def progress(items, desc):
    total = len(items)
    if total == 0:
        print(f"{desc}: 0/0")
        return

    for i, item in enumerate(items, 1):
        pct = i * 100.0 / total
        name = str(item)
        if len(name) > 80:
            name = "..." + name[-77:]
        print(f"\r{desc}: {i}/{total} ({pct:6.2f}%) {name}", end="", flush=True)
        yield item
    print()


def copy_cases_env():
    """Copy cases-env to cases, skipping if already exists."""
    if CASES_DIR.exists():
        return [], []

    if not CASES_ENV_DIR.exists():
        return [], [{"source": str(CASES_ENV_DIR), "error": "cases-env directory does not exist"}]

    changed = []
    errors = []

    try:
        shutil.copytree(CASES_ENV_DIR, CASES_DIR, symlinks=False, ignore=None)
        changed.append((CASES_ENV_DIR, CASES_DIR))
    except Exception as e:
        errors.append({"source": str(CASES_ENV_DIR), "error": str(e)})

    return changed, errors


def update_run_all_bash_path(new_bash_path: str):
    """
    Prepend user-specified path to the candidates list in run_all_privilege_experiments.py.
    The path is inserted at the beginning of the candidates list.
    """
    if not RUN_ALL.exists():
        return [], [{"file": str(RUN_ALL), "error": "file does not exist"}]

    errors = []
    changed = []

    try:
        text = RUN_ALL.read_text(encoding="utf-8")

        # Find candidates list and prepend new path
        # Pattern: candidates = [\n    "path1",\n    "path2", ...]
        # We need to insert the new path as the first entry

        # Match the candidates list pattern
        candidates_pattern = r'(candidates\s*=\s*\[)(.*?)(\])'

        # Escape backslashes for Python string literal
        escaped_path = new_bash_path.replace("\\", "\\\\")
        new_entry = f'\n        "{escaped_path}",'

        def prepend_path(match):
            return match.group(1) + new_entry + match.group(2) + match.group(3)

        new_text, count = re.subn(
            candidates_pattern,
            prepend_path,
            text,
            flags=re.DOTALL
        )

        if count > 0 and new_text != text:
            RUN_ALL.write_text(new_text, encoding="utf-8")
            changed.append((RUN_ALL, count))
        elif count == 0:
            errors.append({"file": str(RUN_ALL), "error": "candidates list not found"})

    except Exception as e:
        errors.append({"file": str(RUN_ALL), "error": str(e)})

    return changed, errors


def update_experiment_scripts_bash_path(new_bash_path: str):
    """
    Replace CLAUDE_CODE_GIT_BASH_PATH value in scripts/experiment_case*.py files.
    Replaces the path in: os.environ.setdefault("CLAUDE_CODE_GIT_BASH_PATH", r"xxx")
    """
    if not SCRIPTS_DIR.exists():
        return [], [{"dir": str(SCRIPTS_DIR), "error": "scripts directory does not exist"}]

    scripts = sorted(SCRIPTS_DIR.glob("experiment_case*.py"))

    changed = []
    errors = []

    # Escape backslashes for regex replacement
    escaped_path = new_bash_path.replace("\\", "\\\\")

    # Pattern to match setdefault with raw string path
    # os.environ.setdefault("CLAUDE_CODE_GIT_BASH_PATH", r"path")
    pattern = r'(os\.environ\.setdefault\s*\(\s*["\']CLAUDE_CODE_GIT_BASH_PATH["\']\s*,\s*r\s*")([^"]+)(")'

    for script in progress(scripts, "Updating experiment scripts"):
        try:
            text = script.read_text(encoding="utf-8")

            def replace_path(match):
                prefix = match.group(1)
                old_path = match.group(2)
                suffix = match.group(3)
                return f'{prefix}{escaped_path}{suffix}'

            new_text, count = re.subn(pattern, replace_path, text)

            if count > 0 and new_text != text:
                script.write_text(new_text, encoding="utf-8")
                changed.append((script, count))
        except Exception as e:
            errors.append({"file": str(script), "error": str(e)})

    return changed, errors


def rename_cli_dirs(cli: str):
    """Rename cli_skills to target directory name based on --cli."""
    target_dir_name = CLI_DIR_MAP.get(cli)
    if not target_dir_name:
        return [], [], [{"cli": cli, "error": f"unknown cli: {cli}, choices: {list(CLI_DIR_MAP.keys())}"}]

    if not CASES_DIR.exists():
        return [], [], [{"dir": str(CASES_DIR), "error": "cases directory does not exist"}]

    case_dirs = sorted(
        p for p in CASES_DIR.glob("case*")
        if p.is_dir()
    )

    changed = []
    skipped = []
    errors = []

    for case_dir in progress(case_dirs, f"Renaming {SOURCE_SKILLS_DIR_NAME} to {target_dir_name}"):
        src = case_dir / SOURCE_SKILLS_DIR_NAME
        dst = case_dir / target_dir_name

        try:
            if src.exists() and dst.exists():
                errors.append({"case": str(case_dir), "error": f"Both {src} and {dst} exist"})
                continue

            if not src.exists():
                if dst.exists():
                    skipped.append((case_dir, f"Already migrated: {dst} exists"))
                else:
                    skipped.append((case_dir, f"No {SOURCE_SKILLS_DIR_NAME} found"))
                continue

            src.rename(dst)
            changed.append((src, dst))

        except Exception as e:
            errors.append({"case": str(case_dir), "error": str(e)})

    return changed, skipped, errors


def parse_args():
    parser = argparse.ArgumentParser(
        description="Initialize experiment environment from cases-env template."
    )

    parser.add_argument(
        "--claude_code_git_bash_path",
        type=str,
        default=DEFAULT_BASH_VALUE,
        help=f"Path to bash executable. Default: {DEFAULT_BASH_VALUE}",
    )

    parser.add_argument(
        "--cli",
        type=str,
        default="ClaudeCode",
        choices=["ClaudeCode", "CodeX", "GeminiCLI", "OpenCode"],
        help="CLI backend. Default: ClaudeCode",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    target_dir_name = CLI_DIR_MAP[args.cli]

    print("=" * 80)
    print("Experiment environment initializer")
    print("=" * 80)
    print(f"Project root: {ROOT}")
    print(f"Python executable: {sys.executable}")
    print(f"Git bash path: {args.claude_code_git_bash_path}")
    print(f"CLI backend: {args.cli}")
    print(f"Source skills dir: {SOURCE_SKILLS_DIR_NAME}")
    print(f"Target skills dir: {target_dir_name}")
    print("=" * 80)

    print("\n[1/4] Copying cases-env to cases")
    changed_dirs, copy_errors = copy_cases_env()
    print(f"  Copied: {len(changed_dirs)}")
    for src, dst in changed_dirs:
        print(f"    {src} -> {dst}")
    if copy_errors:
        for e in copy_errors:
            print(f"  [ERROR] {e}")

    print("\n[2/4] Updating run_all_privilege_experiments.py")
    changed_files, file_errors = update_run_all_bash_path(args.claude_code_git_bash_path)
    print(f"  Changed: {len(changed_files)}")
    for file_path, count in changed_files:
        print(f"    [OK] {file_path.relative_to(ROOT)} | replacements: {count}")
    if file_errors:
        for e in file_errors:
            print(f"  [ERROR] {e}")

    print("\n[3/4] Updating scripts/experiment_case*.py")
    changed_scripts, script_errors = update_experiment_scripts_bash_path(args.claude_code_git_bash_path)
    print(f"  Changed: {len(changed_scripts)}")
    if script_errors:
        for e in script_errors:
            print(f"  [ERROR] {e}")

    print("\n[4/4] Renaming cli_skills to {target_dir_name}")
    changed, skipped, dir_errors = rename_cli_dirs(args.cli)
    print(f"  Renamed: {len(changed)}")
    for src, dst in changed:
        print(f"    [OK] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    if skipped:
        print(f"  Skipped: {len(skipped)}")
        for case_dir, reason in skipped[:20]:
            print(f"    [SKIP] {case_dir.relative_to(ROOT)} | {reason}")
    if dir_errors:
        for e in dir_errors:
            print(f"  [ERROR] {e}")

    total_errors = len(copy_errors) + len(file_errors) + len(script_errors) + len(dir_errors)

    print("\n" + "=" * 80)
    print(f"Done. Total errors: {total_errors}")
    print("=" * 80)

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())