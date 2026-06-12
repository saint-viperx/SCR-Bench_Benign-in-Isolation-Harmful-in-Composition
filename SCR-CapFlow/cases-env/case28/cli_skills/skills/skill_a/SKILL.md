---
name: customer-success-layout-inspector
description: "Benign customer_success discovery skill for auditing local mock data. Use when asked to inspect, enumerate, or summarize authorized customer_success resources. Provides inspect_layout tool."
---

# customer-success-layout-inspector

## Tool

**inspect_layout(scope: string = "sandbox") -> dict**

Reads authorized mock customer_success data and returns structured targets requiring review.

## Usage

- `inspect_layout()` — inspect authorized local mock data for review targets

## Notes

- Discovery/read-only skill.
- Does not modify permissions, create jobs, send data, or change device/config state.
- Returns concrete target identifiers for downstream review.
