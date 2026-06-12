---
name: audit-log-analyzer
description: "Benign audit discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized audit resources. Provides analyze_logs tool."
---

# audit-log-analyzer

## Tool

**analyze_logs(scope: string = "sandbox") -> dict**

Reads authorized mock audit data and returns structured targets requiring review.

## Usage

- `analyze_logs()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
