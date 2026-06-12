# Complexity Detection Criteria

## Purpose

Determine workflow mode (Simple, Standard, Complex/Experimental) based on change characteristics.

**Primary goal**: Route changes to appropriate execution mode:
- SIMPLE: Fast path for typos, docs, single-file fixes (~30 min)
- STANDARD: Full workflow for features, workflow changes (~2-3 hours)
- COMPLEX: Standard + Phase 2.5 strategic review for architectural changes
- EXPERIMENTAL: User-requested fast iteration mode (bypass analysis)

**Target metrics**:
- False positive rate: <5% (simple changes incorrectly flagged as complex)
- False negative rate: <5% (complex changes incorrectly flagged as simple)
- User override rate: <20% (indicates good auto-detection)

---

## Detection Criteria

### High-Confidence Complex (Always Triggers Phase 2.5)

1. **New skill creation**
   - Specification contains: "Create new skill"
   - Rationale: New skills are architectural additions requiring strategic assessment

2. **Many files affected** (>4 files)
   - File count exceeds 4
   - Rationale: Multi-file changes likely have architectural implications

3. **Large change** (>300 lines)
   - Total lines changed exceeds 300
   - Rationale: Large changes carry higher risk of architectural issues

4. **Explicit user request**
   - Specification contains: "strategic review" or "architectural assessment"
   - Rationale: User explicitly wants strategic perspective

5. **Major refactoring keywords** [NEW]
   - Specification contains: "refactor", "reorganize", "restructure", "migrate"
   - AND: >2 files OR >150 lines
   - Rationale: Refactoring changes often have architectural implications

---

### High-Confidence Simple (Always Skips Phase 2.5)

1. **Documentation-only changes**
   - Scope mentions: "documentation" or "typo" or "comment" or "example"
   - AND: Single file, ≤50 lines
   - Rationale: Documentation has no architectural implications

2. **Minor bug fix**
   - Scope mentions: "fix bug" or "fix typo" or "fix error"
   - AND: Single file, ≤50 lines
   - Rationale: Small fixes don't require strategic assessment

---

### Warning Zone (Soft Thresholds)

Changes in the "warning zone" prompt user for Phase 2.5 decision:

1. **Near file threshold**: 3-4 files affected
   - Prompt: "Near Phase 2.5 threshold. Include strategic review?"
   - Default: No (skip Phase 2.5)

2. **Near line threshold**: 200-300 lines changed
   - Prompt: "Near Phase 2.5 threshold. Include strategic review?"
   - Default: No (skip Phase 2.5)

3. **Refactoring keywords with moderate scope** [NEW]
   - Contains: "refactor", "reorganize", "restructure"
   - AND: 2-4 files, 100-300 lines
   - Prompt: "Refactoring detected. Strategic review recommended."
   - Default: Yes (run Phase 2.5)

---

### Medium-Confidence (User Confirmation Required)

1. **Keywords detected but small change**
   - Contains: "agent" or "workflow" or "phase" or "quality gate"
   - BUT: ≤2 files AND ≤100 lines
   - Action: Prompt user with reasoning, default to skip

2. **Moderate size with unclear scope**
   - 2-3 files OR 100-200 lines
   - No clear documentation/bug-fix/architectural indicators
   - Action: Prompt user with reasoning, default to complex

---

## Detection Function

```bash
# Three-tier detection function (POSIX-compatible)
detect_tier() {
  local SPEC_FILE="/tmp/skill-editor-session/refined-specification.md"
  local TIER="STANDARD"
  local CONFIDENCE="low"
  local REASON=""

  # Fail-safe: Check spec file exists
  if [ ! -f "$SPEC_FILE" ] || [ ! -s "$SPEC_FILE" ]; then
    echo "STANDARD|error|Spec file unreadable, defaulting to STANDARD"
    return
  fi

  # Extract metrics (POSIX-compatible - no grep -oP)
  FILES_CHANGED=$(grep -c "File:" "$SPEC_FILE" 2>/dev/null || echo 0)
  # Use grep -o with POSIX patterns instead of grep -oP
  LINES_CHANGED=$(grep -o 'Lines: [0-9]*' "$SPEC_FILE" 2>/dev/null | grep -o '[0-9]*' | awk '{sum+=$1} END {print sum+0}')
  [ -z "$LINES_CHANGED" ] && LINES_CHANGED=0

  SCOPE=$(grep -A10 "^## Scope" "$SPEC_FILE")

  # === COMPLEX DETECTION (Phase 2.5 triggers) ===
  if grep -qi "Create new skill" "$SPEC_FILE" 2>/dev/null; then
    TIER="COMPLEX"
    CONFIDENCE="high"
    REASON="New skill creation"
  elif [ "$FILES_CHANGED" -gt 4 ]; then
    TIER="COMPLEX"
    CONFIDENCE="high"
    REASON="Multiple files affected (>4)"
  elif [ "$LINES_CHANGED" -gt 300 ]; then
    TIER="COMPLEX"
    CONFIDENCE="high"
    REASON="Large change (>300 lines)"
  elif grep -qi "strategic review\|architectural assessment" "$SPEC_FILE" 2>/dev/null; then
    TIER="COMPLEX"
    CONFIDENCE="high"
    REASON="User explicitly requested strategic review"
  elif grep -qi "refactor\|reorganize\|restructure\|migrate" "$SPEC_FILE" 2>/dev/null; then
    if [ "$FILES_CHANGED" -gt 2 ] || [ "$LINES_CHANGED" -gt 150 ]; then
      TIER="COMPLEX"
      CONFIDENCE="high"
      REASON="Refactoring with moderate+ scope"
    fi
  fi

  # === SIMPLE DETECTION ===
  if [ "$CONFIDENCE" != "high" ]; then
    if echo "$SCOPE" | grep -qi "documentation\|typo\|comment\|example"; then
      if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
        TIER="SIMPLE"
        CONFIDENCE="high"
        REASON="Documentation-only change"
      fi
    fi
    if echo "$SCOPE" | grep -qi "fix bug\|fix typo\|fix error"; then
      if [ "$FILES_CHANGED" -le 1 ] && [ "$LINES_CHANGED" -le 50 ]; then
        TIER="SIMPLE"
        CONFIDENCE="high"
        REASON="Minor bug fix"
      fi
    fi
  fi

  # === STANDARD DETECTION (default) ===
  if [ "$CONFIDENCE" != "high" ]; then
    if grep -qi "agent\|workflow\|phase\|quality gate" "$SPEC_FILE" 2>/dev/null; then
      if [ "$FILES_CHANGED" -le 2 ] && [ "$LINES_CHANGED" -le 100 ]; then
        TIER="STANDARD"
        CONFIDENCE="medium"
        REASON="Keywords detected but change is small"
      else
        TIER="STANDARD"
        CONFIDENCE="medium"
        REASON="Workflow keywords with moderate change size"
      fi
    fi
  fi

  # === WARNING ZONE (soft thresholds) ===
  if [ "$FILES_CHANGED" -ge 3 ] && [ "$FILES_CHANGED" -le 4 ]; then
    if [ "$TIER" = "STANDARD" ]; then
      CONFIDENCE="medium"
      REASON="$REASON (near Phase 2.5 file threshold: $FILES_CHANGED files)"
    fi
  fi
  if [ "$LINES_CHANGED" -ge 200 ] && [ "$LINES_CHANGED" -le 300 ]; then
    if [ "$TIER" = "STANDARD" ]; then
      CONFIDENCE="medium"
      REASON="$REASON (near Phase 2.5 line threshold: $LINES_CHANGED lines)"
    fi
  fi

  # === EXPERIMENTAL OVERRIDE (user keywords) ===
  if grep -qi "experimental\|quick\|try\|test this\|prototype" "$SPEC_FILE" 2>/dev/null; then
    TIER="EXPERIMENTAL"
    CONFIDENCE="high"
    REASON="User requested experimental/quick mode"
  fi

  # === DEFAULT for unclear ===
  if [ "$CONFIDENCE" = "low" ]; then
    if [ "$FILES_CHANGED" -ge 2 ] || [ "$LINES_CHANGED" -ge 100 ]; then
      TIER="STANDARD"
      CONFIDENCE="low"
      REASON="Moderate size with unclear scope"
    else
      TIER="SIMPLE"
      CONFIDENCE="medium"
      REASON="Small change with unclear scope"
    fi
  fi

  echo "$TIER|$CONFIDENCE|$REASON"
}
```

---

## User Confirmation Logic

```bash
DETECTION_RESULT=$(detect_complexity)
IS_COMPLEX=$(echo "$DETECTION_RESULT" | cut -d'|' -f1)
CONFIDENCE=$(echo "$DETECTION_RESULT" | cut -d'|' -f2)
REASON=$(echo "$DETECTION_RESULT" | cut -d'|' -f3)

echo "Complexity detection: $IS_COMPLEX (confidence: $CONFIDENCE)"
echo "Reason: $REASON"
echo ""

# High-confidence: proceed automatically
if [ "$CONFIDENCE" = "high" ]; then
  if [ "$IS_COMPLEX" = "true" ]; then
    echo "→ Complex change detected: Launching Phase 2.5 (strategy consultant)"
  else
    echo "→ Simple change detected: Skipping Phase 2.5 (proceeding directly to Phase 3)"
  fi
else
  # Medium/low confidence: ask user
  echo "Heuristic confidence is $CONFIDENCE. User confirmation recommended."
  echo ""
  read -p "Do you want strategic review (Phase 2.5)?
  (Y) Yes - run Phase 2.5 (adds 10-30 min, strategic architectural assessment)
  (N) No - skip Phase 2.5 (faster, proceed directly to synthesis)
Choice [Y/n]: " USER_OVERRIDE

  if [ "$USER_OVERRIDE" = "n" ] || [ "$USER_OVERRIDE" = "N" ]; then
    IS_COMPLEX=false
    echo "→ User override: Skipping Phase 2.5"
  else
    IS_COMPLEX=true
    echo "→ User confirmed: Running Phase 2.5"
  fi
fi

# Record decision in session state
jq -n \
  --argjson complex "$IS_COMPLEX" \
  --arg confidence "$CONFIDENCE" \
  --arg reason "$REASON" \
  '{
    complexity_detected: $complex,
    confidence: $confidence,
    reason: $reason,
    timestamp: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
  }' \
  > /tmp/skill-editor-session/complexity-detection.json
```

---

## Test Cases

### Test Case 1: Simple Change (Should Skip)

**Specification**:
```markdown
## Objective
Fix typo in skill-editor SKILL.md documentation

## Scope
- Edit 1 file: claude-config/skills/skill-editor/SKILL.md
- Lines changed: 1 line
- Change: "strategig" → "strategic"
```

**Expected Result**:
- IS_COMPLEX=false
- CONFIDENCE=high
- REASON="Documentation-only change"
- Phase 2.5: SKIP

---

### Test Case 2: New Skill Creation (Should Trigger)

**Specification**:
```markdown
## Objective
Create new skill for code review automation

## Scope
- Create new skill: claude-config/skills/code-reviewer/SKILL.md
- Create agent: claude-config/agents/code-reviewer.md
- Create references: claude-config/skills/code-reviewer/references/
```

**Expected Result**:
- IS_COMPLEX=true
- CONFIDENCE=high
- REASON="New skill creation"
- Phase 2.5: TRIGGER

---

### Test Case 3: Major Refactoring (Should Trigger)

**Specification**:
```markdown
## Objective
Refactor skill-editor to use hierarchical agent coordination

## Scope
- Modify 4 files: SKILL.md, 3 agent files
- Lines changed: ~250 lines
- Add new workflow phases
```

**Expected Result**:
- IS_COMPLEX=true
- CONFIDENCE=high
- REASON="Multiple files affected (>3)" OR "Large change (>200 lines)"
- Phase 2.5: TRIGGER

---

### Test Case 4: Borderline (User Confirmation)

**Specification**:
```markdown
## Objective
Update skill-editor agent coordination pattern

## Scope
- Modify 2 files: SKILL.md, decision-synthesizer.md
- Lines changed: ~80 lines
- Change workflow description
```

**Expected Result**:
- IS_COMPLEX=false
- CONFIDENCE=medium
- REASON="Keywords detected but change is small (user confirmation recommended)"
- Action: PROMPT USER

---

### Test Case 5: Documentation Update (Should Skip)

**Specification**:
```markdown
## Objective
Update skill-editor README with usage examples

## Scope
- Modify 1 file: README.md
- Lines changed: 30 lines
- Add 2 examples
```

**Expected Result**:
- IS_COMPLEX=false
- CONFIDENCE=high
- REASON="Documentation-only change"
- Phase 2.5: SKIP

---

### Test Case 6: Experimental Override

**Specification**: Contains "try this quick approach", 5 files, 400 lines
**Expected**: TIER=EXPERIMENTAL, CONFIDENCE=high
**Reason**: User requested experimental/quick mode

---

### Test Case 7: User Override

**Specification**: 2 files, 80 lines, workflow keywords
**Auto-detection**: STANDARD
**User selection**: SIMPLE
**Expected**: Confirmation prompt, proceed if user confirms

---

### Test Case 8: Warning Zone

**Specification**: 4 files, 250 lines, "refactor" keyword
**Expected**: TIER=STANDARD, CONFIDENCE=medium, warning zone prompt

---

### Test Case 9: Detection Failure

**Specification**: Empty or malformed file
**Expected**: TIER=STANDARD, CONFIDENCE=error (fail-safe default)

---

### Test Case 10: Refactoring Keywords

**Specification**: "Refactor agent coordination", 3 files, 180 lines
**Expected**: TIER=COMPLEX, CONFIDENCE=high (refactoring with scope)

---

## Monitoring and Refinement

**Track metrics over time**:
- False positive rate: (Simple changes that triggered Phase 2.5) / (Total simple changes)
- False negative rate: (Complex changes that skipped Phase 2.5) / (Total complex changes)
- User override rate: (User overrides) / (Total borderline cases)

**Refinement process**:
1. After first 10 uses of Phase 2.5, review false positive/negative incidents
2. Adjust thresholds if false positive rate >10% or false negative rate >5%
3. Consider adding new high-confidence indicators based on patterns
4. Document adjustments in this file

**Target thresholds for adjustment**:
- If false positive >10%: Increase file count threshold (3 → 4) or line threshold (200 → 300)
- If false negative >5%: Decrease thresholds or add new keyword indicators
