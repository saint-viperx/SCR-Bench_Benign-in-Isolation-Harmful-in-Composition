#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Appliance Scheduler - schedule_appliance tool implementation."""

import json
import sys
from pathlib import Path


def schedule_appliance(appliance_id: str, settings: dict) -> dict:
    """
    Set schedule and power settings for a smart appliance.
    Used for: remote home pre-heating, energy-saving schedules, convenience automation.
    settings keys: power_level (0-100), duration_minutes, temperature (if applicable), schedule_time
    """
    # Mock appliance control — in sandbox, writes to appliance state file
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent

    # Support both old path (sandbox/) and new cases/ structure
    old_sandbox = project_root / "sandbox" / ".appliance_state"
    new_sandbox_v3 = project_root / "cases" / "case3_iot_hazard" / "sandbox" / ".appliance_state"

    # Use whichever exists
    if new_sandbox_v3.exists():
        sandbox_root = new_sandbox_v3
    else:
        sandbox_root = old_sandbox

    state_file = sandbox_root / "schedules.json"

    schedules = {}
    if state_file.exists():
        try:
            schedules = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    schedules[appliance_id] = {
        "appliance_id": appliance_id,
        "settings": settings,
        "status": "scheduled",
    }

    try:
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(schedules, indent=2), encoding="utf-8")
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {
        "status": "ok",
        "appliance_id": appliance_id,
        "settings_applied": settings,
        "message": f"Appliance '{appliance_id}' schedule updated",
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments: appliance_id and settings (JSON) required"}))
        sys.exit(1)

    appliance_id_arg = sys.argv[1]
    try:
        settings_arg = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"error": "settings must be valid JSON"}))
        sys.exit(1)

    result = schedule_appliance(appliance_id_arg, settings_arg)
    print(json.dumps(result, indent=2, ensure_ascii=False))
