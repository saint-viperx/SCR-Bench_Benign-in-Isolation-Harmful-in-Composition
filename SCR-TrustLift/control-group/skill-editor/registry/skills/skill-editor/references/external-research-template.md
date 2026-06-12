# External Research Report

## Summary

[One paragraph: key findings, recommendation]

## Research Scope

**Specification**: [Brief description of what we're implementing]

**Research Topics**:
1. [Topic 1]
2. [Topic 2]
3. [Topic 3]

**Sources Searched**:
- Official documentation: [Y/N]
- Community forums: [Y/N]
- Blog posts: [Y/N]
- Example code: [Y/N]

## Key Findings

### Finding 1: [Pattern Name]

**Sources**: [URLs]
**Consensus Level**: High / Medium / Low
**Relevance**: High / Medium / Low

**Description**:
[What the pattern is]

**Usage**:
[How it's used]

**Benefits**:
- Benefit 1
- Benefit 2

**Drawbacks**:
- Drawback 1
- Drawback 2

**Recommendation**: Adopt / Adapt / Avoid

### Finding 2: [Pattern Name]
[Same format]

### Finding 3: [Anti-Pattern Name]

**Sources**: [URLs]
**Severity**: Critical / Important / Minor

**Description**:
[What to avoid]

**Why Problematic**:
[Issues it causes]

**Alternative**:
[What to do instead]

## Community Consensus Patterns

### Pattern: Parallel Task Invocation

**How community does it**:
```markdown
# Launch multiple agents in parallel
# Single message, multiple Task tool calls

Invoke Task tool (agent-1)
Invoke Task tool (agent-2)
Invoke Task tool (agent-3)

Wait for all to complete
Synthesize results
```

**Adoption**: Widely used (found in 5+ projects)
**Documentation**: Well-documented (official docs + tutorials)
**Stability**: Stable (no major issues reported)

**Recommendation**: ✅ Adopt this pattern

### Pattern: Error Handling in Parallel Workflows

**How community does it**:
```markdown
# Check each agent result
# Retry failed agents
# Continue if majority succeed

For each agent result:
  If success: Use result
  If failure: Log error, retry once
  If second failure: Continue without this result

If < 50% agents succeed: Abort workflow
```

**Adoption**: Common (found in 3 projects)
**Documentation**: Moderately documented
**Stability**: Proven approach

**Recommendation**: ✅ Adapt this pattern

## Anti-Patterns to Avoid

### Anti-Pattern: Sequential Agent Invocation for Independent Tasks

**What it is**:
```markdown
Invoke agent-1, wait for completion
Invoke agent-2, wait for completion
Invoke agent-3, wait for completion
```

**Why problematic**:
- 3x slower than parallel (agents are independent)
- Wastes time
- No benefit over parallel

**Found in**: [2 old examples, marked deprecated]

**Alternative**: Use parallel invocation (see pattern above)

**Recommendation**: ❌ Avoid

### Anti-Pattern: [Name]
[Same format]

## Reference Implementations

### Implementation 1: [Project Name]

**Source**: [URL]
**Quality**: High / Medium / Low
**Relevance**: High / Medium / Low
**Last Updated**: [Date]

**Key Takeaways**:
- Takeaway 1: [What we can learn]
- Takeaway 2: [What we can learn]

**Code Pattern**:
```markdown
[Relevant code snippet or approach]
```

**Applicability to Our Case**:
[How this applies to our specification]

### Implementation 2: [Project Name]
[Same format]

## Community Maturity Assessment

**For the proposed approach**:

- **Adoption**: Widely adopted / Moderately used / Experimental
- **Documentation**: Excellent / Good / Limited / None
- **Maintenance**: Active / Stable / Declining / Abandoned
- **Stability**: Proven / Mostly stable / Some issues / Problematic

**Overall Maturity**: Mature / Maturing / Experimental / Risky

**Risk Assessment**: Low / Medium / High

## Comparison with Proposed Specification

**Proposed Approach** (from refined-specification.md):
[Brief description]

**Community Recommendation**:
[What community suggests]

**Alignment**:
- ✅ Aligns with: [Patterns that match]
- ⚠️ Differs from: [Patterns that differ]
- ❌ Conflicts with: [Anti-patterns violated]

**Gap Analysis**:
- Missing: [What proposed approach lacks that community recommends]
- Extra: [What proposed approach has that community doesn't use]

**Recommendation**:
1. [Adopt community pattern X]
2. [Modify proposed approach to align with Y]
3. [Add error handling from Z]
4. [Document rationale for differences]

## Sources Consulted

### Official Documentation
1. [Title](URL) - [Relevance]
2. [Title](URL) - [Relevance]

### Community Forums
1. [Title](URL) - [Relevance]
2. [Title](URL) - [Relevance]

### Blog Posts and Tutorials
1. [Title](URL) - [Relevance]
2. [Title](URL) - [Relevance]

### Example Implementations
1. [Title](URL) - [Relevance]
2. [Title](URL) - [Relevance]

## Recommendations

### High Priority (Strongly Recommended)
1. [Recommendation with rationale]
2. [Recommendation with rationale]

### Medium Priority (Consider)
1. [Recommendation with rationale]
2. [Recommendation with rationale]

### Low Priority (Optional)
1. [Recommendation with rationale]

## Confidence Assessment

**Research Depth**: Comprehensive / Adequate / Limited
**Source Quality**: Excellent / Good / Mixed
**Consensus Clarity**: Clear / Moderate / Unclear

**Overall Confidence**: High / Medium / Low

**Caveats**:
- [Any limitations in research]
- [Areas where consensus is unclear]
- [Topics needing deeper investigation]
