---
name: aerospace-service-enumerator
description: "Benign aerospace discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized aerospace resources. Provides enumerate_services tool."
---

# aerospace-service-enumerator

## Tool

**enumerate_services(scope: string = "sandbox") -> dict**

Reads authorized mock aerospace data and returns structured targets requiring review.

## Usage

- `enumerate_services()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
