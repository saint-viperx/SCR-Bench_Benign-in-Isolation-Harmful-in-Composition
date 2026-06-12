# Strategic Review Report Template

Use this template when writing /tmp/skill-editor-session/strategic-review.md

---

# Strategic Review: [Change Title]

**Date**: [YYYY-MM-DD]
**Complexity Level**: [Simple/Medium/Complex]
**Classification**: [MINOR ONLY / MAJOR REFACTORING DETECTED]
**Confidence**: [High/Medium/Low]

---

## Executive Summary

[2-3 paragraphs summarizing]:
- Architectural assessment (does structure match problem type?)
- Key findings (patterns identified, mismatches detected)
- Classification (minor improvements only, or major refactoring opportunity)
- Recommendation (proceed as-is, proceed with modifications, or explore alternatives)

---

## Architectural Assessment

### Problem Type Analysis

What type of problem is this?
- [Workflow extension / New capability / Architectural change / Performance optimization / etc.]

### Current Approach Analysis

What architectural approach does the specification propose?
- Pattern: [e.g., Sequential workflow / Parallel execution / Hierarchical coordination / etc.]
- Rationale: [Why was this approach chosen?]

### Architectural Fit

Does the proposed structure match the problem type?
- **Fit assessment**: [Good fit / Partial fit / Mismatch]
- **Reasoning**: [Why does it fit or not?]

---

## Pattern Analysis

### Pattern 1: [Domain Name - e.g., Program Management]

**Source**: [PMI PMBOK / Stage-Gate / etc.]

**Pattern description**: [Brief description of the pattern]

**Resemblance to proposed approach**:
- Similarities: [What matches?]
- Differences: [What doesn't match?]
- Applicability: [How relevant is this pattern?]

**Insight**: [What does this pattern tell us about the proposed approach?]

---

### Pattern 2: [Domain Name - e.g., Software Engineering]

[Same structure as Pattern 1]

---

### Pattern 3: [Domain Name - Optional]

[Same structure as Pattern 1]

---

## Recommendations

### Minor Improvements (Non-Blocking)

These recommendations can be integrated into the current plan without architectural changes:

1. **[Recommendation Title]**
   - **What**: [Brief description]
   - **Why**: [Rationale from pattern analysis]
   - **How**: [Specific implementation guidance]
   - **Expected benefit**: [Quantified if possible: 20-30% improvement, etc.]
   - **Priority**: [High/Medium/Low]

2. **[Recommendation Title]**
   [Same structure]

---

### Major Refactoring Opportunity (Go/No-Go Decision)

[Only include this section if major refactoring detected]

**Issue**: [Describe fundamental architectural mismatch or deficiency]

**Severity**: [Critical/High/Medium - use criteria from agent definition]

**Current Approach Assessment**:
- **Pros**: [What works with current approach?]
- **Cons**: [What are the fundamental issues?]
- **Risk**: [What's the likelihood of failure or technical debt?]

**Alternative Approach**:
- **Pattern basis**: [Which cross-domain pattern suggests this?]
- **Description**: [High-level description of alternative]
- **Pros**: [Advantages of alternative]
- **Cons**: [Trade-offs and challenges]
- **Estimated effort**: [Rough comparison: 2x current estimate, etc.]

**Recommendation**: [Proceed with current / Explore alternative in parallel / Abort and reconsider]

**User decision required**: [Reference that go/no-go decision was presented to user]

---

## Confidence Assessment

**Overall confidence in this assessment**: [High/Medium/Low]

**Factors affecting confidence**:
- [e.g., Limited external research due to WebSearch unavailable]
- [e.g., Novel architectural approach without many comparable patterns]
- [e.g., High confidence - multiple corroborating sources from different domains]

**Areas needing deeper investigation** (if confidence is Medium/Low):
- [List specific questions that remain unresolved]
- [Suggest additional research or expert consultation if needed]

---

## Integration Notes for decision-synthesizer

**How to use this strategic perspective**:

1. **If MINOR ONLY**: Integrate recommendations into implementation plan as enhancements. No workflow changes needed.

2. **If MAJOR REFACTORING DETECTED**:
   - User made decision: [Proceed with current / Explore in parallel / Aborted]
   - If "Explore in parallel": Launch Track 2 after Phase 3 completion
   - If "Proceed with current": Note alternative available in implementation plan

3. **Priority for conflict resolution**: Strategy consultant has authority on architectural approach (top-down), knowledge-engineer has authority on structural completeness (bottom-up)

4. **Key architectural guidance**: [1-2 sentences summarizing most important strategic insight]

---

## References

**Internal sources**:
- [List files from claude-config that were analyzed]

**External sources**:
- [List WebSearch sources, academic papers, frameworks referenced]
- [Format: Title - URL or Citation]

---

## Appendix: Detailed Analysis (Optional)

[Include if detailed case studies, extended pattern analysis, or risk assessments are relevant and space permits]

### Case Study: [Example from other domain]

[Description of how similar problem was solved in other field]

---

**End of Template**
