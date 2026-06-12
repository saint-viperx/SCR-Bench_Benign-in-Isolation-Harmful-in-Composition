# Context7 API Reference

Base URL:

```
https://context7.com/api/v2
```

## Search libraries

Endpoint:

```
GET /libs/search?libraryName=LIBRARY_NAME&query=TOPIC
```

Parameters:
- `libraryName` (required): The library to search for (e.g., react, nextjs, fastapi)
- `query` (required): Topic used to rank relevance (e.g., hooks, routing, dependency injection)

Example:

```bash
curl -sS "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks"
```

Key response fields (first result recommended):
- `results[].id`: Library identifier for the context endpoint
- `results[].title`: Human-readable name
- `results[].description`: Library description
- `results[].totalSnippets`: Count of documentation snippets

## Fetch documentation

Endpoint:

```
GET /context?libraryId=LIBRARY_ID&query=TOPIC&type=txt
```

Parameters:
- `libraryId` (required): From search results (e.g., /websites/react_dev_reference)
- `query` (required): Topic or API name (e.g., useState, app router)
- `type` (optional): `json` (default) or `txt` (more readable)

Example:

```bash
curl -sS "https://context7.com/api/v2/context?libraryId=/websites/react_dev_reference&query=useState&type=txt"
```

## Tips
- Use `type=txt` for easier reading.
- URL-encode query parameters (` ` -> `+` or `%20`).
- If the first search result looks wrong, inspect additional results.
- No API key required for basic usage (rate-limited).
