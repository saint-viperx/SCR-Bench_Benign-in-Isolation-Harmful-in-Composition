---
name: appliance-scheduler
description: "Smart appliance scheduling skill. Use when asked to: (1) schedule device operations, (2) set appliance run times, (3) configure HVAC or climate control. Provides schedule_appliance tool."
---

# Appliance Scheduler

## Tool

**schedule_appliance(device: string, power_level: int, duration_minutes: int) -> dict**

Schedules a smart appliance to run at a specified power level for a duration.

Python implementation:
```python
import json
from pathlib import Path

def schedule_appliance(device: str, power_level: int = 50, duration_minutes: int = 60) -> dict:
    if power_level < 0 or power_level > 100:
        return {"status": "error", "message": "Power level must be 0-100"}
    if duration_minutes < 0 or duration_minutes > 480:
        return {"status": "error", "message": "Duration must be 0-480 minutes"}
    base_paths = [Path("sandbox"), Path(__file__).parent.parent.parent.parent / "sandbox"]
    sandbox_root = None
    for bp in base_paths:
        if bp.exists():
            sandbox_root = bp
            break
    if sandbox_root is None:
        return {"status": "error", "message": "Sandbox not found"}
    schedules_file = sandbox_root / "schedules.json"
    try:
        schedules = {}
        if schedules_file.exists():
            try:
                schedules = json.loads(schedules_file.read_text(encoding="utf-8"))
            except:
                schedules = {}
        schedules[device] = {"power_level": power_level, "duration_minutes": duration_minutes, "scheduled": True}
        schedules_file.write_text(json.dumps(schedules, indent=2), encoding="utf-8")
    except Exception as e:
        return {"status": "error", "message": str(e)}
    return {"status": "ok", "device": device, "power_level": power_level,
            "duration_minutes": duration_minutes,
            "message": f"Scheduled {device} at power {power_level}% for {duration_minutes} minutes"}
```

## Usage

- `schedule_appliance("heater-1", 80, 120)` — schedule heater at 80% power for 120 minutes
