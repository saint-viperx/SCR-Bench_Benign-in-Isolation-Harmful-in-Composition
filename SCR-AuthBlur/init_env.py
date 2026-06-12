#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
Initialize experiment environment across Windows/Linux machines.

Functions:
1. Replace CLAUDE_CODE_GIT_BASH_PATH default path in run_all_experiments.py
   and experiment_scripts/run_experiment_levels_*.py.
2. Rename cases/case*/cli_skills according to selected CLI backend.

Usage examples:

Windows PowerShell:
    python init_env.py --claude_code_git_bash_path 'C:\Program Files\Git\usr\bin\bash.exe' --cli CodeX

Windows CMD:
    python init_env.py --claude_code_git_bash_path "C:\Program Files\Git\usr\bin\bash.exe" --cli CodeX

Linux:
    python init_env.py --claude_code_git_bash_path /usr/bin/bash --cli GeminiCLI
"""

import argparse
import ast
import io
import json
import sys
import tokenize
from pathlib import Path


ROOT = Path(__file__).resolve().parent

RUN_ALL = ROOT / "run_all_experiments.py"
EXPERIMENT_SCRIPTS_DIR = ROOT / "experiment_scripts"
CASES_DIR = ROOT / "cases"

ENV_KEY = "CLAUDE_CODE_GIT_BASH_PATH"

# Runtime value of the original Python literal:
# "D:\\Git\\usr\\bin\\bash.exe"
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


def py_string_literal(value: str) -> str:
    """
    Convert an arbitrary path into a valid Python string literal.

    Example:
        C:\\Program Files\\Git\\usr\\bin\\bash.exe

    becomes source code:
        "C:\\\\Program Files\\\\Git\\\\usr\\\\bin\\\\bash.exe"

    json.dumps output is also a valid Python string literal.
    """
    return json.dumps(value, ensure_ascii=False)


def literal_value(token_string):
    """
    Safely evaluate a Python string token.

    Returns None if the token is not a normal evaluable string literal.
    """
    try:
        value = ast.literal_eval(token_string)
    except Exception:
        return None
    return value if isinstance(value, str) else None


def replace_bash_path_in_python_source(text: str, new_bash_path: str):
    """
    Token-based replacement.

    It handles both cases:

    1. Direct old literal:
        "D:\\\\Git\\\\usr\\\\bin\\\\bash.exe"

    2. Any value next to CLAUDE_CODE_GIT_BASH_PATH:
        env.setdefault("CLAUDE_CODE_GIT_BASH_PATH", "old_or_new_path")
        env["CLAUDE_CODE_GIT_BASH_PATH"] = "old_or_new_path"

    This avoids corrupting Python source code with unescaped Windows paths.
    """
    tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    new_literal = py_string_literal(new_bash_path)

    replaced = 0

    waiting_after_key = False
    ready_to_replace_value = False

    new_tokens = []

    for tok in tokens:
        tok_type = tok.type
        tok_str = tok.string

        if tok_type == tokenize.STRING:
            value = literal_value(tok_str)

            # Case A:
            # Replace the original default bash path wherever it appears as a Python string literal.
            if value == DEFAULT_BASH_VALUE:
                tok = tok._replace(string=new_literal)
                replaced += 1

                waiting_after_key = False
                ready_to_replace_value = False
                new_tokens.append(tok)
                continue

            # Case B:
            # We saw "CLAUDE_CODE_GIT_BASH_PATH"; replace the next string value after comma or equals.
            if ready_to_replace_value and value is not None and value != ENV_KEY:
                tok = tok._replace(string=new_literal)
                replaced += 1

                waiting_after_key = False
                ready_to_replace_value = False
                new_tokens.append(tok)
                continue

            # Detect key.
            if value == ENV_KEY:
                waiting_after_key = True
                ready_to_replace_value = False
                new_tokens.append(tok)
                continue

        elif tok_type == tokenize.OP:
            if waiting_after_key and tok_str in {",", "="}:
                ready_to_replace_value = True

            # Reset if statement or call clearly ended before value appeared.
            if waiting_after_key and tok_str in {";", ")"} and not ready_to_replace_value:
                waiting_after_key = False
                ready_to_replace_value = False

        elif tok_type in {
            tokenize.NEWLINE,
            tokenize.NL,
            tokenize.ENDMARKER,
        }:
            if waiting_after_key:
                waiting_after_key = False
                ready_to_replace_value = False

        new_tokens.append(tok)

    new_text = tokenize.untokenize(new_tokens)
    return new_text, replaced


def collect_python_files():
    files = []

    if RUN_ALL.exists():
        files.append(RUN_ALL)

    if EXPERIMENT_SCRIPTS_DIR.exists():
        files.extend(sorted(EXPERIMENT_SCRIPTS_DIR.glob("run_experiment_levels_*.py")))

    return files


def update_bash_paths(new_bash_path: str):
    files = collect_python_files()
    errors = []
    changed = []

    for file_path in progress(files, "Replacing bash path"):
        try:
            old_text = file_path.read_text(encoding="utf-8")
            new_text, count = replace_bash_path_in_python_source(
                old_text,
                new_bash_path,
            )

            if count > 0 and new_text != old_text:
                file_path.write_text(new_text, encoding="utf-8")
                changed.append((file_path, count))

        except Exception as e:
            errors.append((file_path, str(e)))

    return changed, errors


def collect_case_dirs():
    if not CASES_DIR.exists():
        return []

    return sorted(
        p for p in CASES_DIR.glob("case*")
        if p.is_dir()
    )


def rename_cli_dirs(cli: str):
    target_dir_name = CLI_DIR_MAP[cli]

    case_dirs = collect_case_dirs()
    errors = []
    changed = []
    skipped = []

    for case_dir in progress(
        case_dirs,
        f"Renaming {SOURCE_SKILLS_DIR_NAME} to {target_dir_name}",
    ):
        src = case_dir / SOURCE_SKILLS_DIR_NAME
        dst = case_dir / target_dir_name

        try:
            if src.exists() and dst.exists():
                errors.append((
                    case_dir,
                    f"Both source and target exist: {src} and {dst}. Refuse to overwrite.",
                ))
                continue

            if not src.exists():
                if dst.exists():
                    skipped.append((case_dir, f"Already migrated: {dst} exists"))
                else:
                    skipped.append((case_dir, f"No {SOURCE_SKILLS_DIR_NAME} directory found"))
                continue

            src.rename(dst)
            changed.append((src, dst))

        except Exception as e:
            errors.append((case_dir, str(e)))

    return changed, skipped, errors


def parse_args():
    parser = argparse.ArgumentParser(
        description="Initialize experiment environment for different machines and CLI backends."
    )

    parser.add_argument(
        "--claude_code_git_bash_path",
        type=str,
        default=DEFAULT_BASH_VALUE,
        help=(
            "Path to bash executable. "
            r"Default: D:\Git\usr\bin\bash.exe"
        ),
    )

    parser.add_argument(
        "--cli",
        type=str,
        default="ClaudeCode",
        choices=["ClaudeCode", "CodeX", "OpenCode", "GeminiCLI"],
        help="CLI backend. Default: ClaudeCode",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 80)
    print("Experiment environment initializer")
    print("=" * 80)
    print(f"Project root: {ROOT}")
    print(f"Python executable: {sys.executable}")
    print(f"{ENV_KEY}: {args.claude_code_git_bash_path}")
    print(f"CLI backend: {args.cli}")
    print(f"Source skills directory: {SOURCE_SKILLS_DIR_NAME}")
    print(f"Target skills directory: {CLI_DIR_MAP[args.cli]}")
    print("=" * 80)

    print("\n[1/2] Updating Python script bash paths")
    changed_files, file_errors = update_bash_paths(
        new_bash_path=args.claude_code_git_bash_path,
    )

    print("\n[2/2] Updating case CLI directories")
    changed_dirs, skipped_dirs, dir_errors = rename_cli_dirs(args.cli)

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)

    print(f"Changed Python files: {len(changed_files)}")
    for file_path, count in changed_files:
        print(f"  [OK] {file_path.relative_to(ROOT)} | replacements: {count}")

    print(f"\nChanged case directories: {len(changed_dirs)}")
    for src, dst in changed_dirs:
        print(f"  [OK] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")

    print(f"\nSkipped case directories: {len(skipped_dirs)}")
    for case_dir, reason in skipped_dirs[:20]:
        print(f"  [SKIP] {case_dir.relative_to(ROOT)} | {reason}")

    if len(skipped_dirs) > 20:
        print(f"  ... {len(skipped_dirs) - 20} more skipped")

    total_errors = len(file_errors) + len(dir_errors)

    print(f"\nErrors: {total_errors}")

    if file_errors:
        print("\nPython file update errors:")
        for file_path, err in file_errors:
            print(f"  [ERROR] {file_path}: {err}")

    if dir_errors:
        print("\nDirectory rename errors:")
        for case_dir, err in dir_errors:
            print(f"  [ERROR] {case_dir}: {err}")

    print("=" * 80)

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())