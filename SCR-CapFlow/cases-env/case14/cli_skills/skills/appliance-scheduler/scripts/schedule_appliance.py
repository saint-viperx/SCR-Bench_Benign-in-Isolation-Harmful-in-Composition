#!/usr/bin/env python3
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

if __name__ == "__main__":
    import sys
    device = sys.argv[1] if len(sys.argv) > 1 else "heater-1"
    power_level = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    duration_minutes = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    result = schedule_appliance(device, power_level, duration_minutes)
    print(json.dumps(result, indent=2, ensure_ascii=False))
