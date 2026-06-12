# Orchestrator Best Practices

> Canonical reference for orchestrator skill patterns extracted from 8 existing orchestrators.
> This document is the single source of truth. Other files reference it, not duplicate it.

**Version**: 1.0
**Last Updated**: 2026-02-07
**Source Orchestrators**: 8 (programming-pm, lit-pm, scientific-analysis-architect, brainstorming-pm, skill-editor, technical-pm, research-pipeline, parallel-coordinator)
**Next Review**: When a new orchestrator is created or modified

**Staleness Warning**: If current date is more than 90 days past Last Updated, patterns may not reflect recent orchestrator changes. Consider running a refresh analysis.

---

## What Is an Orchestrator Skill?

An orchestrator skill coordinates other skills or agents to accomplish complex, multi-phase work. It delegates specialist tasks, manages state across phases, enforces quality gates, and handles errors and timeouts.

### Detection Algorithm

Score the target skill against these signals (0-7 possible):

| Signal | Score | Check |
|--------|-------|-------|
| Name contains orchestrator keyword (pm, coordinator, orchestrator, pipeline, architect) | +1 | Check skill name |
| Description mentions coordination terms (coordinate, orchestrate, multi-agent, pipeline) | +1 | Check description field |
| Delegates to other skills via Task tool | +2 | Search for Task tool usage |
| Has named phases/stages with sequential progression | +1 | Search for Phase/Stage headers |
| Has quality gates between phases | +1 | Search for Gate references |
| Manages session state across phases | +1 | Search for state file management |

**Decision thresholds**:
- Score >= 4: High confidence orchestrator. Prompt: "Detected as orchestrator (confidence: high). Apply orchestrator analysis? [Y/n]"
- Score 2-3: Medium confidence. Prompt: "May be an orchestrator (confidence: medium). Apply orchestrator analysis? [y/N]"
- Score 0-1: Not an orchestrator. Skip orchestrator analysis.

**Recovery for false negatives**: Always append to detection output: "If this IS an orchestrator, reply 'orchestrator' to enable pattern analysis."

---

## Pattern Classification Methodology

Patterns are classified into 4 evidence-based tiers:

| Tier | Criteria | Severity |
|------|----------|----------|
| **Best Practice** | 4+ orchestrators, independently discovered, demonstrated effectiveness | REQUIRED |
| **Strong Practice** | 4+ orchestrators OR 2+ with strong evidence, independently discovered | RECOMMENDED |
| **Common Practice** | 2-3 orchestrators, may be propagated rather than independently discovered | RECOMMENDED |
| **Promising Pattern** | 1 orchestrator, insufficient evidence for broader classification | OPTIONAL |

---

## Pattern Categories

- **Identity and Role**: Delegation Mandate, Tool Selection Table
- **State and Lifecycle**: State Anchoring, Session Management, Timeout Configuration
- **Communication**: Handoff Schema, Handoff Frontmatter, Pre-Flight Validation
- **Quality and Safety**: Error Handling (Structured), Mode Selection, Quality Gate Override

---

## REQUIRED Patterns (6 patterns)

### Pattern 1: Delegation Mandate

**Classification**: Best Practice | **Severity**: REQUIRED | **Adoption**: 4/8

**Source orchestrators**: programming-pm (Delegation Mandate section), lit-pm (Delegation Mandate section), scientific-analysis-architect (Delegation Mandate section), brainstorming-pm (Delegation Mandate section)

**Evidence**: Prevents context bloat by keeping specialist instructions out of orchestrator context. All 4 implementations were independently developed with consistent structure.

**Variants**:
- **Formal anti-resistance table** (programming-pm only): Full Rationalization/Reality table with 5+ entries
- **Self-check prompt** (lit-pm, scientific-analysis-architect, brainstorming-pm): Briefer "Am I about to do specialist work?" prompt with 2-3 rationalization examples

**Template** (formal variant):

```markdown
## Delegation Mandate

You are an **orchestrator**. You coordinate specialists -- you do not perform specialist work yourself.
**You ARE the coordinator who ensures** [actions] happen through delegation.
**You are NOT** a [specialist]. You do not [specialist actions].
**Orchestrator-owned tasks**: Session setup, state management, quality gate evaluation, user communication, workflow routing.

### When You Might Be Resisting Delegation
| Rationalization | Reality |
|----------------|---------|
| "This is too simple to delegate" | Simple tasks still consume context window. Delegate. |
| "I can do it faster myself" | Speed is not the goal; context isolation is. |

**Self-check**: "Am I about to load specialist instructions into my context? If yes, use Task tool."
```

**Applicability**: All orchestrator skills. Skip only if the skill has a single phase with no delegation.

---

### Pattern 2: State Anchoring

**Classification**: Best Practice | **Severity**: REQUIRED | **Adoption**: 4/8

**Source orchestrators**: programming-pm (State Anchoring section), lit-pm (State Anchoring section), scientific-analysis-architect (State Anchoring section), brainstorming-pm (State Anchoring section)

**Evidence**: Prevents phase drift during long multi-phase sessions. All 4 implementations use response-prefix format.

**Template**:

```markdown
## State Anchoring

Start every response with: `[Phase N/M - {phase_name}] {brief status}`

**Protocol**:
1. Before starting any phase: Read state file. Confirm current_phase matches expectations.
2. After any user interaction: Answer the user, then re-anchor with phase indicator.
3. If phase indicator and state file disagree: Trust state file, not memory.
```

**Applicability**: All orchestrator skills with 2+ phases. Skip for single-phase orchestrators.

---

### Pattern 3: Tool Selection Table

**Classification**: Best Practice | **Severity**: REQUIRED | **Adoption**: 4/8

**Source orchestrators**: programming-pm (Tool Selection section), lit-pm (Tool Selection section), scientific-analysis-architect (Tool Selection section), brainstorming-pm (Tool Selection section)

**Evidence**: Prevents incorrect tool use (e.g., using Read tool for specialist work instead of Task tool for delegation).

**Template**:

```markdown
## Tool Selection

| Situation | Tool | Reason |
|-----------|------|--------|
| Specialist doing independent work | Task tool | Context isolation |
| 2+ specialists simultaneously | Task tool (multiple) | Parallelization |
| Loading domain knowledge for YOUR routing decisions | Read tool | Orchestrator decision support |
| User interaction | AskUserQuestion | Structured communication |
| File operations | Write/Edit tool (via executor) | Delegated to specialist |
| Infrastructure commands | Bash tool | Validation, git, sync |

**Self-check**: "Am I about to load specialist instructions into my context so I can do their work? If yes, use Task tool instead."
```

**Applicability**: All orchestrator skills that delegate work. Skip for orchestrators that only sequence file operations.

---

### Pattern 4: Error Handling (Structured)

**Classification**: Best Practice | **Severity**: REQUIRED | **Adoption**: 5/8

**Source orchestrators**: programming-pm (Circuit Breaker section), lit-pm (Saga Compensation section), scientific-analysis-architect (Error Handling section), brainstorming-pm (Timeout/Error section), skill-editor (Error Handling section)

**Evidence**: Named error patterns enable consistent recovery behavior. Orchestrators without structured handling exhibit ad-hoc, inconsistent error responses.

**Named patterns**:
- **Retry Protocol**: First failure auto-retry, second failure user decision, maximum N attempts
- **Graceful Degradation**: Supplementary failures proceed without; critical failures escalate
- **Circuit Breaker** (programming-pm): Open after N consecutive failures, require user decision
- **Saga Compensation** (lit-pm): Per-stage forward and compensation actions
- **Rollback Protocol**: Stop, revert, re-sync, document, report

**Template**:

```markdown
## Error Handling

### Retry Protocol
- First failure: Wait 30s, retry automatically
- Second failure: User decision required
- Maximum 2 attempts per critical component

### Graceful Degradation
- Supplementary component timeout: Proceed without
- Critical component timeout (after retry): Escalate to user

### Circuit Breaker
- If 2+ critical components fail: Stop retrying, escalate to user
- User choices: retry all, proceed with available, or abort

### Rollback Protocol
1. Stop immediately
2. Revert uncommitted changes
3. Re-sync state
4. Document failure
5. Report to user with options
```

**Applicability**: All orchestrator skills. Adjust specific patterns based on architecture (saga for stage-based, circuit breaker for parallel execution).

---

### Pattern 5: Timeout Configuration

**Classification**: Best Practice | **Severity**: REQUIRED | **Adoption**: 5/8

**Source orchestrators**: programming-pm (timeout-config.md reference), lit-pm (Timeout Configuration section), scientific-analysis-architect (Timeout Configuration section), brainstorming-pm (Timeout Configuration section), research-pipeline (stage timeout section)

**Evidence**: Prevents indefinite hangs in multi-agent workflows. Orchestrators without timeout configuration have experienced unbounded agent execution.

**Template**:

```markdown
## Timeout Configuration

| Phase | Component | Timeout | Exceeded Action |
|-------|-----------|---------|-----------------|
| 1 | [component] | N min | [action] |
| 2 | [component] | N min | [action] |
| Global | entire workflow | N hours | Safety ceiling, force escalate |
```

**Applicability**: All orchestrator skills that delegate to agents. Skip for orchestrators that only perform file operations.

---

### Pattern 6: Session Management

**Classification**: Best Practice | **Severity**: REQUIRED | **Adoption**: 5/8

**Source orchestrators**: skill-editor (Pre-Workflow section), programming-pm (Session Management section), lit-pm (Session Management section), scientific-analysis-architect (Session Management section), brainstorming-pm (atomic writes section)

**Evidence**: Enables resume after interruption. Orchestrators without session management lose all progress on interrupt.

**Key elements**:
- Session directory in /tmp/ or project directory
- State file (JSON or YAML) tracking current phase
- Interrupt handling (trap signals, persist state)
- Resume protocol (detect existing session, offer resume)
- Atomic writes (write .tmp, validate, rename -- from brainstorming-pm)

**Template**:

```markdown
## Session Management
- **Session Directory**: `/tmp/{skill-name}-session/` with `session-state.json`
- **Interrupt Handling**: Persist current state before exit; session artifacts preserved for resume
- **Resume Protocol**: On invocation, check for existing session; offer resume from last completed phase
```

**Applicability**: All orchestrator skills with workflows longer than 10 minutes. Skip for quick single-pass orchestrators.

---

## RECOMMENDED Patterns (4 patterns)

### Pattern 7: Handoff Schema

**Classification**: Strong Practice | **Severity**: RECOMMENDED | **Adoption**: 4/8

**Source orchestrators**: programming-pm (Handoff Schema section with validation scripts), lit-pm (Handoff Schema v1.1), research-pipeline (Handoff v1.0), brainstorming-pm (perspective-swarm handoffs)

**Evidence**: Structured handoffs reduce information loss between phases. However, no direct outcome data comparing structured vs. unstructured handoffs.

**Template**: YAML schema with fields: version, from_phase, to_phase, producer, consumer, timestamp, deliverable (location), context (focus_areas, known_gaps), quality (status, confidence). See programming-pm Handoff Schema section for the most mature example.

---

### Pattern 8: Pre-Flight Validation

**Classification**: Strong Practice | **Severity**: RECOMMENDED | **Adoption**: 2/8

**Source orchestrators**: programming-pm (Pre-Flight Validation section), lit-pm (Dependency Check section)

**Evidence**: Catches missing dependencies before workflow starts, preventing late-stage failures. Strong evidence despite low adoption.

**Template**: Check required skill dependencies (abort if missing) and optional dependencies (warn and continue). See programming-pm Pre-Flight Validation section for full bash example.

---

### Pattern 9: Mode Selection / Complexity Detection

**Classification**: Common Practice | **Severity**: RECOMMENDED | **Adoption**: 3/8

**Source orchestrators**: skill-editor (Mode Selection section), programming-pm (Complexity Detection section), lit-pm (Adaptive Orchestration section)

**Evidence**: Adapts workflow depth to change complexity. Uncertain whether complexity detection accuracy justifies the implementation cost.

**Key elements**:
- Three-tier detection (simple/standard/complex)
- User override with confirmation for risky overrides
- Mode-based branching (skip phases for simple changes)

---

### Pattern 10: Handoff Frontmatter

**Classification**: Common Practice | **Severity**: RECOMMENDED | **Adoption**: 3/8

**Source orchestrators**: programming-pm (YAML frontmatter), lit-pm (YAML frontmatter), brainstorming-pm (YAML frontmatter)

**Note**: This pattern may have propagated from programming-pm rather than being independently discovered. All three implementations share similar structure.

**Template**: YAML frontmatter block with fields: accepts_handoff, handoff_categories, handoff_description, handoff_trigger, protocol_version, requires, optional_consumes. See programming-pm frontmatter for the canonical example.

---

## OPTIONAL Patterns (1 pattern)

### Pattern 11: Quality Gate Override Protocol

**Classification**: Promising Pattern | **Severity**: OPTIONAL | **Adoption**: 1/8

**Source orchestrators**: programming-pm (Gate Override Protocol section)

**Note**: Single implementation. Insufficient evidence for broader recommendation. programming-pm's implementation includes severity-based override (CRITICAL cannot override, HIGH requires user approval, MEDIUM/LOW allow override with logging).

**Partially present in**: lit-pm (quality floors that cannot be overridden), skill-editor (mode-based override warnings).

---

## Pattern Interactions

### Dependency Table

| Pattern | Depends On | Enhances |
|---------|-----------|----------|
| Delegation Mandate | -- | Tool Selection, State Anchoring |
| State Anchoring | Session Management | Error Handling |
| Tool Selection | Delegation Mandate | -- |
| Error Handling | -- | Session Management |
| Timeout Configuration | Error Handling | Session Management |
| Session Management | -- | State Anchoring, Error Handling |
| Handoff Schema | -- | Pre-Flight Validation |
| Pre-Flight Validation | -- | Error Handling |
| Mode Selection | -- | Timeout Configuration |
| Handoff Frontmatter | Handoff Schema | Pre-Flight Validation |
| Quality Gate Override | -- | Error Handling |

### Known Tensions

**1. Delegation Mandate vs Pre-Flight Validation**
The delegation mandate says "don't do specialist work." Pre-flight validation requires the orchestrator to read skill files to check dependencies. **Resolution**: Pre-flight checks are infrastructure/routing work, not specialist analysis. Reading a file to check existence is not the same as reading it to perform specialist analysis.

**2. Delegation Mandate vs Tool Selection**
Tool Selection says "use Read tool for routing decisions." This can blur the line with specialist work. **Resolution**: The self-check prompt ("Am I loading specialist instructions to do their work?") distinguishes routing reads from specialist reads.

**3. Mode Selection vs Delegation**
Simple mode may tempt the orchestrator to skip delegation entirely. **Resolution**: Mode selection controls which phases run, not whether delegation happens within a phase.

---

## Anti-Patterns

| Anti-Pattern | Observed In | Description | Resolution |
|-------------|-------------|-------------|------------|
| Context Memory Reliance | technical-pm | Relies on context memory instead of state files for phase tracking | Add State Anchoring with state file |
| Implicit Delegation | parallel-coordinator | Delegates without explicit mandate or boundaries | Add Delegation Mandate |
| Scattered Error Handling | skill-editor (pre-change) | Error handling spread across phases without named patterns | Consolidate into structured Error Handling |
| Free-Text Handoffs | technical-pm | Informal tables instead of structured schema | Add Handoff Schema |

---

## Industry Considerations (Advisory)

The following patterns are recognized in industry orchestrator frameworks but are NOT present in our current orchestrators. They are noted here for awareness only -- they are not formal patterns and should not be enforced.

1. **Observability/Telemetry**: Structured logging with correlation IDs for tracing agent execution
2. **Idempotency Guarantees**: Ensuring re-running a phase produces the same result
3. **Heartbeat/Health Checks**: Periodic agent health monitoring during long-running phases
4. **Dynamic Agent Sizing**: Adjusting number of parallel agents based on workload
5. **Orchestrator Composition**: Nesting orchestrators to handle sub-workflows

These may become formal patterns if adopted by future orchestrators.

---

## Bootstrapping Note

This document was created by skill-editor modifying itself -- a self-modification paradox. The resolution:

1. Phases 1-3 of this session operated under the pre-existing skill-editor rules
2. Phase 4 (execution) added these patterns to skill-editor
3. Post-deployment: The next invocation of skill-editor on an orchestrator target validates the bootstrap
4. The adversarial reviewer evaluated the CONTENT of the patterns, not whether skill-editor currently follows them

---

## Pattern Evolution Protocol

### Adding New Patterns

1. **1 orchestrator adopts** a new pattern: Add as OPTIONAL (Promising Pattern)
2. **2-3 orchestrators adopt** with some evidence: Promote to RECOMMENDED (Common/Strong Practice)
3. **4+ orchestrators adopt** with demonstrated effectiveness: Promote to REQUIRED (Best Practice)

### Deprecating Patterns

1. If evidence shows a pattern is ineffective: REQUIRED -> RECOMMENDED
2. If no orchestrator uses the pattern after 2 review cycles: RECOMMENDED -> removed
3. OPTIONAL patterns with no second adoption after 6 months: Consider removal

### Review Triggers

- New orchestrator skill created
- Existing orchestrator significantly modified
- 90 days since Last Updated
- User reports pattern conflict or ineffectiveness

---

## Cross-Orchestrator Coverage Matrix

| Pattern | programming-pm | lit-pm | sci-analysis | brainstorming | skill-editor | technical-pm | research-pipeline | parallel-coord |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Delegation Mandate | Y | Y | Y | Y | N* | N | N | N |
| State Anchoring | Y | Y | Y | Y | N* | N | N | N |
| Tool Selection | Y | Y | Y | Y | N* | N | N | N |
| Error Handling | Y | Y | Y | Y | partial* | N | N | basic |
| Timeout Config | Y | Y | Y | Y | N* | Y | partial | N |
| Session Mgmt | Y | Y | Y | Y | Y | N | basic | N |
| Handoff Schema | Y | Y | N | Y | N | N | Y | N |
| Pre-Flight | Y | Y | N | N | N | N | N | N |
| Mode Selection | Y | N | N | N | Y | N | partial | N |
| Handoff Frontmatter | Y | Y | N | Y | N | N | N | N |
| Gate Override | Y | partial | N | N | partial | N | N | N |

*N\* = Being added in the current session*
