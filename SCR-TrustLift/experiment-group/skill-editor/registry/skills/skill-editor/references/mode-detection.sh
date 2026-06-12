#!/usr/bin/env bash
# skill-editor reference: three-tier mode detection and selection
# Extracted from SKILL.md (lines 477-763) for readability. See SKILL.md for workflow context.
# This file contains: complexity detection (COMPLEX/SIMPLE/STANDARD/EXPERIMENTAL),
# mode selection prompt, user override confirmation, experimental warning, mode recording,
# and mode-based branching.

# === Step 1: Three-Tier Complexity Detection ===

echo "=== Mode Selection ==="
echo ""

SPEC_FILE="${SESSION_DIR}/refined-specification.md"

# Source detection function (see references/complexity-detection-criteria.md)
# Inline detection for robustness

# Extract metrics (POSIX-compatible - no grep -oP)
FILES_CHANGED=$(grep -c "File:" "$SPEC_FILE" 2>/dev/null || echo 0)
# [FIX: Adversarial Issue #4] Use POSIX-compatible grep instead of grep -oP
LINES_CHANGED=$(grep -o 'Lines: [0-9]*' "$SPEC_FILE" 2>/dev/null | grep -o '[0-9]*' | awk '{sum+=$1} END {print sum+0}')
[ -z "$LINES_CHANGED" ] && LINES_CHANGED=0
SCOPE=$(grep -A10 "^## Scope" "$SPEC_FILE")

# Initialize
DETECTED_TIER="STANDARD"
CONFIDENCE="low"
REASON=""

# === FAIL-SAFE DEFAULT ===
if [ ! -f "$SPEC_FILE" ] || [ ! -s "$SPEC_FILE" ]; then
  echo "WARNING: Mode detection encountered an error (spec file issue)."
  echo "Defaulting to STANDARD mode for safety."
  DETECTED_TIER="STANDARD"
  CONFIDENCE="error"
  REASON="Spec file unreadable, defaulting to STANDARD (safest option)"
fi

# === COMPLEX DETECTION (Phase 2.5 triggers) ===
if grep -qi "Create new skill" "$SPEC_FILE" 2>/dev/null; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="New skill creation"
elif [ "$FILES_CHANGED" -gt 4 ]; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="Multiple files affected (>4)"
elif [ "$LINES_CHANGED" -gt 300 ]; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="Large change (>300 lines)"
elif grep -qi "strategic review\|architectural assessment" "$SPEC_FILE" 2>/dev/null; then
  DETECTED_TIER="COMPLEX"
  CONFIDENCE="high"
  REASON="User explicitly requested strategic review"
elif grep -qi "refactor\|reorganize\|restructure\|migrate" "$SPEC_FILE" 2>/dev/null; then
  if [ "$FILES_CHANGED" -gt 2 ] || [ "$LINES_CHANGED" -gt 150 ]; then
    DETECTED_TIER="COMPLEX"
    CONFIDENCE="high"
    REASON="Refactoring with moderate+ scope"
  fi
fi

# === SIMPLE DETECTION ===
if [ "$CONFIDENCE" != "high" ]; then
  if echo "$SCOPE" | grep -qi "documentation\|typo\|comment\|example"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      DETECTED_TIER="SIMPLE"
      CONFIDENCE="high"
      REASON="Documentation-only change"
    fi
  fi
  if echo "$SCOPE" | grep -qi "fix bug\|fix typo\|fix error"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      DETECTED_TIER="SIMPLE"
      CONFIDENCE="high"
      REASON="Minor bug fix"
    fi
  fi
fi

# === STANDARD DETECTION (default) ===
if [ "$CONFIDENCE" != "high" ]; then
  if grep -qi "agent\|workflow\|phase\|quality gate" "$SPEC_FILE" 2>/dev/null; then
    if [ "$FILES_CHANGED" -le 2 ] && [ "$LINES_CHANGED" -le 100 ]; then
      DETECTED_TIER="STANDARD"
      CONFIDENCE="medium"
      REASON="Keywords detected but change is small"
    else
      DETECTED_TIER="STANDARD"
      CONFIDENCE="medium"
      REASON="Workflow keywords with moderate change size"
    fi
  fi
fi

# === WARNING ZONE (soft thresholds) ===
if [ "$FILES_CHANGED" -ge 3 ] && [ "$FILES_CHANGED" -le 4 ]; then
  if [ "$DETECTED_TIER" = "STANDARD" ]; then
    CONFIDENCE="medium"
    REASON="$REASON (near Phase 2.5 file threshold: $FILES_CHANGED files)"
  fi
fi
if [ "$LINES_CHANGED" -ge 200 ] && [ "$LINES_CHANGED" -le 300 ]; then
  if [ "$DETECTED_TIER" = "STANDARD" ]; then
    CONFIDENCE="medium"
    REASON="$REASON (near Phase 2.5 line threshold: $LINES_CHANGED lines)"
  fi
fi

# === EXPERIMENTAL OVERRIDE (user keywords) ===
if grep -qi "experimental\|quick\|try\|test this\|prototype" "$SPEC_FILE" 2>/dev/null; then
  DETECTED_TIER="EXPERIMENTAL"
  CONFIDENCE="high"
  REASON="User requested experimental/quick mode"
fi

# === DEFAULT for unclear ===
if [ "$CONFIDENCE" = "low" ]; then
  if [ "$FILES_CHANGED" -ge 2 ] || [ "$LINES_CHANGED" -ge 100 ]; then
    DETECTED_TIER="STANDARD"
    CONFIDENCE="low"
    REASON="Moderate size with unclear scope"
  else
    DETECTED_TIER="SIMPLE"
    CONFIDENCE="medium"
    REASON="Small change with unclear scope"
  fi
fi

echo "Detected tier: $DETECTED_TIER (confidence: $CONFIDENCE)"
echo "Reason: $REASON"
echo ""

# === Step 2: Display Mode Selection Prompt ===

cat << EOF
================================================================================
SPECIFICATION APPROVED - SELECT WORKFLOW MODE
================================================================================

Detected complexity: $DETECTED_TIER (confidence: $CONFIDENCE)
Reason: $REASON

Select workflow mode:

  [A] SIMPLE MODE          ~30 min    Skip analysis, direct implementation
      Best for: typos, documentation, single-file fixes
      Quality: Basic validation only (Gates 4, 5 always run)
      Skips: Phase 2 (4 agents), Phase 2.5 (strategic review)

  [B] STANDARD MODE        ~2-3 hrs   Full analysis and expert review
      Best for: workflow changes, features, refactoring
      Quality: 4-agent analysis + adversarial review
      Runs: All phases (current default behavior)

  [C] EXPERIMENTAL MODE    ~15 min    Minimal process, quick iteration
      Best for: prototypes, testing ideas, will iterate
      Quality: REDUCED - plan to iterate
      WARNING: Creates experimental-tagged output
      Skips: Phase 2, Phase 2.5, full adversarial review

Recommended: [$DETECTED_TIER]

Enter choice [A/B/C] (default based on detection, 60s timeout):
EOF

read -t 60 USER_CHOICE

# Handle timeout
if [ $? -ne 0 ]; then
  echo ""
  echo "No selection made. Using recommended mode: $DETECTED_TIER"
  case "$DETECTED_TIER" in
    SIMPLE) USER_CHOICE="A" ;;
    STANDARD) USER_CHOICE="B" ;;
    COMPLEX) USER_CHOICE="B" ;;  # COMPLEX uses STANDARD mode
    EXPERIMENTAL) USER_CHOICE="C" ;;
    *) USER_CHOICE="B" ;;
  esac
fi

# Normalize input
USER_CHOICE=$(echo "$USER_CHOICE" | tr '[:lower:]' '[:upper:]')

# Map selection to mode
case "$USER_CHOICE" in
  A) SELECTED_MODE="SIMPLE" ;;
  B) SELECTED_MODE="STANDARD" ;;
  C) SELECTED_MODE="EXPERIMENTAL" ;;
  *) SELECTED_MODE="STANDARD" ;;  # Default
esac

# === Step 3: User Override Confirmation ===

# Check for risky overrides
USER_OVERRIDE=false
if [ "$SELECTED_MODE" != "$DETECTED_TIER" ]; then
  USER_OVERRIDE=true

  # Additional confirmation for risky overrides
  if [ "$DETECTED_TIER" = "STANDARD" ] || [ "$DETECTED_TIER" = "COMPLEX" ]; then
    if [ "$SELECTED_MODE" = "SIMPLE" ] || [ "$SELECTED_MODE" = "EXPERIMENTAL" ]; then
      echo ""
      echo "WARNING: You selected $SELECTED_MODE but detection recommended $DETECTED_TIER."
      echo "This change may be more complex than $SELECTED_MODE mode handles."
      read -p "Confirm override? (yes/no): " CONFIRM
      if [ "$CONFIRM" != "yes" ]; then
        SELECTED_MODE="STANDARD"
        USER_OVERRIDE=false
        echo "Using recommended mode: $SELECTED_MODE"
      fi
    fi
  fi
fi

# Experimental mode warning
if [ "$SELECTED_MODE" = "EXPERIMENTAL" ]; then
  echo ""
  echo "=========================================="
  echo "  EXPERIMENTAL MODE SELECTED"
  echo "=========================================="
  echo ""
  echo "  WARNING: Reduced quality assurance"
  echo "  - No Phase 2 analysis agents"
  echo "  - Minimal decision synthesis"
  echo "  - Output will be tagged as experimental"
  echo "  - NOT production-ready without further review"
  echo ""
  read -p "Acknowledge and proceed? (yes/no): " ACK
  if [ "$ACK" != "yes" ]; then
    echo "Returning to mode selection..."
    # Re-run mode selection
  fi
fi

# === Step 4: Record Mode Selection ===

# Record mode selection in session state
jq -n \
  --arg workflow_mode "$SELECTED_MODE" \
  --arg detected_tier "$DETECTED_TIER" \
  --arg confidence "$CONFIDENCE" \
  --arg reason "$REASON" \
  --argjson user_override "$USER_OVERRIDE" \
  '{
    workflow_mode: $workflow_mode,
    detected_tier: $detected_tier,
    confidence: $confidence,
    reason: $reason,
    user_override: $user_override,
    timestamp: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
  }' \
  > ${SESSION_DIR}/mode-selection.json

# Update main session state
jq --arg mode "$SELECTED_MODE" \
   '. + {workflow_mode: $mode}' \
   ${SESSION_DIR}/session-state.json > ${SESSION_DIR}/session-state.tmp.json && \
   mv ${SESSION_DIR}/session-state.tmp.json ${SESSION_DIR}/session-state.json

echo ""
echo "[$SELECTED_MODE MODE] Mode selected. Proceeding..."
echo ""

# === Step 5: Mode-Based Branching ===

case "$SELECTED_MODE" in
  SIMPLE)
    echo "[$SIMPLE MODE] Skipping Phase 2 (no analysis agents)"
    echo "[$SIMPLE MODE] Skipping Phase 2.5 (no strategic review)"
    echo "[$SIMPLE MODE] Proceeding to Phase 3 (lightweight synthesis)"
    # Skip to Phase 3 Lightweight section
    ;;
  STANDARD)
    echo "[STANDARD MODE] Running full workflow"
    echo "[STANDARD MODE] Proceeding to Phase 2 (4 parallel agents)"
    # Continue to Phase 2 (existing behavior)
    ;;
  EXPERIMENTAL)
    echo "[EXPERIMENTAL MODE] Minimal workflow with experimental tagging"
    echo "[EXPERIMENTAL MODE] Skipping Phase 2 (no analysis agents)"
    echo "[EXPERIMENTAL MODE] Skipping Phase 2.5 (no strategic review)"
    echo "[EXPERIMENTAL MODE] Proceeding to Phase 3 (minimal synthesis)"
    # Skip to Phase 3 Minimal section
    ;;
esac
