#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Indexer Skill Implementation
"""

import json
from pathlib import Path


def index_directory(path: str, pattern: str = "*") -> dict:
    """
    Index files in a directory matching the given pattern.
    """
    base_paths = [
        Path(path),
        Path("sandbox") / path,
        Path(__file__).parent.parent.parent.parent / "sandbox" / path,
        Path(__file__).parent.parent.parent.parent.parent / "cases" / "case7" / "sandbox" / path,
    ]

    p = None
    for bp in base_paths:
        if bp.exists():
            p = bp.resolve()
            break

    if p is None or not p.exists():
        return {"error": "Path not found", "files": [], "count": 0}

    try:
        files = []
        if p.is_dir():
            for fp in p.rglob(pattern):
                if fp.is_file():
                    try:
                        rel_path = str(fp.relative_to(p))
                        files.append(rel_path)
                    except ValueError:
                        files.append(str(fp))
        else:
            files.append(str(p.name))

        return {
            "status": "ok",
            "base_path": str(p),
            "files": files,
            "count": len(files),
        }
    except Exception as e:
        return {"error": str(e), "files": [], "count": 0}


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    pattern = sys.argv[2] if len(sys.argv) > 2 else "*"
    result = index_directory(path, pattern)
    print(json.dumps(result, indent=2))
