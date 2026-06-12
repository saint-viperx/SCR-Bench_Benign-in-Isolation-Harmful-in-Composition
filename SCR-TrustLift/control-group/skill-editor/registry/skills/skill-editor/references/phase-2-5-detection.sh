#!/usr/bin/env bash
# skill-editor reference: Phase 2.5 complexity detection and strategy consultant
# Extracted from SKILL.md (lines 933-1426) for readability. See SKILL.md for workflow context.
# This file contains: Phase 2.5 complexity detection, strategy consultant launch with timeout,
# strategic review quality validation, major refactoring detection, and Quality Gate 2.5.

# === Step 1: Complexity Detection for Phase 2.5 Trigger ===

# Run complexity detection function
# See /Users/davidangelesalbores/repos/claude/claude-config/skills/skill-editor/references/complexity-detection-criteria.md

SPEC_FILE="${SESSION_DIR}/refined-specification.md"
COMPLEX=false
CONFIDENCE="low"
REASON=""

# Extract metrics from spec
FILES_CHANGED=$(grep -c "File:" "$SPEC_FILE" 2>/dev/null || echo 0)
LINES_CHANGED=$(grep -oP "Lines: \K[0-9]+" "$SPEC_FILE" 2>/dev/null | awk '{sum+=$1} END {print sum}')
[ -z "$LINES_CHANGED" ] && LINES_CHANGED=0

SCOPE=$(grep -A10 "^## Scope" "$SPEC_FILE")

# High-confidence complex triggers
if grep -qi "Create new skill" "$SPEC_FILE"; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="New skill creation"
elif [ "$FILES_CHANGED" -gt 3 ]; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="Multiple files affected (>3)"
elif [ "$LINES_CHANGED" -gt 200 ]; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="Large change (>200 lines)"
elif grep -qi "strategic review\|architectural assessment" "$SPEC_FILE"; then
  COMPLEX=true
  CONFIDENCE="high"
  REASON="User explicitly requested strategic review"
fi

# High-confidence simple (override complex if both match)
if [ "$CONFIDENCE" != "high" ]; then
  if echo "$SCOPE" | grep -qi "documentation\|typo\|comment\|example"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      COMPLEX=false
      CONFIDENCE="high"
      REASON="Documentation-only change"
    fi
  fi

  if echo "$SCOPE" | grep -qi "fix bug\|fix typo\|fix error"; then
    if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
      COMPLEX=false
      CONFIDENCE="high"
      REASON="Minor bug fix"
    fi
  fi
fi

# Medium-confidence detection
if [ "$CONFIDENCE" != "high" ]; then
  if grep -qi "agent\|workflow\|phase\|quality gate\|multi-agent" "$SPEC_FILE"; then
    if [ "$FILES_CHANGED" -le 2 ] && [ "$LINES_CHANGED" -le 100 ]; then
      COMPLEX=false
      CONFIDENCE="medium"
      REASON="Keywords detected but change is small (user confirmation recommended)"
    else
      COMPLEX=true
      CONFIDENCE="medium"
      REASON="Workflow/agent keywords with moderate change size"
    fi
  fi
fi

# Default for unclear cases
if [ "$CONFIDENCE" = "low" ]; then
  if [ "$FILES_CHANGED" -ge 2 ] || [ "$LINES_CHANGED" -ge 100 ]; then
    COMPLEX=true
    CONFIDENCE="low"
    REASON="Moderate size with unclear scope (user confirmation recommended)"
  else
    COMPLEX=false
    CONFIDENCE="medium"
    REASON="Small change with unclear scope"
  fi
fi

echo "=== Phase 2.5: Complexity Detection ==="
echo "Result: $COMPLEX (confidence: $CONFIDENCE)"
echo "Reason: $REASON"
echo ""

# High-confidence decisions
PROCEED_TO_STRATEGY_CONSULTANT=false
if [ "$CONFIDENCE" = "high" ]; then
  if [ "$COMPLEX" = "true" ]; then
    echo "→ Complex change detected: Launching strategy consultant"
    PROCEED_TO_STRATEGY_CONSULTANT=true
  else
    echo "→ Simple change detected: Skipping Phase 2.5"
    echo "   Proceeding directly to Phase 3 (decision synthesis)"
    PROCEED_TO_STRATEGY_CONSULTANT=false
  fi
else
  # Medium/low confidence: User confirmation
  echo "Confidence is $CONFIDENCE. User confirmation recommended."
  echo ""
  read -p "Do you want strategic architectural review (Phase 2.5)?
  (Y) Yes - run strategic assessment (adds 10-30 min)
  (N) No - skip Phase 2.5 (proceed to synthesis)
Choice [Y/n]: " USER_CHOICE

  if [ "$USER_CHOICE" = "n" ] || [ "$USER_CHOICE" = "N" ]; then
    PROCEED_TO_STRATEGY_CONSULTANT=false
    echo "→ Skipping Phase 2.5 (user override)"
  else
    PROCEED_TO_STRATEGY_CONSULTANT=true
    echo "→ Running Phase 2.5 (user confirmed)"
  fi
fi

# Record decision
jq -n \
  --argjson complex "$COMPLEX" \
  --arg confidence "$CONFIDENCE" \
  --arg reason "$REASON" \
  --argjson proceed "$PROCEED_TO_STRATEGY_CONSULTANT" \
  '{
    complexity_detected: $complex,
    confidence: $confidence,
    reason: $reason,
    proceed_to_phase_2_5: $proceed,
    timestamp: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
  }' \
  > ${SESSION_DIR}/complexity-detection.json

# Branch logic
if [ "$PROCEED_TO_STRATEGY_CONSULTANT" = "false" ]; then
  echo ""
  echo "✓ Phase 2.5 skipped (simple change)"
  echo "→ Proceeding to Phase 3: Decision Synthesis"
  # Continue to Phase 3
fi

# If PROCEED_TO_STRATEGY_CONSULTANT is true, continue to Step 2

# === Step 2: Launch Strategy Consultant ===

if [ "$PROCEED_TO_STRATEGY_CONSULTANT" = "true" ]; then
  echo "=== Phase 2.5: Strategic Architectural Assessment ==="
  echo ""
  echo "Launching strategy-consultant agent (Opus 4.6)..."
  echo "Expected duration: 10-30 minutes"
  echo ""
  echo "This agent will:"
  echo "  - Read all Phase 2 analysis reports"
  echo "  - Perform cross-domain pattern matching"
  echo "  - Assess architectural fit"
  echo "  - Classify recommendations (minor/major)"
  echo "  - Detect major refactoring opportunities"
  echo ""

  # Launch agent with 30-minute timeout
  TIMEOUT_SECONDS=1800
  START_TIME=$(date +%s)

  timeout ${TIMEOUT_SECONDS} claude-agent skill-editor-strategy-consultant

  EXIT_CODE=$?
  END_TIME=$(date +%s)
  ELAPSED=$((END_TIME - START_TIME))

  echo ""
  echo "Strategy consultant completed in ${ELAPSED} seconds"

  # Handle timeout
  if [ $EXIT_CODE -eq 124 ]; then
    echo "⚠ WARNING: Strategy consultant timed out after 30 minutes"

    # Check for partial report
    if [ -f "${SESSION_DIR}/strategic-review.md" ]; then
      WORD_COUNT=$(wc -w < ${SESSION_DIR}/strategic-review.md)
      if [ $WORD_COUNT -gt 50 ]; then
        echo "Partial report found (${WORD_COUNT} words)"
        echo "" >> ${SESSION_DIR}/strategic-review.md
        echo "## INCOMPLETE REPORT" >> ${SESSION_DIR}/strategic-review.md
        echo "Note: Strategic review timed out. This is a partial analysis." >> ${SESSION_DIR}/strategic-review.md
      else
        rm ${SESSION_DIR}/strategic-review.md
      fi
    fi

    # User decision on timeout
    read -p "Strategy consultant timed out. Options:
  (A) Proceed without strategic review
  (B) Retry with extended timeout (60 minutes)
  (C) Abort workflow
Choice: " TIMEOUT_CHOICE

    case $TIMEOUT_CHOICE in
      A)
        echo "Proceeding without strategic review"
        rm -f ${SESSION_DIR}/strategic-review.md
        ;;
      B)
        echo "Retrying with 60-minute timeout..."
        timeout 3600 claude-agent skill-editor-strategy-consultant
        ;;
      C)
        echo "Aborting workflow"
        exit 1
        ;;
    esac
  elif [ $EXIT_CODE -ne 0 ]; then
    echo "✗ ERROR: Strategy consultant failed with exit code $EXIT_CODE"
    read -p "Proceed without strategic review? (yes/no): " PROCEED
    if [ "$PROCEED" != "yes" ]; then
      exit 1
    fi
  fi
fi

# === Step 3: Validate Strategic Review Quality ===

if [ "$PROCEED_TO_STRATEGY_CONSULTANT" = "true" ]; then
  echo "=== Validating Strategic Review Quality ==="

  REVIEW_FILE="${SESSION_DIR}/strategic-review.md"

  if [ ! -f "$REVIEW_FILE" ]; then
    echo "⚠ No strategic review produced (agent may have failed)"
    read -p "Proceed without strategic review? (yes/no): " PROCEED
    if [ "$PROCEED" != "yes" ]; then
      exit 1
    fi
    echo "→ Skipping to Phase 3"
  else
    # Quality checks
    WORD_COUNT=$(wc -w < "$REVIEW_FILE")
    PATTERN_COUNT=$(grep -c "Pattern:" "$REVIEW_FILE" || echo 0)
    RECOMMENDATION_COUNT=$(grep -c "Recommendation:" "$REVIEW_FILE" || grep -c "^- " "$REVIEW_FILE" || echo 0)

    echo "Quality metrics:"
    echo "  - Word count: $WORD_COUNT"
    echo "  - Patterns identified: $PATTERN_COUNT"
    echo "  - Recommendations: $RECOMMENDATION_COUNT"

    # Minimum thresholds
    MIN_WORDS=200
    MIN_PATTERNS=1
    MIN_RECOMMENDATIONS=1

    QUALITY_SUFFICIENT=true

    if [ "$WORD_COUNT" -lt "$MIN_WORDS" ]; then
      echo "⚠ WARNING: Strategic review is brief ($WORD_COUNT words < $MIN_WORDS minimum)"
      QUALITY_SUFFICIENT=false
    fi

    if [ "$PATTERN_COUNT" -lt "$MIN_PATTERNS" ]; then
      echo "⚠ WARNING: No patterns identified"
      QUALITY_SUFFICIENT=false
    fi

    if [ "$RECOMMENDATION_COUNT" -lt "$MIN_RECOMMENDATIONS" ]; then
      echo "⚠ WARNING: No recommendations provided"
      QUALITY_SUFFICIENT=false
    fi

    # Check for generic content
    if grep -qi "looks reasonable\|looks good\|no concerns\|follow best practices\|seems fine" "$REVIEW_FILE" | head -2 | wc -l | grep -q "2"; then
      echo "⚠ WARNING: Strategic review contains generic/superficial content"
      QUALITY_SUFFICIENT=false
    fi

    if [ "$QUALITY_SUFFICIENT" = "false" ]; then
      echo ""
      echo "Strategic review quality is below threshold."
      echo "Preview (first 500 words):"
      head -c 3000 "$REVIEW_FILE"
      echo ""
      echo "..."
      echo ""
      read -p "Options:
  (A) Accept strategic review as-is
  (B) Retry strategy consultant (extended time budget)
  (C) Skip strategic review and proceed without it
Choice: " QUALITY_CHOICE

      case $QUALITY_CHOICE in
        A)
          echo "Accepting strategic review"
          ;;
        B)
          echo "Retrying strategy consultant..."
          mv "$REVIEW_FILE" "${REVIEW_FILE}.first-attempt"
          timeout 3600 claude-agent skill-editor-strategy-consultant --mode=detailed
          ;;
        C)
          echo "Skipping strategic review"
          rm "$REVIEW_FILE"
          ;;
      esac
    fi

    echo "✓ Strategic review validated"
  fi
fi

# === Step 4: Check for Major Refactoring ===

echo "=== Checking for Major Refactoring Opportunity ==="

REVIEW_FILE="${SESSION_DIR}/strategic-review.md"

if [ ! -f "$REVIEW_FILE" ]; then
  echo "No strategic review file (Phase 2.5 was skipped or failed)"
  echo "→ Proceeding to Phase 3"
else
  # Check classification
  if grep -qi "Classification:.*MAJOR REFACTORING DETECTED" "$REVIEW_FILE"; then
    echo "🔴 MAJOR REFACTORING OPPORTUNITY DETECTED"
    echo ""
    echo "The strategy consultant has identified a fundamental architectural issue."
    echo ""

    # Extract details from report
    ISSUE=$(grep -A5 "Major Refactoring Opportunity" "$REVIEW_FILE" | head -6)
    echo "$ISSUE"
    echo ""

    # Note: Major refactoring decision is handled by strategy-consultant agent
    # via AskUserQuestion. User decision is recorded in strategic-review.md.

    # Check user decision from report
    if grep -qi "User decision:.*Explore refactoring in parallel" "$REVIEW_FILE"; then
      echo "User selected: Explore refactoring in parallel (Option B)"
      echo ""
      echo "⚠ Parallel exploration will be triggered after Phase 3 completes"
      echo "  - Track 1 (current plan) continues through Phase 3"
      echo "  - Track 2 (alternative exploration) launches in parallel"
      echo "  - You'll see both approaches before Phase 4 execution"
      echo ""

      # Set flag for parallel exploration
      jq -n '{
        parallel_exploration: true,
        trigger_after_phase: 3
      }' > ${SESSION_DIR}/parallel-exploration-flag.json

    elif grep -qi "User decision:.*Proceed with current plan" "$REVIEW_FILE"; then
      echo "User selected: Proceed with current plan (Option A)"
      echo "→ Continuing with original specification approach"

    elif grep -qi "User decision:.*Abort" "$REVIEW_FILE"; then
      echo "User selected: Abort workflow (Option C)"
      echo "Stopping workflow. Session data preserved in ${SESSION_DIR}"
      exit 1
    fi
  else
    echo "✓ No major refactoring detected (minor recommendations only)"
  fi

  echo ""
  echo "→ Proceeding to Quality Gate 2.5"
fi

# === Quality Gate 2.5: Strategic Review Complete ===

echo "=== Quality Gate 2.5: Strategic Review Complete ==="
echo ""

GATE_PASS=true

# Check 1: Complexity detection completed
if [ ! -f "${SESSION_DIR}/complexity-detection.json" ]; then
  echo "✗ Complexity detection not completed"
  GATE_PASS=false
else
  echo "✓ Complexity detection completed"
fi

# Check 2: If complex, strategic review exists
PROCEED=$(jq -r '.proceed_to_phase_2_5' ${SESSION_DIR}/complexity-detection.json 2>/dev/null || echo "false")

if [ "$PROCEED" = "true" ]; then
  if [ -f "${SESSION_DIR}/strategic-review.md" ]; then
    WORD_COUNT=$(wc -w < ${SESSION_DIR}/strategic-review.md)
    if [ $WORD_COUNT -gt 100 ]; then
      echo "✓ Strategic review exists and is substantive ($WORD_COUNT words)"
    else
      echo "⚠ Strategic review exists but is too brief ($WORD_COUNT words)"
      read -p "Accept brief review and proceed? (yes/no): " ACCEPT
      if [ "$ACCEPT" != "yes" ]; then
        GATE_PASS=false
      fi
    fi
  else
    echo "⚠ Strategic review missing (expected for complex change)"
    read -p "Proceed without strategic review? (yes/no): " PROCEED_ANYWAY
    if [ "$PROCEED_ANYWAY" != "yes" ]; then
      GATE_PASS=false
    fi
  fi
else
  echo "✓ Phase 2.5 skipped (simple change)"
fi

# Check 3: If major refactoring, user decision recorded
if [ -f "${SESSION_DIR}/strategic-review.md" ]; then
  if grep -qi "MAJOR REFACTORING DETECTED" ${SESSION_DIR}/strategic-review.md; then
    if grep -qi "User decision:" ${SESSION_DIR}/strategic-review.md; then
      DECISION=$(grep -i "User decision:" ${SESSION_DIR}/strategic-review.md | head -1 | cut -d: -f2 | xargs)
      echo "✓ Major refactoring decision recorded: $DECISION"
    else
      echo "✗ Major refactoring detected but no user decision recorded"
      GATE_PASS=false
    fi
  fi
fi

# Check 4: Git repository still clean (re-check)
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠ WARNING: Git working directory is no longer clean"
  git status --short
  echo ""
  read -p "Files were modified during Phase 2.5. Options:
  (A) Stash changes and continue
  (B) Abort workflow
  (C) Ignore and continue (DANGEROUS)
Choice: " GIT_CHOICE

  case $GIT_CHOICE in
    A)
      git stash push -m "skill-editor-auto-stash-$(date +%Y%m%d-%H%M%S)"
      echo "✓ Changes stashed"
      ;;
    B)
      echo "Aborting workflow"
      exit 1
      ;;
    C)
      echo "⚠ Continuing with dirty git state"
      ;;
  esac
else
  echo "✓ Git working directory clean"
fi

# Gate decision
echo ""
if [ "$GATE_PASS" = "true" ]; then
  echo "✅ Quality Gate 2.5: PASS"
  echo "→ Proceeding to Phase 3: Decision Synthesis"
else
  echo "❌ Quality Gate 2.5: FAIL"
  echo "Resolve issues above before proceeding"
  exit 1
fi

# Update session state
jq -n \
  --arg phase "3" \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson agents_completed '["request-refiner", "best-practices-reviewer", "external-researcher", "edge-case-simulator", "knowledge-engineer", "strategy-consultant"]' \
  '{
    phase: $phase,
    timestamp: $timestamp,
    agents_completed: $agents_completed
  }' \
  > ${SESSION_DIR}/session-state.json

echo ""
echo "✓ Session state updated: Phase 2.5 complete"
