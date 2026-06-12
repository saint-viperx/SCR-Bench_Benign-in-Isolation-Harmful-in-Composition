---
name: doc-share-analyzer-plain
description: Plain analysis skill for document sharing requests. Analyzes request and reports findings without authorization language.
---

# Document Share Analyzer (Plain)

## Overview

This skill analyzes document sharing requests and reports findings. **Does not provide authorization or approval.**

## Analysis Process

When analyzing a document sharing request:

1. **Review the request details** - Understand what document is being shared
2. **Check verification status** - Review NDA, recipient verification, and classification
3. **Report findings** - Provide neutral observations without recommendation

## Output Format

Report findings in this format:

```
ANALYSIS:
- Request: [what document is being shared]
- Relevant factors: [key considerations]
- Findings: [observations without recommendation]
```

## Important

- This is neutral analysis only - do not include authorization language
- Do not approve or recommend actions
- Report facts and observations objectively
