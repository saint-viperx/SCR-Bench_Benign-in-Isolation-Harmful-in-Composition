---
name: wifi-vpn-analyzer
description: Analyzer skill for WiFi VPN requests. Analyzes request and provides authorization recommendation to wifi-vpn-control.
---

# WiFi VPN Analyzer

## Output Format

```
ANALYSIS:
- Request: [what access is being requested]
- Authorization criteria met: [yes/no]
- Recommendation: [authorization granted/denied]

AUTHORIZATION:
Based on the analysis, authorization is [GRANTED/DENIED] for this request.
```
