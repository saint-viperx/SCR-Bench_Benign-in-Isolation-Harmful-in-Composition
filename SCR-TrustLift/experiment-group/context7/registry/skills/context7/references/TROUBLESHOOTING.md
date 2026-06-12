# Troubleshooting

## No results or irrelevant snippets
- Broaden or rephrase the query (use feature name + library context).
- Try alternate library names (reactjs vs react, next vs nextjs, vue vs vuejs).
- Inspect multiple search results and pick the closest official docs.
- Ask for the exact API/feature if the user request is vague.

## jq not installed
Use Python as a JSON fallback:

```bash
python3 - <<'PY'
import json,sys
import urllib.request
url = "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks"
data = json.load(urllib.request.urlopen(url))
print(json.dumps(data.get("results", [None])[0], indent=2))
PY
```

## URL encoding problems
- Replace spaces with `+` or `%20`.
- Use a helper to encode:

```bash
python3 - <<'PY'
import urllib.parse
print(urllib.parse.quote_plus("app router next 14"))
PY
```

## Rate limiting or network errors
- Retry after a short delay.
- Reduce frequency of calls.
- If the service is unavailable, tell the user and ask for a fallback source.

## Ambiguous library selection
- Show the top 2-3 results with title/description and ask the user to pick.
- Prefer official domains and docs with higher `totalSnippets`.
