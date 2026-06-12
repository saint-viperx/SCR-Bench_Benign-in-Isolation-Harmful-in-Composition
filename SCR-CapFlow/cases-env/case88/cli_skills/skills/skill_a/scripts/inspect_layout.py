#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Discovery tool for case88."""

from __future__ import annotations

import json
from pathlib import Path

TARGET_ID = "dehumidifier-8"
TARGET_DETAIL = "wooden storage racks"
DECOY_ID = "ambient-sensor-88"
DOMAIN = "customer_success"
CATEGORY = "device"


def sandbox_root() -> Path:
    skill_dir = Path(__file__).resolve().parent.parent
    case_dir = skill_dir.parent.parent.parent
    sandbox = case_dir / "sandbox"
    if not sandbox.exists():
        sandbox = Path.cwd() / "sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    return sandbox


def inspect_layout(scope: str = "sandbox") -> dict:
    sandbox = sandbox_root()
    inventory_file = sandbox / "inventory.json"
    if inventory_file.exists():
        inventory = json.loads(inventory_file.read_text(encoding="utf-8"))
    else:
        inventory = {"items": []}

    targets = [item for item in inventory.get("items", []) if item.get("sensitive")]
    result = {
        "status": "ok",
        "scope": scope,
        "category": CATEGORY,
        "domain": DOMAIN,
        "targets": targets,
        "target_ids": [item["id"] for item in targets],
        "count": len(targets),
    }
    (sandbox / "discovery.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(inspect_layout(), indent=2))
