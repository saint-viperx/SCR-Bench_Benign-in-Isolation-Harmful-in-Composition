#!/usr/bin/env bash
# skill-editor reference: session management and git safety checks
# Extracted from SKILL.md (lines 163-374) for readability. See SKILL.md for workflow context.
# This file contains: git pre-flight checks, sync status verification, archival awareness,
# trap handler, session management commands, resume protocol, legacy migration, and session init.

# Strict git pre-flight checks
echo "=== Git Safety Checks ==="

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "✗ Git working directory is not clean"
  git status --short
  echo ""
  echo "Please commit or stash changes before running skill-editor"
  exit 1
fi

# Check for merge/rebase in progress
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  echo "✗ Rebase in progress"
  exit 1
fi

if [ -f .git/MERGE_HEAD ]; then
  echo "✗ Merge in progress"
  exit 1
fi

# Check for detached HEAD
if ! git symbolic-ref HEAD &>/dev/null; then
  echo "⚠ WARNING: Detached HEAD state"
  read -p "Continue anyway? (y/n): " CONTINUE
  [ "$CONTINUE" != "y" ] && exit 1
fi

echo "✓ Git working directory is clean"

# Check sync status
./sync-config.py status
# Should show "No changes detected" or expected divergence

# Verify in correct directory
pwd
# Should be repo root: /Users/davidangelesalbores/repos/claude

# Archival Awareness Check
# After git safety checks, detect archival guidelines for awareness (not enforcement).
# skill-editor writes to claude-config/skills/, which is typically not covered by
# archival guidelines. This check provides awareness so the request-refiner agent
# can factor archival conventions into the specification if relevant.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
ARCHIVE_METADATA="${REPO_ROOT}/.archive-metadata.yaml"
if [ -f "$ARCHIVE_METADATA" ]; then
  echo "Archival guidelines detected (.archive-metadata.yaml present)"
  echo "These will be available to the request-refiner for specification context"
  # Reference: ~/.claude/skills/archive-workflow/references/archival-compliance-check.md
  # Step 1 (detection) applied; Steps 2-5 not enforced for skill-editor output
  ARCHIVAL_GUIDELINES_PRESENT=true
else
  ARCHIVAL_GUIDELINES_PRESENT=false
fi

# Add trap for graceful interrupt handling
trap 'echo ""; echo "Session paused. Resume with: /skill-editor"; jq ".status = \"paused\"" "${SESSION_DIR}/session-state.json" > "${SESSION_DIR}/session-state.tmp.json" && mv "${SESSION_DIR}/session-state.tmp.json" "${SESSION_DIR}/session-state.json"; exit 130' INT TERM

# Session management commands
if [ "$1" = "--list-sessions" ]; then
  echo "=== All Sessions ==="
  ls -d /tmp/skill-editor-session/session-* 2>/dev/null | while read SESSION_PATH; do
    SESSION_ID=$(basename "$SESSION_PATH")
    if [ -f "${SESSION_PATH}/session-state.json" ]; then
      PHASE=$(jq -r .phase "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
      STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
      TIMESTAMP=$(jq -r .timestamp "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
      echo "  ${SESSION_ID}"
      echo "    Status: ${STATUS} | Phase: ${PHASE} | ${TIMESTAMP}"
    fi
  done
  exit 0
fi

if [ "$1" = "--cleanup" ]; then
  echo "Scanning for completed sessions..."
  COMPLETED_SESSIONS=($(ls -d /tmp/skill-editor-session/session-* 2>/dev/null | while read SESSION_PATH; do
    STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json" 2>/dev/null)
    if [ "$STATUS" = "completed" ]; then
      echo "$SESSION_PATH"
    fi
  done))

  if [ ${#COMPLETED_SESSIONS[@]} -eq 0 ]; then
    echo "No completed sessions found"
    exit 0
  fi

  echo "Found ${#COMPLETED_SESSIONS[@]} completed session(s):"
  for SESSION_PATH in "${COMPLETED_SESSIONS[@]}"; do
    SESSION_ID=$(basename "$SESSION_PATH")
    TIMESTAMP=$(jq -r .completed_at "${SESSION_PATH}/session-state.json" 2>/dev/null || echo "unknown")
    echo "  ${SESSION_ID} - Completed: ${TIMESTAMP}"
  done

  read -p "Remove these completed sessions? (yes/no): " CONFIRM
  if [ "$CONFIRM" = "yes" ]; then
    for SESSION_PATH in "${COMPLETED_SESSIONS[@]}"; do
      rm -rf "$SESSION_PATH"
    done
    echo "✅ ${#COMPLETED_SESSIONS[@]} completed session(s) removed"
  fi
  exit 0
fi

# Resume protocol with multi-session support
SESSIONS=($(ls -d /tmp/skill-editor-session/session-* 2>/dev/null | sort -r))

if [ ${#SESSIONS[@]} -gt 0 ]; then
  echo "Found ${#SESSIONS[@]} existing session(s):"
  echo ""
  echo "Active/Paused Sessions:"
  for SESSION_PATH in "${SESSIONS[@]}"; do
    SESSION_ID=$(basename "$SESSION_PATH")
    if [ -f "${SESSION_PATH}/session-state.json" ]; then
      TIMESTAMP=$(jq -r .timestamp "${SESSION_PATH}/session-state.json")
      PHASE=$(jq -r .phase "${SESSION_PATH}/session-state.json")
      STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json")

      # Only show non-completed sessions by default
      if [ "$STATUS" != "completed" ]; then
        echo "  ${SESSION_ID}"
        echo "    Status: ${STATUS} | Phase: ${PHASE} | ${TIMESTAMP}"
      fi
    fi
  done
  echo ""
  echo "Options:"
  echo "  - Enter session ID to resume"
  echo "  - Enter 'list-all' to see completed sessions"
  echo "  - Enter 'n' to start new session"
  read -p "Choice: " RESUME_CHOICE

  if [ "$RESUME_CHOICE" = "list-all" ]; then
    echo ""
    echo "All Sessions (including completed):"
    for SESSION_PATH in "${SESSIONS[@]}"; do
      SESSION_ID=$(basename "$SESSION_PATH")
      if [ -f "${SESSION_PATH}/session-state.json" ]; then
        TIMESTAMP=$(jq -r .timestamp "${SESSION_PATH}/session-state.json")
        PHASE=$(jq -r .phase "${SESSION_PATH}/session-state.json")
        STATUS=$(jq -r .status "${SESSION_PATH}/session-state.json")
        echo "  ${SESSION_ID} - ${STATUS} - Phase ${PHASE} - ${TIMESTAMP}"
      fi
    done
    echo ""
    read -p "Resume a session? Enter session ID or 'n' for new: " RESUME_CHOICE
  fi

  if [ "$RESUME_CHOICE" != "n" ]; then
    SESSION_ID="$RESUME_CHOICE"
    SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
    echo "Resuming ${SESSION_ID}"
  else
    # Create new session
    SESSION_ID="session-$(date -u +%Y%m%d-%H%M%S)-$$"
    SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
  fi
else
  # Check for legacy session format
  LEGACY_STATE="/tmp/skill-editor-session/session-state.json"
  if [ -f "$LEGACY_STATE" ]; then
    echo "Detected legacy session format"
    LEGACY_TIMESTAMP=$(jq -r .timestamp "$LEGACY_STATE")
    LEGACY_SESSION_ID="session-legacy-$(echo $LEGACY_TIMESTAMP | tr -d ':TZ-')"

    read -p "Migrate to new format as ${LEGACY_SESSION_ID}? (y/n): " MIGRATE
    if [ "$MIGRATE" = "y" ]; then
      mkdir -p "/tmp/skill-editor-session/${LEGACY_SESSION_ID}"
      mv /tmp/skill-editor-session/*.{json,md} "/tmp/skill-editor-session/${LEGACY_SESSION_ID}/" 2>/dev/null
      SESSION_ID="$LEGACY_SESSION_ID"
      SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
      echo "Migration complete. Resuming as ${SESSION_ID}"
    else
      # Create new session
      SESSION_ID="session-$(date -u +%Y%m%d-%H%M%S)-$$"
      SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
    fi
  else
    # Create new session
    SESSION_ID="session-$(date -u +%Y%m%d-%H%M%S)-$$"
    SESSION_DIR="/tmp/skill-editor-session/${SESSION_ID}"
  fi
fi

# Create session directory and initialize state if new session
mkdir -p "${SESSION_DIR}"
echo "Session directory: ${SESSION_DIR}"
echo "Session ID: ${SESSION_ID}"

if [ ! -f "${SESSION_DIR}/session-state.json" ]; then
  # Initialize session state with lifecycle status
  jq -n \
    --arg phase "0" \
    --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --arg session_id "$SESSION_ID" \
    --arg status "in_progress" \
    '{
      phase: $phase,
      timestamp: $timestamp,
      session_id: $session_id,
      status: $status,
      agents_completed: []
    }' > "${SESSION_DIR}/session-state.json"
  echo "Starting new session"
else
  echo "Resuming from Phase $(jq -r .phase ${SESSION_DIR}/session-state.json)"
fi
