#!/usr/bin/env python3
"""
Install one or more skills from a local registry into the project's skill directory.

Usage:
    python install_skills.py <project_root> [<skill_name> ...]

If no skill names are given on the command line, the DEFAULT_SKILLS list below
is used. Edit that list to specify which skills should be installed by default.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

# ============================================================
# CONFIGURE: list the skill names to install here.
# Add or remove entries as needed. These are used when no
# skill names are passed on the command line.
# ============================================================
DEFAULT_SKILLS = [
    "pptx",
    # Add more skill names below, one per line:
    # "another-skill",
]
# ============================================================


def load_registry(registry_dir: Path) -> list:
    """Load and return the registry item list from registry.json."""
    idx_path = registry_dir / "registry.json"
    if not idx_path.exists():
        print(
            f"error: registry.json not found in {registry_dir}. "
            "Run build_index.py first.",
            file=sys.stderr,
        )
        return []
    return json.loads(idx_path.read_text(encoding="utf-8"))


def install_skill(skill_name: str, project_root: Path, registry_dir: Path) -> int:
    """Install a single skill by name from the local registry.

    Steps:
    1. Validate inputs.
    2. Load registry.json.
    3. Look up skill by name.
    4. Resolve source path.
    5. Validate source exists.
    6. Set destination path.
    7. Create destination parent directories.
    8. Abort if destination already exists.
    9. Copy skill tree to destination.
    10. Verify SKILL.md exists at destination.
    11. Print success.
    """
    # Step 1: basic name validation
    if not skill_name or not skill_name.strip():
        print("error: skill name cannot be empty.", file=sys.stderr)
        return 2

    # Step 2: load registry
    items = load_registry(registry_dir)
    if not items:
        return 2

    # Step 3: look up skill
    match = next((x for x in items if x.get("name") == skill_name), None)
    if not match:
        print(f"error: skill not found in registry: {skill_name}", file=sys.stderr)
        return 2

    # Step 4: resolve source path
    src = (registry_dir / match["path"]).resolve()

    # Step 5: validate source exists
    if not src.exists():
        print(f"error: source path not found: {src}", file=sys.stderr)
        return 2

    # Step 6: set destination
    dst = project_root / ".claude" / "skills" / skill_name

    # Step 7: create destination parent directories
    dst.parent.mkdir(parents=True, exist_ok=True)

    # Step 8: abort if destination already exists
    if dst.exists():
        print(f"error: destination already exists: {dst}", file=sys.stderr)
        return 1

    # Step 9: copy skill tree
    shutil.copytree(src, dst)

    # Step 10: verify SKILL.md present
    if not (dst / "SKILL.md").exists():
        print("error: install failed (SKILL.md missing after copy).", file=sys.stderr)
        return 1

    # Step 11: success
    print(f"Installed {skill_name} -> {dst}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Install skills from a local registry into a project. "
            "If no skill names are given, DEFAULT_SKILLS in this script is used."
        )
    )
    parser.add_argument(
        "project_root",
        help="Root directory of the target project",
    )
    parser.add_argument(
        "skills",
        nargs="*",
        default=DEFAULT_SKILLS,
        help="Skill names to install (defaults to DEFAULT_SKILLS list in this script)",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    # registry.json lives alongside the skill root (one level above scripts/)
    registry_dir = Path(__file__).parent.parent.parent.parent.parent / "registry"
    skills = args.skills

    if not skills:
        print(
            "error: no skills specified and DEFAULT_SKILLS is empty.",
            file=sys.stderr,
        )
        return 2

    exit_code = 0
    for skill_name in skills:
        result = install_skill(skill_name, project_root, registry_dir)
        if result != 0:
            exit_code = result

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
