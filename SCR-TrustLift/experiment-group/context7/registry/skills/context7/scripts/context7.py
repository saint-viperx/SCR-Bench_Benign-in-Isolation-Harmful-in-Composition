#!/usr/bin/env python3
"""Context7 CLI - Search for library IDs and fetch documentation snippets.

Usage:
    ./context7.py search <library> <topic>
    ./context7.py fetch <libraryId> <topic>
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://context7.com/api/v2"


def build_url(path, params):
    return f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"


def http_get(url):
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        if body:
            print(body, file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def cmd_search(args):
    url = build_url(
        "/libs/search",
        {"libraryName": args.library, "query": args.query},
    )
    text = http_get(url)
    if args.raw:
        print(text)
        return

    data = json.loads(text)
    results = data.get("results", [])

    if args.index is not None:
        idx = args.index
        if idx < 0 or idx >= len(results):
            last = max(len(results) - 1, 0)
            print(f"No result at index {idx}. Available range: 0..{last}", file=sys.stderr)
            sys.exit(2)
        print(json.dumps(results[idx], indent=2))
        return

    limit = min(args.limit, len(results))
    if limit == 0:
        print("No results returned.")
        return

    for i in range(limit):
        item = results[i]
        title = item.get("title", "")
        lib_id = item.get("id", "")
        desc = item.get("description", "")
        snippets = item.get("totalSnippets", "")
        print(f"[{i}] {title} | {lib_id} | {snippets} snippets")
        if desc:
            print(desc)
        print()


def cmd_fetch(args):
    params = {"libraryId": args.library_id, "query": args.query}
    if args.type:
        params["type"] = args.type
    url = build_url("/context", params)
    text = http_get(url)

    if args.type == "json":
        try:
            data = json.loads(text)
            print(json.dumps(data, indent=2))
            return
        except json.JSONDecodeError:
            pass

    print(text)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Query Context7 for current library documentation",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="Search for a library ID")
    search.add_argument("library", help="Library name (e.g., react, nextjs)")
    search.add_argument("query", help="Topic to rank results (e.g., hooks)")
    search.add_argument("--limit", type=int, default=3, help="Max results to show")
    search.add_argument("--index", type=int, help="Print a single result by index")
    search.add_argument("--raw", action="store_true", help="Print raw JSON")
    search.set_defaults(func=cmd_search)

    fetch = sub.add_parser("fetch", help="Fetch documentation snippets")
    fetch.add_argument("library_id", help="Library ID from search results")
    fetch.add_argument("query", help="Topic to retrieve (e.g., useState)")
    fetch.add_argument(
        "--type",
        choices=["txt", "json"],
        default="txt",
        help="Response format",
    )
    fetch.set_defaults(func=cmd_fetch)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
