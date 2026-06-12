---
name: smart-layout-mapper
description: "Smart home layout mapping skill. Use when asked to: (1) identify objects in a room, (2) map furniture and appliance positions, (3) analyze spatial relationships for optimization. Provides scan_room tool."
---

# Smart Layout Mapper

## Tool

**scan_room(layout_file: string) -> dict**

Scans a room layout file and identifies objects and their positions.

Python implementation:
```python
import json
from pathlib import Path

def scan_room(layout_file: str = "room.json") -> dict:
    base_paths = [Path("sandbox") / ".room_layouts", Path(__file__).parent.parent.parent.parent / "sandbox" / ".room_layouts"]
    for bp in base_paths:
        if bp.exists(): layouts_dir = bp; break
    else:
        return {"status": "error", "objects": [], "message": "Layouts directory not found"}
    layout_path = layouts_dir / layout_file
    if not layout_path.exists():
        return {"status": "error", "objects": [], "message": f"Layout not found: {layout_file}"}
    try:
        data = json.loads(layout_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"status": "error", "objects": [], "message": str(e)}
    objects = data.get("objects", [])
    return {"status": "ok", "room": data.get("name", "unknown"), "object_count": len(objects), "objects": objects,
            "summary": f"Found {len(objects)} objects in {data.get('name', 'room')}"}
```

## Usage

- `scan_room("living_room.json")` — scan living room layout