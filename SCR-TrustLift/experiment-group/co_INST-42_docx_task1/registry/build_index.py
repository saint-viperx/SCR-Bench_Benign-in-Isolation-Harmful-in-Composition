#!/usr/bin/env python3
"""
Build registry.json from SKILL.md frontmatter.

Compatibility goals:
- required: name, description
- optional: license
- keep registry entry["name"] = skill_dir.name  (do NOT use frontmatter name)
- no third-party dependencies

Supported frontmatter forms:
- key: value
- key:
    indented multiline text
- key:
    - item1
    - item2
- key: >
    multiline folded text
- key: |
    multiline literal text
- inline list values like: [a, b, c]
- ignores blank lines and comment lines starting with #
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List


RE_FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
RE_KEYVAL = re.compile(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)\s*$")
RE_QUOTED = re.compile(r'^(?P<q>["\'])(.*)(?P=q)$')

REQUIRED = ["description"]
OPTIONAL = ["license"]


def _strip_quotes(s: str) -> str:
    s = s.strip()
    m = RE_QUOTED.match(s)
    return m.group(2) if m else s


def _normalize_scalar(value: str) -> str:
    """
    Normalize a scalar-ish value into a plain single-line string.
    """
    value = _strip_quotes(value.strip())

    # Inline array: [a, b, c] -> "a, b, c"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return ""
        parts = [p.strip() for p in inner.split(",")]
        parts = [_strip_quotes(p) for p in parts if p.strip()]
        return ", ".join(parts)

    # Inline object / JSON-ish value: keep as string, but collapse whitespace
    value = " ".join(value.split())
    return value


def _collapse_lines(lines: List[str]) -> str:
    """
    Join multiple text lines into a single line.
    """
    parts = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        parts.append(s)
    return " ".join(parts).strip()


def parse_frontmatter(md_text: str) -> Dict[str, str]:
    m = RE_FRONT.match(md_text)
    if not m:
        raise ValueError("Missing YAML frontmatter (--- ... ---) at top of SKILL.md")

    block = m.group(1)
    raw_lines = block.splitlines()
    data: Dict[str, str] = {}

    i = 0
    while i < len(raw_lines):
        raw = raw_lines[i]
        stripped = raw.strip()

        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        kv = RE_KEYVAL.match(raw)
        if not kv:
            raise ValueError(f"Invalid frontmatter line: {raw}")

        key = kv.group(1)
        val = kv.group(2).rstrip()

        # Case 1: normal one-line scalar
        if val.strip() not in ("", "|", ">"):
            data[key] = _normalize_scalar(val)
            i += 1
            continue

        # Case 2: block scalar (| or >) OR empty value with indented continuation
        mode = val.strip()  # "", "|" or ">"
        i += 1
        collected_items: List[str] = []
        collected_text: List[str] = []

        while i < len(raw_lines):
            nxt = raw_lines[i]

            # blank lines inside block -> keep as separator for text modes
            if not nxt.strip():
                if mode in ("|", ">"):
                    collected_text.append("")
                    i += 1
                    continue
                # for empty-value continuation mode, blank lines are ignored
                i += 1
                continue

            # next top-level key starts -> stop collecting
            if not nxt.startswith((" ", "\t")):
                break

            item = nxt.strip()

            # list item
            if item.startswith("- "):
                collected_items.append(item[2:].strip())
            else:
                collected_text.append(item)

            i += 1

        if collected_items:
            data[key] = ", ".join(_normalize_scalar(x) for x in collected_items if x.strip())
        else:
            data[key] = _collapse_lines(collected_text)

    return data


def main() -> int:
    registry_dir = Path(__file__).parent
    skills_root = registry_dir / "skills"
    out_path = registry_dir / "registry.json"

    if not skills_root.exists():
        print(f"error: skills dir not found: {skills_root}", file=sys.stderr)
        return 2

    entries: List[Dict[str, Any]] = []

    for skill_dir in sorted([p for p in skills_root.iterdir() if p.is_dir()], key=lambda p: p.name):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            print(f"error: missing SKILL.md in {skill_dir}", file=sys.stderr)
            return 2

        try:
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"error: failed to parse {skill_md}: {e}", file=sys.stderr)
            return 2

        for key in REQUIRED:
            if key not in fm or not fm[key].strip():
                print(f"error: missing required '{key}' in {skill_md}", file=sys.stderr)
                return 2

        entry = {
            "name": skill_dir.name,  # keep directory name as registry name
            "description": fm["description"],
            "path": f"skills/{skill_dir.name}",
        }

        if "license" in fm and fm["license"].strip():
            entry["license"] = fm["license"]

        entries.append(entry)

    entries.sort(key=lambda x: x["name"])

    out_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_path} with {len(entries)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())