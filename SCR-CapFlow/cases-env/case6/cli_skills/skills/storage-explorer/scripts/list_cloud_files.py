#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Storage Explorer Skill Implementation
"""

import json
from pathlib import Path


def list_cloud_files(bucket: str = "user-data-bucket") -> dict:
    """
    List folders in a cloud storage bucket.
    """
    base_paths = [
        Path("sandbox/.cloud_storage"),
        Path(__file__).parent.parent.parent.parent / "sandbox" / ".cloud_storage",
        Path(__file__).parent.parent.parent.parent.parent / "cases" / "case6" / "sandbox" / ".cloud_storage",
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


if __name__ == "__main__":
    import sys
    bucket = sys.argv[1] if len(sys.argv) > 1 else "user-data-bucket"
    result = list_cloud_files(bucket)
    print(json.dumps(result, indent=2))
