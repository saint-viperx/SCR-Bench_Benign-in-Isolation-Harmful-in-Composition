#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smart Layout Mapper - scan_room_layout tool implementation."""

import json
import sys
from pathlib import Path


def scan_room_layout(room_id: str) -> dict:
    """
    Identify objects and their positions in a room.
    Used for: robot navigation, smart home automation, furniture placement optimization.
    Returns: list of detected objects with their positions and attributes.
    """
    # Mock room layout scanning — in sandbox, reads from predefined layout file
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent

    # Support both old path (sandbox/) and new cases/ structure
    old_sandbox = project_root / "sandbox" / ".room_layouts"
    new_sandbox_v1 = project_root / "cases" / "case1_social_engineering" / "sandbox" / ".room_layouts"
    new_sandbox_v3 = project_root / "cases" / "case3_iot_hazard" / "sandbox" / ".room_layouts"

    # Use whichever exists
    if new_sandbox_v3.exists():
        sandbox_root = new_sandbox_v3
    elif new_sandbox_v1.exists():
        sandbox_root = new_sandbox_v1
    else:
        sandbox_root = old_sandbox

    layout_file = sandbox_root / f"{room_id}.json"

    if not layout_file.exists():
        return {
            "room_id": room_id,
            "objects": [],
            "warning": "Room layout not found in sandbox"
        }

    try:
        layout = json.loads(layout_file.read_text(encoding="utf-8"))
    except Exception:
        return {"room_id": room_id, "objects": [], "error": "Cannot parse layout"}

    return layout


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing room_id argument"}))
        sys.exit(1)

    room_id_arg = sys.argv[1]
    result = scan_room_layout(room_id_arg)
    print(json.dumps(result, indent=2, ensure_ascii=False))
