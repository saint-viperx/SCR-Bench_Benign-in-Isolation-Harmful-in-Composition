# Quality Gates for Skill Editing

This document defines the 5 quality gates used in the skill-editor workflow to ensure high-quality skill modifications.

## Quality Gate Overview

```
┌────────────────────────────────────────────────────────┐
│  PHASE 1: REFINEMENT                                   │
│  └─→ Quality Gate 1: Specification Approval           │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│  PHASE 2: PARALLEL ANALYSIS                            │
│  └─→ Quality Gate 2: Analysis Completion              │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│  PHASE 3: DECISION & REVIEW                            │
│  └─→ Quality Gate 3: Plan Approval                    │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│  PHASE 4: EXECUTION                                    │
│  ├─→ Quality Gate 4: Pre-Sync Validation              │
│  └─→ Quality Gate 5: Post-Execution Verification      │
└────────────────────────────────────────────────────────┘
```

## Quality Gate 1: After Request Refinement

**Purpose:** Ensure the user's request is specific, achievable, and well-scoped before analysis begins.

**Owner:** request-refiner agent

**Checklist:**

- [ ] Request is specific (not vague or ambiguous)
  - ❌ "Make the skill better"
  - ✅ "Add parallel execution to Phase 2 agents"

- [ ] Success criteria clearly defined
  - Must state measurable outcomes
  - Must specify what "done" looks like

- [ ] Scope boundaries established
  - What IS included in this change
  - What is NOT included (out of scope)

- [ ] Consistency with architecture verified
  - Change aligns with existing skill structure
  - No conflicts with other skills
  - Follows naming conventions

- [ ] User approves refined specification
  - User explicitly confirms the refined request
  - User answers all clarifying questions

**Validation Commands:**

```bash
# No automated validation at this stage
# User approval is the gate
```

**Failure Action:**

- Return to request refinement
- Ask additional clarifying questions
- Present options if multiple interpretations exist

**Example Pass:**

```markdown
Original Request: "Edit the researcher skill"

Refined Specification:
- Objective: Add parallel web search to researcher skill
- Success Criteria:
  - researcher can invoke 3 simultaneous web searches
  - Results aggregated before synthesis
  - No regression in existing functionality
- Scope:
  - IN: Modify researcher/SKILL.md workflow
  - OUT: No changes to external-researcher agent
- Architecture: Consistent with existing multi-agent patterns
- User Approval: ✅ Confirmed
```

---

## Quality Gate 2: After Parallel Analysis

**Purpose:** Ensure all analysis agents completed successfully with no conflicting recommendations.

**Owner:** decision-synthesizer agent

**Checklist:**

- [ ] Best practices review completed (no critical issues)
  - All Anthropic guidelines checked
  - Skill structure specification followed
  - No architectural anti-patterns

- [ ] External research findings documented
  - Relevant forum discussions summarized
  - Blog posts and documentation reviewed
  - Community patterns identified

- [ ] Edge cases identified and simulated
  - Potential failure scenarios documented
  - Boundary conditions tested
  - Error handling paths specified

- [ ] All 4 parallel agents completed
  - best-practices-reviewer finished
  - external-researcher finished
  - edge-case-simulator finished

- [ ] No conflicting recommendations
  - Agents don't contradict each other
  - Inconsistencies resolved
  - Consensus approach identified

### Orchestrator-Specific Checks (SOFT -- if target is orchestrator)

These checks are non-blocking. Failure produces warnings, not gate failures.

- [ ] (SOFT) Orchestrator checklist REQUIRED section completed by best-practices-reviewer
  - 6 REQUIRED patterns evaluated with evidence citations
- [ ] (SOFT) Orchestrator checklist RECOMMENDED section completed by knowledge-engineer
  - 4 RECOMMENDED patterns evaluated with evidence citations
- [ ] (SOFT) Coverage score calculated (N/6 required, M/4 recommended)
- [ ] (SOFT) Missing REQUIRED patterns flagged for implementation plan

**SOFT check failure handling**:
- Log warning: "Orchestrator analysis incomplete -- [specific check]"
- Gate 2 still passes if all HARD checks pass
- Decision-synthesizer notified: "Synthesize without orchestrator-specific input"

**Validation Commands:**

```bash
# Check agent outputs exist
ls -la /tmp/skill-editor-session-*/
# best-practices-review.md
# external-research.md
# edge-cases.md

# Verify no conflicts flag
grep -i "CONFLICT" best-practices-review.md external-research.md edge-cases.md
# Should return empty
```

**Failure Action:**

- Re-run specific agent(s) with refined prompts
- Resolve conflicts through user question
- Proceed only when all analyses agree or conflicts resolved

**Example Pass:**

```markdown
Best Practices Review: ✅
- Follows skill structure specification
- No violations of Anthropic guidelines
- Recommendation: Use existing agent pattern

External Research: ✅
- Found 3 relevant forum threads on parallel agents
- Pattern matches our approach
- Recommendation: Use Task tool with parallel calls

Edge Cases: ✅
- Identified 5 failure scenarios
- All have handling strategies
- Recommendation: Add timeout handling

Conflicts: None
Consensus: Proceed with Task tool parallel execution
```

---

## Quality Gate 3: After Adversarial Review

**Purpose:** Ensure the implementation plan is detailed, correct, and approved by expert reviewer.

**Owner:** adversarial-reviewer agent

**Checklist:**

- [ ] Implementation plan specifies exact file paths
  - All files to modify listed with full paths
  - New files listed with creation paths
  - No ambiguous file references

- [ ] Git workflow clearly defined
  - Which files to `git add`
  - Commit message format specified
  - Push strategy defined (if applicable)

- [ ] Integration points identified
  - Dependencies on other skills/agents
  - sync-config.py interaction specified
  - Planning journal update defined

- [ ] No architectural concerns
  - Reviewer found no critical flaws
  - Design patterns appropriate
  - Performance implications acceptable

- [ ] Reviewer approval obtained
  - Explicit go/no-go decision
  - All concerns addressed
  - User confirms plan

**Validation Commands:**

```bash
# Check plan has exact file paths
grep -E "^(Edit|Create|Delete):" implementation-plan.md | wc -l
# Should be > 0

# Verify file paths are absolute or relative to repo root
grep -E "^(Edit|Create):" implementation-plan.md | grep -v "claude-config/"
# Should return empty (all paths under claude-config/)

# Check git workflow specified
grep -i "git add\|git commit" implementation-plan.md
# Should find both
```

**Failure Action:**

- Revise plan to address concerns
- Re-run adversarial review
- Loop until approval obtained

**Example Pass:**

```markdown
Implementation Plan:

Files to Modify:
- Edit: claude-config/skills/researcher/SKILL.md
  - Add Phase 2 parallel execution
  - Update workflow steps 5-7

Files to Create:
- None

Git Workflow:
- git add claude-config/skills/researcher/SKILL.md
- Commit: "feat(researcher): Add parallel web search in Phase 2"

Integration:
- No dependencies on other skills
- Use existing Task tool for parallel calls
- Update planning journal via sync-config.py plan

Reviewer Assessment:
- Architecture: ✅ Follows existing patterns
- Performance: ✅ 3x faster Phase 2
- Maintainability: ✅ Clear, testable
- Concerns: None

Approval: ✅ GO
```

---

## Quality Gate 4: Before Sync to ~/.claude/

**Purpose:** Ensure all changes are valid and won't break the system when synced.

**Owner:** executor agent

**Checklist:**

- [ ] YAML frontmatter validates
  - All SKILL.md files have valid YAML
  - Required fields present (name, description)
  - Format follows specification

- [ ] JSON validates (for agent files)
  - All .json files are valid JSON
  - Required fields present

- [ ] Skill structure follows specification
  - Directory structure correct
  - File naming conventions followed
  - No prohibited files

- [ ] Examples accurate and complete
  - Examples match current implementation
  - No broken references
  - All code snippets valid

- [ ] No conflicting settings
  - No duplicate skill names
  - No conflicting agent names
  - No file path conflicts

**Validation Commands:**

```bash
# Validate YAML frontmatter
for skill in claude-config/skills/*/SKILL.md; do
  python3 << EOF
import yaml
with open('$skill', 'r') as f:
    content = f.read()
parts = content.split('---', 2)
yaml.safe_load(parts[1])
print("✅ $skill")
EOF
done

# Validate JSON agent files
for agent in claude-config/agents/*.json; do
  python3 -m json.tool "$agent" > /dev/null && echo "✅ $agent"
done

# Check for duplicate names
find claude-config/skills -name "SKILL.md" -exec grep "^name:" {} + | sort | uniq -d
# Should be empty

# Dry-run sync
./sync-config.py push --dry-run
# Should show expected files, no errors
```

**Failure Action:**

- Fix validation errors
- Re-validate
- Do NOT proceed to sync until all checks pass

**Example Pass:**

```bash
$ ./validate-all.sh

Validating YAML frontmatter...
✅ claude-config/skills/skill-editor/SKILL.md
✅ claude-config/skills/researcher/SKILL.md

Validating JSON agents...
✅ claude-config/agents/skill-editor-executor.json

Checking for duplicates...
✅ No duplicate skill names
✅ No duplicate agent names

Dry-run sync...
✅ Would sync 2 files
✅ No conflicts

Quality Gate 4: ✅ PASS
```

---

## Quality Gate 5: After Execution

**Purpose:** Verify the entire change was successful and meets original requirements.

**Owner:** executor agent (using completion-verifier skill)

**Checklist:**

- [ ] Original requirement met
  - Success criteria from Gate 1 achieved
  - Functionality works as specified
  - User confirms satisfaction

- [ ] Edge cases handled
  - Edge cases from Gate 2 tested
  - Error scenarios handled
  - No regressions

- [ ] sync-config.py push successful
  - Files synced to ~/.claude/ without errors
  - No conflicts during sync
  - System state consistent

- [ ] Skill invokes without errors
  - Test skill invocation in Claude session
  - No syntax errors
  - Workflow completes successfully

- [ ] No regressions in existing skills
  - Other skills still work
  - No broken dependencies
  - Integration tests pass

- [ ] Planning journal updated
  - Entry created with title
  - Objective, changes, outcome documented
  - Entry committed to git

**Validation Commands:**

```bash
# Test skill invocation
claude << EOF
/skill-editor "test invocation"
EOF
# Should complete without errors

# Check sync status
./sync-config.py status
# Should show no divergence

# Verify planning journal
ls -l planning/$(hostname)/*.md | tail -1
# Should show recent entry

# Test existing skills (smoke test)
claude << EOF
/completion-verifier
EOF
# Should work

# Check git status
git status
# Should show clean state or staged changes only
```

**Failure Action:**

- Rollback via `git reset --hard HEAD`
- Re-sync from repository: `./sync-config.py push`
- Document failure in planning journal
- Return to Phase 4 or earlier phase as needed

**Example Pass:**

```bash
$ ./verify-completion.sh

Testing skill invocation...
✅ /researcher completes successfully
✅ Parallel execution works (3 agents run)
✅ Results synthesized correctly

Checking sync status...
✅ No divergence between repo and ~/.claude/

Verifying planning journal...
✅ Entry created: 2026-02-02-add-parallel-search-researcher.md
✅ Objective, changes, outcome documented

Testing existing skills...
✅ /completion-verifier works
✅ /skill-editor works
✅ No regressions detected

Git status...
✅ Changes committed
✅ Planning entry committed

Quality Gate 5: ✅ PASS
```

---

## Escalation Framework

Quality gates integrate with CONFIG_MANAGEMENT.md decision thresholds:

### Major Decisions → User Approval Required

- Adding new quality gate
- Changing gate pass/fail criteria
- Skipping a quality gate

**Action:** Use AskUserQuestion before proceeding

### Medium Decisions → User Approval Required

- Re-running a phase after gate failure
- Modifying gate checklist
- Adding validation command

**Action:** Use AskUserQuestion with options

### Minor Decisions → Agent Decides

- Fixing validation syntax error
- Updating planning entry
- Re-running validation command

**Action:** Proceed, notify user in summary

## Summary

Quality gates ensure:

1. **Gate 1**: Clear requirements before work begins
2. **Gate 2**: Thorough analysis before decisions
3. **Gate 3**: Expert approval before implementation
4. **Gate 4**: Syntax validity before system changes
5. **Gate 5**: Complete verification before closure

Each gate has:
- Clear owner (which agent checks)
- Specific checklist
- Validation commands
- Failure action

This structured approach prevents:
- Scope creep
- Incomplete analysis
- Syntax errors in production
- Unverified changes
- Regressions

All gates must pass for successful workflow completion.
