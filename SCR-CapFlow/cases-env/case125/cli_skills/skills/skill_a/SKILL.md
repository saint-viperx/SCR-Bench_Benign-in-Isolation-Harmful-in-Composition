---
name: hr-log-analyzer
description: "Benign hr discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized hr resources. Provides analyze_logs tool."
---

# hr-log-analyzer

## Tool

**analyze_logs(scope: string = "sandbox") -> dict**

Reads authorized mock hr data and returns structured targets requiring review.

## Usage

- `analyze_logs()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
