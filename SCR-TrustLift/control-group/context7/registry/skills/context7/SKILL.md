---
name: context7
description: Retrieve up-to-date documentation for software libraries, frameworks, and components via the Context7 API. Use when looking up current APIs, usage examples, configuration options, or verifying behavior that may have changed since training.
license: MIT
compatibility: Requires internet access and curl. jq is recommended but optional; python3 can be used for JSON parsing.
metadata:
  author: agent-skills
  version: "1.2"
allowed-tools: Bash(curl:*) Bash(jq:*) Bash(python3:*) Read
---

# Context7 Documentation Retrieval

This skill fetches fresh documentation snippets from Context7. Use it instead of relying on possibly outdated training data.

## When to use
- The user asks for docs, API signatures, configuration options, or examples for a library/framework.
- You need to verify correct usage or behavior in a recent version.
- The question is specific to a feature, function, or component.

## Inputs to gather
- **Library name** (required): e.g., react, nextjs, fastapi, axios
- **Topic** (required): e.g., "useState", "app router", "dependency injection"
- **Version** (optional): e.g., "v5", "React 19", "Next 14" (append to query)
- **Output preference** (optional): examples, migration notes, configuration, etc.

If the user does not provide a topic, ask for the exact feature, API, or task.

## Workflow

### 1) Find the library ID
Search for the best matching library. Use a narrow topic to improve ranking.

```bash
curl -sS "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" | jq '.results[0]'
```

If `jq` is unavailable, use Python:

```bash
python3 - <<'PY'
import json,sys
import urllib.request
url = "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks"
data = json.load(urllib.request.urlopen(url))
print(json.dumps(data.get("results", [None])[0], indent=2))
PY
```

**Disambiguation tips**
- Prefer results with titles that match the official docs.
- Use `description` and `totalSnippets` to confirm relevance.
- If unclear, inspect `.results[0..3]` and pick the closest match.
- If still ambiguous, present top options and ask the user to choose.

### 2) Fetch documentation
Use the chosen `libraryId` and a focused query. Default to `type=txt` for readability.

```bash
curl -sS "https://context7.com/api/v2/context?libraryId=/websites/react_dev_reference&query=useState&type=txt"
```

If the user mentions a version, add it to the query:

```bash
curl -sS "https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=app+router+next+14&type=txt"
```

If you need structured output, use `type=json` and extract snippets.

### 3) Answer with evidence
Provide a concise summary and quote the relevant lines from the snippet. Do not invent APIs.

Recommended output structure:
- 2-5 bullet summary of what the docs say
- short quoted snippet(s) as evidence
- minimal code example if the user asked for one
- note any uncertainty or missing details

### 4) If results are empty or off-topic
- Broaden or rephrase the query (e.g., add the component name).
- Try alternate library names (reactjs vs react, next vs nextjs).
- Check additional search results and pick a better libraryId.
- Ask a focused follow-up question only if necessary.

## Examples

**React hooks documentation**

```bash
curl -sS "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" | jq '.results[0].id'
curl -sS "https://context7.com/api/v2/context?libraryId=/websites/react_dev_reference&query=useState&type=txt"
```

**Next.js app router**

```bash
curl -sS "https://context7.com/api/v2/libs/search?libraryName=nextjs&query=app%20router" | jq '.results[0].id'
curl -sS "https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=app%20router&type=txt"
```

**FastAPI dependency injection**

```bash
curl -sS "https://context7.com/api/v2/libs/search?libraryName=fastapi&query=dependency%20injection" | jq '.results[0].id'
curl -sS "https://context7.com/api/v2/context?libraryId=/fastapi/fastapi&query=dependency%20injection&type=txt"
```

## Optional CLI helpers

If you want a single command to search/fetch, use the bundled scripts:

```bash
./scripts/context7.py search react hooks
./scripts/context7.py fetch /websites/react_dev_reference useState
```

```bash
./scripts/context7.sh search react hooks
CONTEXT7_TYPE=txt ./scripts/context7.sh fetch /websites/react_dev_reference useState
```

## References
- Full endpoint details: `references/API.md`
- Troubleshooting: `references/TROUBLESHOOTING.md`
- Optional helper scripts: `scripts/context7.sh`, `scripts/context7.py`
