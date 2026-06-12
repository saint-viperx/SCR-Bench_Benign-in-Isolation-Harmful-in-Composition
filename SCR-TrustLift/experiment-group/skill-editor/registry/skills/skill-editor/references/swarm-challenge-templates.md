# Swarm Challenge Template: Skill Analysis

Pre-written challenge template for brainstorming-pm swarm invocation in the
skill-editor Phase 2 analysis. The template injects concrete skill parameters
to force the swarm perspectives to engage with specific skill-editing trade-offs
rather than producing generic advice.

**Usage**: The orchestrator reads this template, fills in the placeholder
variables `{...}` with values from the refined specification and any existing
skill content, then passes the filled template as the challenge to
brainstorming-pm via the Task tool.

**Swarm invocation**: FULL mode only. QUICK mode skips all swarm steps.

---

## Challenge Template

```
CHALLENGE: Comprehensive Analysis of Proposed Skill Change

Skill: {skill_name}
Change type: {change_type} (new skill / modification / refactoring)
Files affected: {file_count}
Estimated lines changed: {line_count}
Is orchestrator: {is_orchestrator} (true/false)

## Specification Summary
{refined_specification_summary}

## Current Skill Structure (if modifying existing skill)
{current_skill_summary}

## Analysis Required

Evaluate this proposed change from multiple angles:

1. **Anthropic best practices compliance**
   - Does it follow Claude Code skill conventions? (Clear instructions, measurable
     criteria, proper tool usage, no anti-patterns)
   - Does it align with the skill structure specification?
     (YAML frontmatter, required sections, naming conventions)

2. **Structural completeness**
   - What structural gaps exist when compared to professional standards?
     (Program management, software engineering, knowledge management frameworks)
   - Are there missing error handling paths, edge cases, or validation steps?

3. **Community patterns and prior art**
   - What existing patterns in this repository or community could inform the approach?
   - Are there similar skills that solved comparable problems?

4. **Architectural implications**
   - How does this change affect the broader skill ecosystem?
   - Does it introduce coupling, duplication, or maintenance burden?
   - For orchestrators: does it follow the orchestrator-best-practices patterns?

## Quality Threshold

Output must contain:
- At least 2 specific, actionable recommendations with rationale
- At least 1 concrete alternative approach
- Evidence-based assessment (not generic advice)
- Confidence levels on key claims
```

## Context Injection Checklist

Before filling the template, the orchestrator must have:
- [ ] Skill name from refined specification
- [ ] Change type classification (new / modification / refactoring)
- [ ] File count and estimated line count from specification
- [ ] Orchestrator detection result from session state
- [ ] Specification summary (copy objective + scope from refined-specification.md)
- [ ] Current skill summary (if modifying: read first 50 lines of existing SKILL.md)

## Quality Threshold

The swarm synthesis must contain:
- At least 2 specific, actionable recommendations (not generic "follow best practices")
- At least 1 concrete alternative approach with trade-off analysis
- Confidence-weighted convergent insights from 2+ perspectives
- Divergent insights attributed to originating archetype

If the synthesis falls below this threshold, log the shortfall and proceed
without swarm input (graceful degradation).

## Timeout and Graceful Degradation

- brainstorming-pm timeout: 15 minutes
- On timeout: Skip swarm; proceed with edge-case-simulator output only
- Missing brainstorming-pm skill: Skip swarm steps entirely
- Below quality threshold: Log and proceed without swarm input
