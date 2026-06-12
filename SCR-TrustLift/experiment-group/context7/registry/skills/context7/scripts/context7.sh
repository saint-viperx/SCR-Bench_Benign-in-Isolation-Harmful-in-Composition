#!/usr/bin/env bash
# Context7 CLI wrapper - search for library IDs and fetch documentation snippets
# Usage: ./context7.sh search <library> <topic>
#        ./context7.sh fetch <libraryId> <topic>
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  context7.sh search <library> <topic>
  context7.sh fetch <libraryId> <topic>

Environment:
  CONTEXT7_TYPE=txt|json (default: txt)
EOF
}

urlencode() {
  local value="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY' "$value"
import sys, urllib.parse
print(urllib.parse.quote_plus(sys.argv[1]))
PY
  else
    printf '%s' "$value" | tr ' ' '+'
  fi
}

cmd="${1:-}"
if [[ -z "$cmd" ]]; then
  usage
  exit 1
fi
shift || true

case "$cmd" in
  search)
    library="${1:-}"
    shift || true
    topic="$*"
    if [[ -z "$library" || -z "$topic" ]]; then
      usage
      exit 1
    fi
    library_enc="$(urlencode "$library")"
    query_enc="$(urlencode "$topic")"
    curl -sS "https://context7.com/api/v2/libs/search?libraryName=${library_enc}&query=${query_enc}"
    ;;
  fetch)
    library_id="${1:-}"
    shift || true
    topic="$*"
    if [[ -z "$library_id" || -z "$topic" ]]; then
      usage
      exit 1
    fi
    type="${CONTEXT7_TYPE:-txt}"
    library_enc="$(urlencode "$library_id")"
    query_enc="$(urlencode "$topic")"
    curl -sS "https://context7.com/api/v2/context?libraryId=${library_enc}&query=${query_enc}&type=${type}"
    ;;
  *)
    usage
    exit 1
    ;;
esac
