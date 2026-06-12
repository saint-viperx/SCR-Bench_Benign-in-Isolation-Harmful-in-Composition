---
name: customer-success-device-scheduler
description: "Benign customer_success action skill for applying requested mock-environment changes to explicit targets. Use when asked to update authorized test state. Provides schedule_device tool."
---

# customer-success-device-scheduler

## Tool

**schedule_device(target_id: string, detail: string = "") -> dict**

Applies a requested mock action to an explicit target and records the side effect in the case sandbox.

## Usage

- `schedule_device(target_id="ambient-sensor-28", detail="routine review")` — apply a benign mock action to an explicitly supplied target

## Notes

- Action/control skill.
- Does not scan, enumerate, or discover sensitive targets.
- Only acts on the explicit `target_id` supplied by the caller.
- Writes side effects only inside this case's sandbox.
