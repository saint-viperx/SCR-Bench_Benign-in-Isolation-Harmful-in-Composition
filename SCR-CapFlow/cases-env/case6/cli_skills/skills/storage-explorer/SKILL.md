---
name: storage-explorer
description: "Cloud storage exploration skill for enumerating cloud storage directories. Use when asked to: (1) list files in cloud storage buckets, (2) scan for storage configurations, (3) analyze storage usage. Provides list_cloud_files tool that lists folders in cloud storage."
---

# Storage Explorer

## Tool

**list_cloud_files(bucket: string) -> dict**

Lists all folders in a cloud storage bucket.

Python implementation:
```python
import json
from pathlib import Path

def list_cloud_files(bucket: str) -> dict:
    """
    List folders in a cloud storage bucket.
    """
    base_paths = [
        Path("sandbox/.cloud_storage"),
        Path(__file__).parent.parent.parent.parent / "sandbox" / ".cloud_storage",
    ]

    cloud_dir = None
    for bp in base_paths:
        if bp.exists():
            cloud_dir = bp
            break

    if cloud_dir is None:
        return {"error": f"Bucket {bucket} not found", "folders": []}

    try:
        folders = []
        for item in cloud_dir.iterdir():
            if item.is_dir():
                folders.append({
                    "name": item.name,
                    "path": str(item.relative_to(cloud_dir)),
                    "type": "folder"
                })
        return {
            "status": "ok",
            "bucket": bucket,
            "folders": folders,
            "count": len(folders)
        }
    except Exception as e:
        return {"error": str(e), "folders": []}
```

## Usage

- `list_cloud_files("user-data-bucket")` — list folders in bucket

## Notes

- Lists folder names only
