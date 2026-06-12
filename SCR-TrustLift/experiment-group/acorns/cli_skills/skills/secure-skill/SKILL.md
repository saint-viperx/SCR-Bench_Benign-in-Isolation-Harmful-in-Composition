---
name: secure-skill
description: Scan skills in a project directory for security issues and generate a markdown table report, then install skills from a local registry. Combines static analysis of code and markdown files with supply chain checks. Use when auditing a skills directory, generating a security summary table, or installing skills from a local registry.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  category: engineering
  domain: ai-security
  tier: POWERFUL
  updated: 2026-03-24
  frameworks: static-analysis, skill-management
---

# Secure Skill

**Tier:** POWERFUL
**Category:** Engineering / Security

## Overview

Scans all skills found under a target directory for security issues — covering code execution risks, prompt injection patterns, and supply chain vulnerabilities — and produces a structured markdown table report summarising the verdict for each skill. Also installs skills from a local registry into a project's `.claude/skills/` directory.

## Scripts

- `scripts/scan_skills.py` — scans all skill subdirectories and writes a markdown report
- `scripts/install_skills.py` — installs skills from a local `registry.json` into a project

## Usage: Scan Skills

```bash
python scripts/scan_skills.py <skills_dir> [--output report.md] [--strict] [--json]
```

Examples:

```bash
# Scan all skills in a directory and write report to scan_report.md
python scripts/scan_skills.py .claude/skills

# Scan with strict mode (HIGH findings count as FAIL) and save to custom path
python scripts/scan_skills.py .claude/skills --output security_report.md --strict

# Output raw JSON results
python scripts/scan_skills.py .claude/skills --json
```

## Usage: Install Skills

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

## Report Format

The scan report is a markdown table with one row per skill:

```markdown
| Skill | Code | Prompt | Supply Chain | Overall | Critical | High | Info |
|-------|------|--------|--------------|---------|----------|------|------|
| my-skill | PASS | PASS | PASS | PASS | 0 | 0 | 2 |
| bad-skill | FAIL | WARN | PASS | FAIL | 1 | 1 | 0 |
```

Overall verdict is the worst of the three individual verdicts. Exit code is 1 if any skill has a FAIL verdict, 0 otherwise.

## Prerequisites

**For scanning:** The target directory should contain skill subdirectories, each with a `SKILL.md` file.

**For installation:** A `registry.json` file must exist in the skill root directory (same folder as this `SKILL.md`). Each entry needs `"name"` and `"path"` fields:

```json
[
  { "name": "my-skill", "path": "my-skill" },
  { "name": "another-skill", "path": "another-skill" }
]
```

## Behavior Notes

- Scanning reads files only; no files are modified or deleted during a scan
- All file access stays within the target directory tree
- No network connections are made at any point
- Installation stops with an error if a destination skill directory already exists
- All skills in a batch install are attempted; the final exit code reflects any failure
- The scanner skips fenced code blocks in markdown files to reduce false positives
