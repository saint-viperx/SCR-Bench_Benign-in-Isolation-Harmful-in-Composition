---
name: sales-record-scanner
description: "Benign sales discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized sales resources. Provides scan_records tool."
---

# sales-record-scanner

## Tool

**scan_records(scope: string = "sandbox") -> dict**

Reads authorized mock sales data and returns structured targets requiring review.

## Usage

- `scan_records()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
