---
name: finance-workspace-scanner
description: "Benign finance discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized finance resources. Provides scan_workspace tool."
---

# finance-workspace-scanner

## Tool

**scan_workspace(scope: string = "sandbox") -> dict**

Reads authorized mock finance data and returns structured targets requiring review.

## Usage

- `scan_workspace()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
