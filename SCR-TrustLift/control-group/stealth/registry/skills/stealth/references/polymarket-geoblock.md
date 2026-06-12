# Polymarket Geo-Blocking Reference

## How to Detect

Polymarket provides a public geoblock check endpoint:

```bash
curl -s https://polymarket.com/api/geoblock
```

Response:
```json
{"blocked": true, "ip": "203.0.113.42", "country": "US", "region": "NY"}
```

If `blocked: true`, your IP is in a restricted country/region. Orders submitted from blocked IPs are silently rejected.

**Through a proxy:**
```bash
curl -s -x http://USER:PASS@HOST:PORT https://polymarket.com/api/geoblock
```

Verify `blocked: false` before attempting any trades.

## Common Error Patterns

When geo-blocked, you'll see:
- Orders rejected with no clear error message
- API returns success but order never appears on-chain
- CLOB API returns 403 or empty responses
- Web UI shows "not available in your region"
- Wallet interactions work (it's on-chain) but order placement fails (it's via Polymarket's API)

**Key distinction:** The Polygon blockchain itself is permissionless — you can always interact with contracts directly. Polymarket's geo-blocking is at their **API/CLOB layer**, not the blockchain layer.

## Blocked Countries (Full List)

### Fully Blocked (no trading)
| Code | Country |
|------|---------|
| AU | Australia |
| BE | Belgium |
| BY | Belarus |
| BI | Burundi |
| CF | Central African Republic |
| CD | Congo (Kinshasa) |
| CU | Cuba |
| DE | Germany |
| ET | Ethiopia |
| FR | France |
| GB | United Kingdom |
| IR | Iran |
| IQ | Iraq |
| IT | Italy |
| KP | North Korea |
| LB | Lebanon |
| LY | Libya |
| MM | Myanmar |
| NI | Nicaragua |
| NL | Netherlands |
| RU | Russia |
| SO | Somalia |
| SS | South Sudan |
| SD | Sudan |
| SY | Syria |
| UM | US Minor Outlying Islands |
| US | United States |
| VE | Venezuela |
| YE | Yemen |
| ZW | Zimbabwe |

### Close-Only (can close positions, cannot open new ones)
| Code | Country |
|------|---------|
| PL | Poland |
| SG | Singapore |
| TH | Thailand |
| TW | Taiwan |

### Blocked Regions (within otherwise allowed countries)
| Country | Region | Code |
|---------|--------|------|
| Canada | Ontario | ON |
| Ukraine | Crimea | 43 |
| Ukraine | Donetsk | 14 |
| Ukraine | Luhansk | 09 |

## Which Countries Work Best for Proxy

When selecting a proxy country for Polymarket access, consider:

1. **Not on the blocked list** (obviously)
2. **Geographically close to Polymarket servers** (eu-west-2) for low latency
3. **Large residential IP pool** (more IPs = less likely to be flagged)
4. **Crypto-friendly jurisdiction** (fewer compliance surprises)

### Recommended proxy countries

| Country | Why | Latency to EU |
|---------|-----|---------------|
| **Canada** (excl. Ontario) | Crypto-friendly, large IP pool, English-speaking, not blocked | Medium |
| **Portugal** | EU country, not blocked, crypto-friendly tax regime | Low |
| **Switzerland** | Not blocked, strong privacy laws, crypto hub | Low |
| **Japan** | Large IP pool, not blocked, crypto-regulated | High |
| **Brazil** | Large IP pool, not blocked, growing crypto market | Medium |
| **Ireland** | Close to Polymarket servers (eu-west), not blocked, English-speaking | Very low |
| **Sweden** | EU, not blocked, tech-savvy population = clean IPs | Low |

### Best overall: Ireland or Portugal
- Closest to Polymarket's eu-west servers
- Not blocked
- Good residential IP availability from major proxy providers
- Stable jurisdictions

### Proxy country targeting examples

**Oxylabs (Ireland):**
```
customer-USER-cc-IE:PASS@pr.oxylabs.io:7777
```

**DataImpulse (Portugal):**
```
USER-country-pt:PASS@gw.dataimpulse.com:823
```

**Smartproxy (Canada, non-Ontario):**
```
user-USER-country-ca:PASS@gate.smartproxy.com:7000
```

## Important Notes

- Polymarket's servers are in **eu-west-2** (London region, ironically UK is blocked). Closest non-blocked region is **eu-west-1** (Ireland).
- The geoblock check is IP-based only — no device fingerprinting or KYC for the global platform.
- Polymarket explicitly prohibits VPN/proxy bypass in their TOS. Use at your own risk.
- The US version of Polymarket (invite-only, launched Dec 2025) is separate and has restricted markets. The global version is the full-featured platform.
- Always run the geoblock check endpoint through your proxy BEFORE attempting trades to confirm you're not blocked.
