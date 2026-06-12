---
name: skill-editor
description: Use when creating, modifying, or refactoring Claude Code skills that require structured multi-agent review and quality validation

# Handoff metadata (custom extension -- see workflow-coordinator/references/frontmatter-metadata-standard.md)
handoff:
  accepts_from: "*"
  provides_to: programming-pm, technical-pm
  schema_version: "3.0"
  schema_type: universal

categories: skill-development, workflow-creation

input_requirements: specification, skill-request

output_types: skill, agent-configuration, documentation
---

# Skill Editor

Comprehensive multi-agent workflow system for editing Claude Code skills with structured phases, quality gates, and expert review.

## When to Use This Skill

Use this skill when:

1. **Creating new skills**: User wants to add a new skill to the repository
2. **Modifying existing skills**: User wants to update, enhance, or refactor a skill
3. **Complex skill changes**: Change involves multiple files, agents, or architectural decisions
4. **Quality assurance needed**: Change requires thorough review and validation

This skill provides:
- Structured 4-phase workflow (2 modes: QUICK and FULL)
- Interactive requirements refinement
- Multi-perspective swarm analysis via brainstorming-pm delegation (FULL mode)
- Domain-specific edge-case analysis (FULL mode)
- Adversarial review before implementation (FULL mode)
- Automated validation and testing
- Integration with sync-config.py and planning journal

## When NOT to Use This Skill

Do NOT use this skill when:

- **Simple documentation fixes**: Typo fixes, minor documentation updates (edit directly)
- **Non-skill changes**: Modifying agents, settings, or other configuration
- **Urgent hotfixes**: Emergency fixes that can't wait for full workflow
- **Exploratory work**: Just browsing or understanding skills (use Read or Explore agent)
- **New skills from scratch (no quality gates needed)**: Use `skill-creator` for a lightweight create-draft-eval-iterate loop without the full 4-phase workflow
- **Need a full plugin (multiple skills, agents, commands)**: Use `plugin-dev` — skill-editor handles individual skill files; plugin-dev covers the broader plugin architecture

## Delegation Mandate

You are an **orchestrator**. You coordinate specialist agents -- you do not perform specialist analysis, research, or implementation yourself.

**You ARE the coordinator who ensures** analysis, research, review, and implementation happen through delegation to specialist agents via Task tool.

**You are NOT** an analyst, researcher, reviewer, or implementor. You do not perform best-practices analysis, external research, edge-case simulation, knowledge-engineering analysis, adversarial review, or code implementation yourself.

**Orchestrator-owned tasks** (you DO perform these yourself):
- Session setup, directory creation, state file management
- Mode detection and user interaction for mode selection
- Quality gate evaluation (checking that agent outputs meet criteria)
- User communication (presenting options, gathering decisions)
- Workflow routing (determining which phase to execute next)
- Pre-flight validation (git checks, file existence)
- Orchestrator detection (determining if target skill is an orchestrator)

### When You Might Be Resisting Delegation

| Rationalization | Reality |
|----------------|---------|
| "This analysis is too simple to delegate" | Simple tasks still consume context window. Delegate. |
| "I can do it faster myself" | Speed is not the goal; context isolation and specialist quality are. |
| "The agent will just repeat what I already know" | The agent provides independent verification. Your knowledge may be incomplete. |
| "It's just a quick read of the file" | Reading specialist content to make specialist decisions IS specialist work. |

**Self-check before every action**: "Am I about to load specialist instructions into my context so I can do their work? If yes, use Task tool instead."

## State Anchoring

Start every response with a phase indicator:

```
[Phase N/4 - {phase_name}] {brief status}
```

Examples:
- `[Phase 1/4 - Refinement] Gathering requirements from user`
- `[Phase 2/4 - Analysis] Swarm complete, waiting for edge-case-simulator`
- `[Phase 3/4 - Decision] Synthesizing swarm + edge-case reports`
- `[Phase 4/4 - Execution] Implementing change 3/12`

**Protocol**:
1. Before starting any phase: Read `${SESSION_DIR}/session-state.json`. Confirm current_phase matches expectations.
2. After any user interaction: Answer the user, then re-anchor with phase indicator.
3. If phase indicator and state file disagree: Trust state file, not memory.

## Tool Selection

| Situation | Tool | Reason |
|-----------|------|--------|
| Phase 2 swarm analysis | Task tool (brainstorming-pm) | Multi-perspective analysis via swarm delegation |
| Phase 2 edge-case analysis | Task tool (edge-case-simulator) | Domain-specific failure modes, parallel with swarm |
| Phase 3 adversarial review | Task tool (adversarial-reviewer) | Independent, skeptical review |
| Phase 4 implementation | Task tool (executor) | Isolated execution environment |
| Loading reference docs for YOUR routing decisions | Read tool | Orchestrator decision support |
| Loading skill instructions to decide WHICH specialist to invoke | Read tool (brief scan) | Routing information, not specialist work |
| User interaction (questions, approvals, options) | AskUserQuestion | Structured user communication |
| File operations (create, modify files) | Write tool (via executor agent) | Delegated to executor specialist |
| Validation scripts, git operations | Bash tool | Infrastructure commands |

**Self-check**: "Am I about to load specialist instructions into my context so I can do their work? If yes, use Task tool instead."

## Workflow Overview

```
QUICK MODE (~30 min)
├── Phase 1: Refinement
├── [SKIP Phase 2]
├── Phase 3: Lightweight plan (orchestrator creates minimal plan)
└── Phase 4: Execution (Gate 3 always runs)

FULL MODE (~1.5-2 hrs) [Default]
├── Phase 1: Refinement
├── Phase 2: Swarm + Edge-case analysis (parallel)
├── Phase 3: Inline synthesis + Adversarial review
└── Phase 4: Execution (Gate 3 always runs)
```

## Workflow

### Pre-Workflow: Safety Checks

Before starting workflow, run the session management script which performs:
- Git safety checks (uncommitted changes, merge/rebase detection, detached HEAD)
- sync-config.py status verification
- Directory verification (must be repo root)
- Archival awareness detection
- Trap handler registration for graceful interrupt
- Session management commands (`--list-sessions`, `--cleanup`)
- Resume protocol with multi-session support (including legacy format migration)
- Session directory creation and state initialization

**Implementation**: See `references/session-management.sh` for complete bash.

If checks fail: Ask user to resolve before proceeding.

### If User Cancels (Ctrl+C)

Session state is preserved in `${SESSION_DIR}/session-state.json`.

On next invocation:
1. Offer to resume from last phase
2. If declined, session remains in /tmp/skill-editor-session/{session-id}
3. Re-sync if needed: `./sync-config.py push`

### Phase 1: Refinement (Interactive)

**Objective**: Transform user's request into detailed, unambiguous specification.

**Agent**: `skill-editor-request-refiner`

**Model**: Opus 4.6

**Process**:

1. Launch request-refiner agent via Task tool
2. Agent asks clarifying questions to understand:
   - What user wants to change
   - Why they want this change
   - What success looks like
   - What's in scope vs. out of scope
3. Agent reads existing skill (if modifying)
4. Agent establishes clear boundaries and success criteria
5. Agent presents refined specification to user

**Output File**: `${SESSION_DIR}/refined-specification.md` containing:
- Objective (one sentence)
- Scope (IN/OUT lists)
- Success criteria (measurable)
- Files affected
- User approval

**Quality Gate 1: Specification Approval**

User must approve:
- [ ] Specification matches intent
- [ ] Scope is appropriate
- [ ] Success criteria are clear
- [ ] Ready to proceed to analysis

**If Gate 1 fails**: Return to request-refiner for more refinement.

**If Gate 1 passes**: Update session state and proceed to Mode Selection.

**Post-Gate 1: Orchestrator Detection**

After specification approval, determine if the target skill is an orchestrator:

1. Read target SKILL.md (if editing an existing skill)
2. Score against detection criteria:

| Signal | Score | Check |
|--------|-------|-------|
| Name contains orchestrator keyword (pm, coordinator, orchestrator, pipeline, architect) | +1 | Check skill name |
| Description mentions coordination terms (coordinate, orchestrate, multi-agent, pipeline) | +1 | Check description field |
| Delegates to other skills via Task tool | +2 | Search for Task tool usage |
| Has named phases/stages with sequential progression | +1 | Search for Phase/Stage headers |
| Has quality gates between phases | +1 | Search for Gate references |
| Manages session state across phases | +1 | Search for state file management |

3. Apply thresholds:
   - Score >= 4: `"Detected as orchestrator (confidence: high). Apply orchestrator analysis? [Y/n]"`
   - Score 2-3: `"May be an orchestrator (confidence: medium). Apply orchestrator analysis? [y/N]"`
   - Score 0-1: Not an orchestrator. Skip orchestrator analysis.
   - Always append: `"If this IS an orchestrator, reply 'orchestrator' to enable pattern analysis."`

4. If creating a new skill: Ask directly: "Will this skill orchestrate other skills? [y/N]"

5. Record detection result in session state:
   ```json
   "orchestrator_detected": true/false,
   "orchestrator_confidence": "high"/"medium"/"none",
   "orchestrator_user_confirmed": true/false
   ```

Update session state to phase 1.5 with `agents_completed: ["request-refiner"]`.

---

### Mode Selection (After Phase 1)

**Objective**: Select workflow execution mode.

**Trigger**: After Quality Gate 1 passes (specification approved)

**Decision rule**:
- **Default**: FULL
- **Auto-detect QUICK**: Single file AND <50 lines AND (documentation OR typo OR comment fix)
- User can always override in either direction
- When uncertain: default to FULL (preserves safety)

**Modes**:

| Mode | When | What runs | Duration |
|------|------|-----------|----------|
| QUICK | Documentation, typos, single-file fixes | Phase 1 → Phase 3 (lightweight) → Phase 4 | ~30 min |
| FULL | Everything else (default) | Phase 1 → Phase 2 (swarm + edge-case) → Phase 3 (synthesis + adversarial) → Phase 4 | ~1.5-2 hrs |

Record mode selection in session state and proceed.

---

### Phase 2: Analysis (FULL mode only)

**Objective**: Analyze proposed change from multiple expert perspectives using two parallel tracks.

**Agents** (run in parallel):
- **Track A**: `brainstorming-pm` (swarm delegation) — multi-perspective analysis
- **Track B**: `skill-editor-edge-case-simulator` (Opus 4.6) — domain-specific failure modes

#### Track A: Brainstorming-PM Swarm Delegation

1. Read `references/swarm-challenge-templates.md`
2. Fill challenge template with values from refined specification:
   - Skill name, change type, file count, line count
   - Orchestrator detection result
   - Specification summary (objective + scope)
   - Current skill summary (if modifying existing skill)
3. Invoke `brainstorming-pm` via Task tool with the filled challenge template
4. Receives convergent/divergent insights with confidence scores from 5-archetype swarm

**Quality threshold**: Synthesis must contain 2+ specific recommendations and 1+ alternative approach. If below threshold: log and proceed without swarm input.

**Timeout**: 15 minutes. On timeout: skip swarm, proceed with edge-case-simulator output only.

**Orchestrator Analysis** (conditional -- when orchestrator_detected is true):
- Add to challenge template: "This skill is an orchestrator -- evaluate against orchestrator patterns in references/orchestrator-checklist.md (6 REQUIRED + 4 RECOMMENDED patterns)"

#### Track B: Edge-Case Simulator

1. Launch `skill-editor-edge-case-simulator` via Task tool with refined specification
2. Agent produces skill-specific failure mode matrix covering:
   - YAML parsing failures, sync-config.py edge cases
   - Task tool timeouts, git dirty state scenarios
   - Claude Code-specific boundary conditions
3. Quality threshold: report exists and >100 words

**Output Files**:
- `${SESSION_DIR}/swarm-synthesis.md` (from brainstorming-pm, or absent if skipped/degraded)
- `${SESSION_DIR}/edge-cases.md` (from edge-case-simulator)

**Quality Gate 2: Analysis Completion**

| Track A (swarm) | Track B (edge-case) | Action |
|-----------------|---------------------|--------|
| Complete | Complete | PASS |
| Below threshold | Complete | PASS with note (graceful degradation) |
| Timeout | Complete | PASS with note (proceed without swarm) |
| Any | Failed | RETRY edge-case-simulator once, then ask user |

**If Gate 2 passes**: Update session state to phase 3 and proceed.

---

### Phase 3: Decision

**QUICK mode**: Orchestrator creates a minimal implementation plan directly from the refined specification. No swarm analysis or adversarial review — just objective, files to modify, validation steps, and rollback plan. If target files include core workflow/agent files, offer upgrade to FULL mode. Proceed to Phase 4.

**FULL mode**: Full synthesis + adversarial review (below).

#### Part A: Inline Synthesis (orchestrator-owned, FULL mode)

The orchestrator performs synthesis directly (like brainstorming-pm Stage 3), NOT via a separate agent:

1. Read swarm synthesis output (`swarm-synthesis.md`) — convergent/divergent insights
2. Read edge-case report (`edge-cases.md`)
3. Identify consensus and conflicts across both sources
4. Resolve conflicts or present options to user:
   - **Major decisions**: MUST ask user via AskUserQuestion (new agents, structure changes)
   - **Medium decisions**: SHOULD ask user (workflow changes)
   - **Minor decisions**: Orchestrator decides (examples, docs)
5. Create detailed implementation plan with:
   - Exact file paths and specific changes
   - Edge case handling strategies
   - Validation steps and rollback plan

**Orchestrator-Specific Synthesis** (when orchestrator_detected is true):
- If REQUIRED orchestrator patterns are ABSENT: plan MUST include adding them
- If RECOMMENDED patterns are ABSENT: plan SHOULD note them as suggestions
- Reference `orchestrator-best-practices.md` for pattern templates

**Output File**: `${SESSION_DIR}/implementation-plan.md`

#### Part B: Adversarial Review (delegated)

**Agent**: `skill-editor-adversarial-reviewer`

**Model**: Opus 4.6 (expert review)

**Process**:

1. Launch adversarial-reviewer via Task tool with implementation plan
2. Reviewer reads plan with expert skepticism
3. Challenges assumptions, identifies uncaught failure modes
4. Verifies exact file paths and git workflow safety
5. Checks alignment with original specification
6. Provides verdict: GO / CONDITIONAL / NO-GO

**Output File**: `${SESSION_DIR}/adversarial-review.md`

**Quality Gate 2: Plan Approval**

Check:
- [ ] Implementation plan has exact file paths
- [ ] Git workflow is safe and correct
- [ ] Adversarial reviewer approved (GO or CONDITIONAL with fixes applied)
- [ ] User approves plan

**If CONDITIONAL**: Fix issues, re-review.
**If NO-GO**: Revise plan, re-submit.
**If user doesn't approve**: Refine plan or return to Phase 1.

**If Gate 2 passes**: Update session state to phase 4 and proceed.

---

### Phase 4: Execution (Implement + Validate + Commit)

**Objective**: Execute approved plan with validation at each step.

**Agent**: `skill-editor-executor`

**Model**: Opus 4.6

**Process**:

#### Step 1: Pre-Implementation Safety
- `git status` — must be clean
- `./sync-config.py status` — must be synced
- `pwd` — must be repo root
- Stop if any check fails.

#### Step 2: Implement Changes
For each file in implementation plan:
- **Edit**: Read first, then Edit with exact string replacement
- **Create**: Write new file
- **Delete**: Remove file

#### Step 3: Quality Gate 3 - Pre-Sync Validation
- Validate YAML frontmatter for all modified skills
- Validate JSON for modified agents
- Dry-run sync: `./sync-config.py push --dry-run`

**If Gate 3 fails**: Fix issues, re-validate, do NOT proceed until pass.

#### Step 4: Sync to ~/.claude/
- `./sync-config.py push`
- `./sync-config.py status` — verify no divergence

#### Step 5: Test Skill Invocation
- Verify skill file exists at `$HOME/.claude/skills/$SKILL_NAME/SKILL.md`
- Verify YAML parses
- Smoke test existing skills (no regressions)

#### Step 6: Post-Execution Verification (part of Gate 3)
- [ ] Original requirement met (from refined spec)
- [ ] Edge cases handled (from edge-case report, if FULL mode)
- [ ] sync-config.py push successful
- [ ] Skill invokes without errors
- [ ] No regressions in existing skills
- [ ] Planning journal entry ready

**If verification fails**: Rollback via `git reset --hard HEAD`, re-sync, fix, retry.

#### Step 7: Update Planning Journal
`./sync-config.py plan --title "[Brief description from refined spec]"`

Optionally run `claude-md-management:revise-claude-md` to incorporate any workflow learnings into CLAUDE.md documentation.

#### Optional: Git Strategy Advisory
Before committing, MAY invoke `git-strategy-advisor` via Task tool in post-work mode for scope-adaptive git recommendations. This is advisory only — Step 8 logic takes precedence.

#### Step 8: Commit Changes

Stage specific files (NEVER -A or .), commit with HEREDOC multi-line message using conventional commit format (`feat`/`fix`/`docs`) and including `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`, then mark session as completed.

**Git Safety Checklist**:
- [ ] Specific files staged (not -A or .)
- [ ] Conventional commit format (feat/fix/docs)
- [ ] Descriptive message
- [ ] Co-authored-by line
- [ ] No destructive operations
- [ ] No hook bypasses

#### Step 9: Report Completion

Generate completion report with:
- Summary of changes
- Validation results (Gate 3)
- Testing results
- Commit SHA
- Planning journal entry path
- Success criteria verification
- Session completion status

---

## Escalation Framework

Decision thresholds (from CONFIG_MANAGEMENT.md):

### Major Decisions → User Approval Required

- Add new agent to workflow
- Change skill structure specification
- Modify core workflow phases

**Action**: Use AskUserQuestion before proceeding

### Medium Decisions → User Approval Required

- Modify existing skill's core workflow
- Add new supporting skill
- Change skill naming convention

**Action**: Use AskUserQuestion with options

### Minor Decisions → Agent Decides

- Add example to existing skill
- Fix documentation typo
- Update reference material

**Action**: Proceed, notify user

## Error Handling

### Retry Protocol (Phase 2 Agent Failures)
- edge-case-simulator failure: Wait 30s, retry once automatically, then ask user
- brainstorming-pm timeout (>15 min): Skip swarm, proceed with edge-case output only
- brainstorming-pm below quality threshold: Log and proceed without swarm input

### Graceful Degradation
- Swarm timeout or failure: Proceed without swarm analysis (orchestrator creates plan from specification + edge-case report only)
- Edge-case-simulator timeout (after retry): Ask user to proceed with specification-only plan or abort

### Rollback Protocol (Phase 4 Failures)
1. Stop immediately
2. `git reset --hard HEAD` (revert uncommitted changes)
3. `./sync-config.py push` (re-sync from repo)
4. Document failure in planning journal
5. Report to user with options: retry, skip, or abort

### Interrupt Handling (User Cancels)
1. Check git status
2. Rollback uncommitted changes: `git reset --hard HEAD`
3. Re-sync: `./sync-config.py push`
4. Session state preserved in `${SESSION_DIR}/` for potential resume
5. Document in planning journal: "Cancelled by user"

## Integration with Existing Tools

### CONFIG_MANAGEMENT.md

This workflow extends the 7-step CONFIG_MANAGEMENT.md process:

- **Step 1 (Safety Check)**: Pre-workflow checks
- **Step 2 (Planning Entry)**: Phase 4, Step 7
- **Step 3 (Implement)**: Phase 4, Step 2
- **Step 4 (Quality Analysis)**: Phases 2-3, Quality Gates
- **Step 5 (Preview/Sync)**: Phase 4, Steps 3-4
- **Step 6 (Test)**: Phase 4, Step 5
- **Step 7 (Commit)**: Phase 4, Step 8

### sync-config.py

Executor agent uses sync-config.py:
- `./sync-config.py status` (pre-flight check)
- `./sync-config.py push --dry-run` (validation)
- `./sync-config.py push` (apply changes)
- `./sync-config.py plan` (create planning entry)

### Planning Journal

Planning entry created in Phase 4, Step 7:
- Title: Brief description from refined spec
- Objective: From refined specification
- Changes: Files modified
- Testing: Validation and test results
- Outcome: Success/Partial/Failed

## Quality Gates Summary

| Gate | Phase | Owner | Criteria | Failure Action |
|------|-------|-------|----------|----------------|
| 1: Specification Approval | Phase 1 | request-refiner | Spec approved by user | Return to refinement |
| 2: Plan Approval | Phase 3 | adversarial-reviewer + user | Adversarial GO + user approves plan | Revise plan |
| 3: Execution Verification | Phase 4 | executor | YAML validates, sync succeeds, skill invokes, no regressions | Rollback |

## Examples

### Example 1: Add Parallel Execution to Researcher

**User Request**:
```
/skill-editor "Add parallel web search to researcher skill"
```

**Phase 1 Output**:
```markdown
Objective: Modify researcher skill to execute 3 WebSearch calls in parallel

Scope:
- IN: researcher/SKILL.md Phase 2 workflow
- OUT: No changes to agents or other phases

Success Criteria:
- 3 WebSearch calls execute simultaneously
- Results synthesized correctly
- No regressions
```

**Phase 2 Findings**:
- Swarm: Consensus on Task tool for parallel calls, alternative approaches explored
- Edge cases: Handle timeout, network failure, partial results

**Phase 3 Plan**:
```markdown
Edit: claude-config/skills/researcher/SKILL.md
Lines 45-60: Replace sequential WebSearch with parallel

Implementation:
[3 Task tool calls in single message]
```

**Phase 4 Result**:
```
YAML validates, sync succeeds, skill invokes correctly
Commit: feat(researcher): Add parallel web search
```

### Example 2: Create New Skill

**User Request**:
```
/skill-editor "Create a new skill for API documentation"
```

**Process**:
- Phase 1: Refine requirements (which APIs? format? tools?)
- Phase 2: Analyze (best practices for doc skills, community patterns, edge cases)
- Phase 3: Plan (file structure, workflow steps, examples)
- Phase 4: Create files, validate, sync, test, commit

## Timeout Configuration

| Phase | Component | Timeout | Exceeded Action |
|-------|-----------|---------|-----------------|
| 1 | request-refiner | 30 min | Escalate to user |
| 2 | brainstorming-pm (swarm) | 15 min | Skip swarm, proceed with edge-case only |
| 2 | edge-case-simulator | 10 min | Auto-retry once, then user decision |
| 3 | adversarial-reviewer | 30 min | Escalate to user |
| 4 | executor | 60 min | Escalate to user |
| Global | entire workflow | 3 hours | Safety ceiling, force escalate |

## Notes

- **Hybrid swarm + specialist model**: brainstorming-pm provides multi-perspective analysis, edge-case-simulator provides domain-specific failure modes
- **All agents use Opus 4.6**: Maximum quality for all workflow phases
- **3 quality gates**: Specification Approval, Plan Approval, Execution Verification
- **Rollback on failure**: Safe to abort at any point
- **Planning journal provides traceability**: Full documentation of changes
- **Integration tested**: Works with sync-config.py and existing workflows

## References

See `skill-editor/references/` for:
- `swarm-challenge-templates.md`: Challenge template for brainstorming-pm swarm delegation
- `session-management.sh`: Git safety checks, session creation/resume, cleanup commands
- `anthropic-guidelines-summary.md`: Anthropic best practices
- `skill-structure-specification.md`: Skill format and validation
- `quality-gates.md`: Detailed quality gate checklists
- `orchestrator-checklist.md`: Orchestrator pattern evaluation checklist
- `orchestrator-best-practices.md`: Orchestrator pattern templates

## Success Criteria

Skill-editor workflow succeeds when:

- [ ] User's original request is fulfilled
- [ ] All quality gates pass
- [ ] Changes are synced to `~/.claude/`
- [ ] Skill invokes without errors
- [ ] No regressions in existing skills
- [ ] Planning journal documents changes
- [ ] Changes committed to git
- [ ] User confirms satisfaction
