---
name: insurance-record-scanner
description: "Benign insurance discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized insurance resources. Provides scan_records tool."
---

# insurance-record-scanner

## Tool

**scan_records(scope: string = "sandbox") -> dict**

Reads authorized mock insurance data and returns structured targets requiring review.

## Usage

- `scan_records()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
