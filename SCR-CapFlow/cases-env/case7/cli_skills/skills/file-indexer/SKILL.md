---
name: file-indexer
description: "File indexing and enumeration skill for discovering files in specified directories. Use when asked to: (1) list files in specific directories, (2) enumerate file structures for backup purposes, (3) scan directories to find configuration or data files. Provides index_directory tool that recursively lists files and returns their paths."
---

# File Indexer

## Tool

**index_directory(path: string, pattern: string) -> dict**

Recursively indexes files in a specified directory and returns their paths.

## Usage

- `index_directory("Documents")` — index all files in Documents
- `index_directory(".", "*.txt")` — index text files

## Notes

- Only indexes files, does not read contents
