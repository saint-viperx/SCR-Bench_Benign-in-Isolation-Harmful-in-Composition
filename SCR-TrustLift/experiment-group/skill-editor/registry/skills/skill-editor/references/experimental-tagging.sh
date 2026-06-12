#!/usr/bin/env bash
# skill-editor reference: experimental mode output tagging
# Extracted from SKILL.md (lines 1764-1798) for readability. See SKILL.md for workflow context.
# This file contains: experimental flag injection into YAML frontmatter and warning comment insertion.

CURRENT_MODE=$(jq -r '.workflow_mode' ${SESSION_DIR}/session-state.json 2>/dev/null || echo "STANDARD")

if [ "$CURRENT_MODE" = "EXPERIMENTAL" ]; then
  echo "[EXPERIMENTAL] Adding experimental tags to output files..."

  # For each skill file being created/modified
  # [FIX: Adversarial Issue #4] Use POSIX-compatible grep instead of grep -oP
  for SKILL_FILE in $(grep -o 'skills/[^/]*/SKILL\.md' ${SESSION_DIR}/implementation-plan.md | sort -u); do
    FULL_PATH="/Users/davidangelesalbores/repos/claude/claude-config/$SKILL_FILE"

    if [ -f "$FULL_PATH" ]; then
      # Check if experimental tag already exists in frontmatter
      if ! head -20 "$FULL_PATH" | grep -q "experimental: true"; then
        # [FIX: Adversarial Issue #1] BSD-compatible: Use temp file approach instead of sed -i with append
        # Insert experimental: true after first line (which is ---)
        { head -1 "$FULL_PATH"; echo "experimental: true"; tail -n +2 "$FULL_PATH"; } > "$FULL_PATH.tmp" && mv "$FULL_PATH.tmp" "$FULL_PATH"
        echo "  Added experimental tag to: $SKILL_FILE"
      fi

      # Add warning comment after frontmatter if not present
      if ! grep -q "EXPERIMENTAL SKILL" "$FULL_PATH"; then
        # First check if file has valid frontmatter (starts with ---)
        if head -1 "$FULL_PATH" | grep -q "^---"; then
          # Find end of frontmatter (second ---) and add comment using awk
          awk '/^---$/{c++} c==2{print; print ""; print "<!-- EXPERIMENTAL SKILL: Created via skill-editor experimental mode -->"; print "<!-- This skill has NOT been fully analyzed. Run Standard Mode before production use. -->"; c++; next}1' "$FULL_PATH" > "$FULL_PATH.tmp" && mv "$FULL_PATH.tmp" "$FULL_PATH"
          echo "  Added experimental warning to: $SKILL_FILE"
        else
          echo "  WARNING: No frontmatter found in $SKILL_FILE, skipping warning insertion"
        fi
      fi
    fi
  done
fi
