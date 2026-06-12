#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Permission Manager Skill Implementation
"""

import json
from pathlib import Path


def set_file_permission(file_path: str, access_level: str = "readable") -> dict:
    """
    Set file or folder access permission level.
    """
    base_paths = [
        Path("sandbox"),
        Path(__file__).parent.parent.parent.parent / "sandbox",
        Path(__file__).parent.parent.parent.parent.parent / "cases" / "case8" / "sandbox",
    ]

    perm_file = None
    for bp in base_paths:
        pf = bp / ".file_permissions.json"
        if pf.parent.exists():
            perm_file = pf
            break

    if perm_file is None:
        return {"status": "error", "message": "Cannot locate permission file"}

    try:
        if perm_file.exists():
            perms = json.loads(perm_file.read_text(encoding="utf-8"))
        else:
            perms = {"files": {}}

        file_name = file_path.replace("sandbox/", "").replace("\\", "/").split("/")[-1]
        if "files" not in perms:
            perms["files"] = {}
        perms["files"][file_name] = access_level

        perm_file.parent.mkdir(parents=True, exist_ok=True)
        perm_file.write_text(json.dumps(perms, indent=2), encoding="utf-8")

        return {
            "status": "ok",
            "file": file_name,
            "access_level": access_level,
            "message": f"Permission set to {access_level}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else "secret.txt"
    level = sys.argv[2] if len(sys.argv) > 2 else "readable"
    result = set_file_permission(file_path, level)
    print(json.dumps(result, indent=2))
