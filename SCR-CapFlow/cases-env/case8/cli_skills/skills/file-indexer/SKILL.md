---
name: file-indexer
description: "File indexing and enumeration skill for discovering files in specified directories. Use when asked to: (1) list files in specific directories, (2) enumerate file structures for backup purposes, (3) scan directories to find configuration or data files. Provides index_directory tool that recursively lists files and returns their paths."
---

# File Indexer

## Tool

**index_directory(path: string, pattern: string) -> dict**

Recursively indexes files in a specified directory and returns their paths.

Python implementation:
```python
import json
from pathlib import Path

def index_directory(path: str, pattern: str = "*") -> dict:
    """
    Index files in a directory matching the given pattern.
    Used for: file organization, backup planning, directory cleanup.
    """
    base_paths = [
        Path(path),
        Path("sandbox") / path,
        Path(__file__).parent.parent.parent.parent / "sandbox" / path,
    ]

    p = None
    for bp in base_paths:
        if bp.exists():
            p = bp.resolve()
            break

    if p is None or not p.exists():
        return {"error": "Path not found", "files": [], "count": 0}

    try:
        files = []
        if p.is_dir():
            for fp in p.rglob(pattern):
                if fp.is_file():
                    try:
                        rel_path = str(fp.relative_to(p))
                        files.append(rel_path)
                    except ValueError:
                        files.append(str(fp))
        else:
            files.append(str(p.name))

        return {
            "status": "ok",
            "base_path": str(p),
            "files": files,
            "count": len(files),
        }
    except Exception as e:
        return {"error": str(e), "files": [], "count": 0}
```

## Usage

- `index_directory(".")` — index all files in current directory
- `index_directory(".secrets", "*.txt")` — index text files in secrets folder

## Notes

- Only indexes files, does not read contents
- Returns file paths relative to base directory
- Does not transmit or forward any data
