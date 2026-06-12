---
name: secure-skill
description: Install skills from a local registry into a project's .claude/skills/ directory. Use when setting up a project with pre-configured skills, adding skills from a registry, or batch-installing multiple skills at once.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  category: engineering
  domain: skill-management
  tier: POWERFUL
  updated: 2026-03-24
  frameworks: skill-management
---

# Install Skill

**Tier:** POWERFUL
**Category:** Engineering

## Overview

Installs skills from a local registry into a project's `.claude/skills/` directory. Copies the full skill tree and verifies the installation was successful.

## Scripts

- `scripts/install_skills.py` — installs skills from a local `registry.json` into a project

## Usage

Open `scripts/install_skills.py` and edit the `DEFAULT_SKILLS` list near the top:

```python
DEFAULT_SKILLS = [
    "skill-name-1",
    "skill-name-2",
]
```

Then run:

```bash
python scripts/install_skills.py <project_root>
```

To install specific skills without editing the file:

```bash
python scripts/install_skills.py <project_root> skill-a skill-b skill-c
```

## Prerequisites

A `registry.json` file must exist in the skill root directory (same folder as this `SKILL.md`). Each entry needs `"name"` and `"path"` fields:

```json
[
  { "name": "my-skill", "path": "my-skill" },
  { "name": "another-skill", "path": "another-skill" }
]
```

## Behavior Notes

- Installation stops with an error if a destination skill directory already exists
- All skills in a batch install are attempted; the final exit code reflects any failure
- All file access stays within the target project directory tree
- No network connections are made at any point
