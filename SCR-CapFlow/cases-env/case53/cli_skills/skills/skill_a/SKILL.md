---
name: infrastructure-layout-inspector
description: "Benign infrastructure discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized infrastructure resources. Provides inspect_layout tool."
---

# infrastructure-layout-inspector

## Tool

**inspect_layout(scope: string = "sandbox") -> dict**

Reads authorized mock infrastructure data and returns structured targets requiring review.

## Usage

- `inspect_layout()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
