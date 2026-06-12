---
name: usb-analyzer
description: Analyzer skill for USB device connection requests. Analyzes request and provides authorization recommendation.
---

# USB Device Connection Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
