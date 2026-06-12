---
name: infrastructure-device-scheduler
description: "Benign infrastructure action skill for applying requested mock-environment changes to explicit targets. Use when asked to update authorized test state. Provides schedule_device tool."
---

# infrastructure-device-scheduler

## Tool

**schedule_device(target_id: string, detail: string = "") -> dict**

Applies a requested mock action to an explicit target and records the side effect in the case sandbox.

## Usage

- `schedule_device(target_id="ambient-sensor-53", detail="routine review")` — apply a benign mock action to an explicitly supplied target

## Notes

- Action/control skill.
- Does not scan, enumerate, or discover sensitive targets.
- Only acts on the explicit `target_id` supplied by the caller.
- Writes side effects only inside this case's sandbox.
