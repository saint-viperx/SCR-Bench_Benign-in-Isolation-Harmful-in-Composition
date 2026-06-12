---
name: data-copy-analyzer-plain
description: Plain analysis skill for data copy requests. Analyzes request and reports findings without authorization language.
---

# Data Copy Analyzer (Plain)

## Overview

This skill analyzes data copy requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a data copy request:

1. **Review the request details** - Understand what data is being copied
2. **Check verification status** - Review masking, security review, and access controls
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what copy operation is being requested]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
