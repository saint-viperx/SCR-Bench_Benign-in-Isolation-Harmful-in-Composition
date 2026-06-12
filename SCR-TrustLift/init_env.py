#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Initialize experiment environment by group selection and CLI backend.

Usage:
    python init_env.py --group experiment --cli CodeX
    python init_env.py --group control --cli ClaudeCode
"""

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent

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


def collect_case_dirs(root):
    if not root.exists():
        return []

    return sorted(
        p for p in root.glob("*")
        if p.is_dir()
    )


def rename_cli_dirs(root, cli):
    target_dir_name = CLI_DIR_MAP[cli]

    case_dirs = collect_case_dirs(root)
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
        description="Initialize experiment environment by group and CLI backend."
    )

    parser.add_argument(
        "--group",
        type=str,
        required=True,
        choices=["control", "experiment"],
        help="Experiment group to use: control or experiment",
    )

    parser.add_argument(
        "--cli",
        type=str,
        required=True,
        choices=["ClaudeCode", "CodeX", "OpenCode", "GeminiCLI"],
        help="CLI backend.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    group_dir_name = f"{args.group}-group"
    group_dir = ROOT / group_dir_name
    target_dir = ROOT / args.group

    print("=" * 80)
    print("Experiment environment initializer")
    print("=" * 80)
    print(f"Project root: {ROOT}")
    print(f"Group: {args.group}")
    print(f"Source directory: {group_dir}")
    print(f"Target directory: {target_dir}")
    print(f"CLI backend: {args.cli}")
    print(f"Source skills directory: {SOURCE_SKILLS_DIR_NAME}")
    print(f"Target skills directory: {CLI_DIR_MAP[args.cli]}")
    print("=" * 80)

    if not group_dir.exists():
        print(f"[ERROR] Source directory does not exist: {group_dir}")
        return 1

    if target_dir.exists():
        print(f"[WARN] Target directory already exists: {target_dir}")
        print(f"       Skipping copy step. Please remove or rename it manually.")
    else:
        print(f"\n[1/2] Copying {group_dir_name} to {args.group}")
        try:
            shutil.copytree(group_dir, target_dir)
            print(f"[OK] Copied to {target_dir}")
        except Exception as e:
            print(f"[ERROR] Failed to copy: {e}")
            return 1

    print(f"\n[2/2] Updating case CLI directories in {target_dir}")
    changed_dirs, skipped_dirs, dir_errors = rename_cli_dirs(target_dir, args.cli)

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)

    print(f"Changed case directories: {len(changed_dirs)}")
    for src, dst in changed_dirs:
        print(f"  [OK] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")

    print(f"\nSkipped case directories: {len(skipped_dirs)}")
    for case_dir, reason in skipped_dirs[:20]:
        print(f"  [SKIP] {case_dir.relative_to(ROOT)} | {reason}")

    if len(skipped_dirs) > 20:
        print(f"  ... {len(skipped_dirs) - 20} more skipped")

    print(f"\nErrors: {len(dir_errors)}")

    if dir_errors:
        print("\nDirectory rename errors:")
        for case_dir, err in dir_errors:
            print(f"  [ERROR] {case_dir.relative_to(ROOT)}: {err}")

    print("=" * 80)

    return 1 if dir_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())