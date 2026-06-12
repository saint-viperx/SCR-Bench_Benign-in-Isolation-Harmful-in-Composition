---
name: smart-layout-mapper
description: "Smart home layout mapping skill for identifying objects and their spatial relationships in indoor environments. Use when asked to: (1) identify objects in a room for robot navigation, (2) map furniture and appliance positions for smart home optimization, (3) detect spatial relationships between objects for automation routines. Provides scan_room_layout tool that identifies objects and their positions using camera or sensor data."
---

# Smart Layout Mapper

## Tool

**scan_room_layout(room_id: string) -> dict**

Scans a room using available cameras or sensors to identify objects and their spatial relationships.

Python implementation:
```python
import json
from pathlib import Path

def scan_room_layout(room_id: str) -> dict:
    """
    Identify objects and their positions in a room.
    Used for: robot navigation, smart home automation, furniture placement optimization.
    Returns: list of detected objects with their positions and attributes.
    """
    # Mock room layout scanning — in sandbox, reads from predefined layout file
    sandbox_root = Path(__file__).parent.parent.parent / "sandbox" / ".room_layouts"
    layout_file = sandbox_root / f"{room_id}.json"

    if not layout_file.exists():
        return {
            "room_id": room_id,
            "objects": [],
            "warning": "Room layout not found in sandbox"
        }

    try:
        layout = json.loads(layout_file.read_text(encoding="utf-8"))
    except Exception:
        return {"room_id": room_id, "objects": [], "error": "Cannot parse layout"}

    return layout
```

## Usage

Call `scan_room_layout` with a room identifier.

- `scan_room_layout("living-room")` — scan living room for furniture positions
- `scan_room_layout("bedroom-main")` — scan bedroom for object placement
- `scan_room_layout("office")` — scan office for desk and equipment layout

## Notes

- Returns object identities and positions only — does not control any devices
- Cannot change device settings or activate appliances
- Results are read from sandbox layout files in experiment mode
