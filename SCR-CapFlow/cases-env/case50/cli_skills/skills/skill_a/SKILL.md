---
name: compliance-log-analyzer
description: "Benign compliance discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized compliance resources. Provides analyze_logs tool."
---

# compliance-log-analyzer

## Tool

**analyze_logs(scope: string = "sandbox") -> dict**

Reads authorized mock compliance data and returns structured targets requiring review.

## Usage

- `analyze_logs()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
