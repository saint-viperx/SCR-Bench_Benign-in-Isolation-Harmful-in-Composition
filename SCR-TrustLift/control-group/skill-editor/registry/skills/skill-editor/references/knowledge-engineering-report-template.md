# Knowledge Engineering Analysis Report

> **Usage Guidance**: This template structures the knowledge-engineering analysis report. Include all Required sections. Optional sections can be omitted if time constrained.

## Executive Summary

[2-3 sentences: Primary domains identified, completeness score, key gaps]

**Completeness Score**: X% (Y required elements present out of Z total)
**Primary Domains**: [List 2-3 most relevant]
**Critical Gaps**: [Count]
**High Priority Recommendations**: [Count]

---

## Domain Classification

**Primary Domain(s)**: [Main framework that applies]
**Secondary Domain(s)**: [Supporting frameworks, if any]

**Rationale**:
[Why these domains were selected based on workflow characteristics. Be specific about which workflow elements triggered domain selection.]

**Confidence in Classification**: High / Medium / Low

---

## Completeness Assessment by Domain

### [Domain 1]: [Name] (e.g., Program Management - PMBOK)

**Required Elements**: [Count]
**Present in Specification**: [Count] ([List them])
**Missing from Specification**: [Count] ([List them])
**Completeness Score**: [Present / Required] = X%

#### Gap Analysis

**Gap 1: Missing [Element Name]**
- **Standard Practice**: [How this domain defines this requirement]
- **Why Required**: [Purpose and value]
- **Impact if Missing**: [Severity: Critical/High/Medium/Low] - [Specific consequences]
- **Found in Current Spec**: Yes / No / Partial
- **Recommendation**: [Specific addition with example]

**Gap 2: Missing [Element Name]**
- **Standard Practice**: [Domain requirement]
- **Why Required**: [Purpose]
- **Impact if Missing**: [Severity] - [Consequences]
- **Found in Current Spec**: Yes / No / Partial
- **Recommendation**: [Specific addition]

[Continue for all gaps in this domain]

### [Domain 2]: [Name]

[Same structure as Domain 1]

### [Domain 3]: [Name] (if applicable)

[Same structure]

---

## Cross-Domain Pattern Analysis

> **Purpose**: Identify patterns that appear across multiple domains and assess presence in specification.

### Pattern 1: [Pattern Name]

**Observed in Domains**:
- **[Domain 1]**: [How they implement this pattern]
- **[Domain 2]**: [How they implement this pattern]
- **[Domain 3]**: [How they implement this pattern]

**Core Principle**:
[The transferable insight that works across all domains - the "why" behind the pattern]

**Application to This Specification**:
[How this pattern would apply to the proposed workflow]

**Current State**:
- **Present**: [What exists that relates to this pattern]
- **Missing**: [What's absent]

**Recommendation**:
[Specific addition with example implementation]

**Example Implementation**:
```markdown
[Concrete code or structural example of how to add this]
```

**Priority**: Critical / High / Medium / Low
**Effort**: High / Medium / Low
**Affected Domains**: [Which domains require this]

### Pattern 2: [Name]

[Same format as Pattern 1]

### Pattern 3: [Name]

[Same format - include 2-3 key patterns total]

---

## Required Field Analysis

> **Purpose**: Identify missing metadata, fields, or structural elements based on domain standards.

### Missing Critical Fields

**Field: [Name]**
- **Found in**: [Which domains require this field]
- **Standard Format**: [How it's typically structured in those domains]
- **Necessity**: Required for [type of workflow]
- **Impact if Missing**: [What problems this causes]
- **Current State**: Not present / Partial / [description]
- **Recommendation**: [How to add, where to add]

**Example Implementation**:
```markdown
[Concrete example of how to add this field to the specification]
```

**Field: [Name]**
[Repeat for each critical field]

### Missing Recommended Fields

[Same format as critical fields, but these are High priority, not Critical]

### Missing Optional Fields

[Same format, but these are nice-to-have, not required]

---

## Structural Gaps

> **Purpose**: Identify missing workflows, phases, protocols, or structural components.

### Gap 1: [Gap Name]

**Domain Standards**:
- **[Domain 1]**: [What they require for this]
- **[Domain 2]**: [What they require for this]
- **[Domain 3]**: [What they require for this]

**Why This Matters**:
[Impact and rationale - explain the value]

**Current State**:
[What exists now regarding this gap - be specific]

**Recommendation**:
[Specific implementation guidance]

**Example**:
```markdown
[Code or structural example of recommended implementation]
```

**Priority**: Critical / High / Medium / Low
**Effort**: High / Medium / Low

### Gap 2: [Name]

[Same format]

[Continue for all structural gaps]

---

## Completeness Metrics

### Quantitative Assessment

**Overall Completeness**: X%

**By Category**:
| Category | Required | Present | Missing | Score |
|----------|----------|---------|---------|-------|
| Identity | X | Y | Z | W% |
| Descriptive | X | Y | Z | W% |
| Relationships | X | Y | Z | W% |
| Quality/Risk | X | Y | Z | W% |
| Operational | X | Y | Z | W% |
| Documentation | X | Y | Z | W% |
| **TOTAL** | **X** | **Y** | **Z** | **W%** |

### Qualitative Assessment (Wang & Strong Framework)

**Intrinsic Quality**: [High/Medium/Low]
- **Accuracy**: [Assessment with rationale]
- **Objectivity**: [Are criteria measurable? Assessment]
- **Believability**: [Are claims credible? Assessment]

**Contextual Quality**: [High/Medium/Low]
- **Relevance**: [Does this address user's need? Assessment]
- **Completeness**: [X%] [Explanation of score]
- **Timeliness**: [Is information current? Assessment]
- **Appropriate Amount**: [Right level of detail? Assessment]

**Representational Quality**: [High/Medium/Low]
- **Interpretability**: [Can others understand? Assessment]
- **Format**: [Follows standards? Assessment]
- **Coherence**: [Internally consistent? Assessment]

**Accessibility Quality**: [High/Medium/Low]
- **Accessibility**: [Can stakeholders find needed info? Assessment]

---

## Recommendations

> **Purpose**: Prioritized list of additions to improve structural completeness.

### Critical Additions (Blocking - MUST Add)

1. **[Recommendation Title]**
   - **Rationale**: [Why this is critical, which domains require it]
   - **Impact**: [What happens without it - be specific]
   - **Implementation**: [How to add it, where to add it]
   - **Effort**: High / Medium / Low
   - **Affected Domains**: [List of domains requiring this]
   - **Example**:
     ```markdown
     [Concrete implementation example]
     ```

2. **[Recommendation Title]**
   [Same format]

[Continue for all critical recommendations]

### High Priority Additions (Strongly Recommended)

1. **[Recommendation Title]**
   - **Rationale**: [Why this is important]
   - **Impact**: [Benefits of adding it]
   - **Implementation**: [How to add it]
   - **Effort**: High / Medium / Low
   - **Affected Domains**: [List]

[Continue for all high-priority recommendations]

### Medium Priority Additions (Should Consider)

1. **[Recommendation Title]**
   - **Rationale**: [Why useful]
   - **Impact**: [Benefits]
   - **Implementation**: [How to add]
   - **Effort**: High / Medium / Low

### Optional Enhancements (Nice to Have)

1. **[Recommendation Title]**
   - **Rationale**: [Best practice rationale]
   - **Impact**: [Marginal benefits]
   - **Implementation**: [How to add]
   - **Effort**: High / Medium / Low

---

## Domain-Specific Insights

> **Optional Section**: Include if time permits. Provides deeper domain-specific context.

### From Program Management

[Key insights about how PM frameworks (PMBOK, PgMP, PMI) would structure this workflow]
[Specific recommendations drawn from PM standards]

### From Supply Chain Management

[Key insights about coordination, orchestration, and exception handling from SCOR model]
[Specific recommendations drawn from supply chain patterns]

### From Software Engineering

[Key insights about quality gates, testing, deployment from SDLC/DevOps/Agile]
[Specific recommendations drawn from software practices]

### From Consulting Methodology

[Key insights about decision-making, synthesis, recommendations from McKinsey/BCG/Bain]
[Specific recommendations drawn from consulting frameworks]

### From Systems Architecture

[Key insights about component design, integration, resilience]
[Specific recommendations drawn from enterprise architecture]

### From Knowledge Management

[Key insights about information quality, completeness, knowledge capture]
[Specific recommendations drawn from KM frameworks]

---

## Comparison with Industry Standards

> **Optional Section**: Include if applicable standards exist.

**Standard**: [Name of relevant standard/framework]
**Source**: [e.g., PMBOK 7th Edition, SCOR Model v13, ISO 9001]
**Version**: [Specify version]
**Applicability**: [Why this standard is relevant to this specification]

**Alignment Analysis**:
- ✅ **Aligns with**: [Elements in specification matching this standard]
- ⚠️ **Partially aligns**: [Elements partially matching, with gaps noted]
- ❌ **Missing from standard**: [Required elements from standard that are absent]

**Compliance Level**: [Percentage or qualitative assessment]

**Standard**: [Another relevant standard]
[Same format]

---

## Knowledge Transfer Examples

> **Optional Section**: Include 1-2 examples if helpful for illustration.

### Example 1: How [Domain] Solves [Problem]

**Domain**: [e.g., Incident Response]
**Problem**: [e.g., Multi-agent coordination under time pressure]

**Their Solution**:
- [Element 1 of their approach]
- [Element 2 of their approach]
- [Element 3 of their approach]

**Why It Works**:
[Core principle that makes this effective]

**Transfer to This Specification**:
- [How to adapt element 1]
- [How to adapt element 2]
- [How to adapt element 3]

**Concrete Recommendation**:
[Specific change to make in the specification]

### Example 2: [Domain] Approach to [Problem]

[Same format]

---

## Confidence Assessment

**Analysis Depth**: Comprehensive / Adequate / Limited
**Domain Coverage**: [List all domains analyzed: 2-3 expected]
**Pattern Matching Confidence**: High / Medium / Low

**Strengths of This Analysis**:
- [What was thoroughly covered]
- [High-confidence areas]
- [Reliable findings]

**Limitations**:
- [Any gaps in analysis - be honest]
- [Domains not considered that might apply]
- [Areas of uncertainty]
- [Time constraints if applicable]

**Additional Research Recommended**:
- [Topic 1 needing deeper investigation, if any]
- [Topic 2 needing deeper investigation, if any]

---

## Integration Notes for Decision-Synthesizer

> **Required Section**: Critical for downstream integration.

**Relationship to Other Analyses**:
- **Best-Practices Review**: [How this complements Anthropic guidelines analysis]
- **External Research**: [How this complements community patterns]
- **Edge-Case Analysis**: [How this complements failure mode analysis]

**Your Distinct Contribution**: Structural completeness assessment from professional domain standards

**Key Handoff Points**:
1. **Critical gaps** identified in this report MUST be addressed in implementation plan
2. **High-priority recommendations** SHOULD be considered in final plan
3. **Cross-domain patterns** provide alternative implementation approaches
4. **Completeness metrics** can inform quality gate criteria

**Potential Conflicts**:
- [Areas where structural completeness might conflict with simplicity - note trade-offs]
- [Areas where domain standards might conflict with Anthropic guidelines - Anthropic wins]
- [Areas where thoroughness might conflict with pragmatism - note balance]

**Conflict Resolution Guidance**:
- **Structure vs. Simplicity**: Start with essential structural elements, make detailed elements optional
- **Domain Standards vs. Anthropic Guidelines**: Anthropic guidelines win for prompt design, domain standards win for workflow structure
- **Required Fields vs. YAGNI**: Mark as Critical if needed now, document others as future enhancements

**Synthesis Recommendations**:
[Specific guidance for decision-synthesizer on how to integrate this analysis with others]

---

## Appendix: Framework References

> **Optional Section**: Include if specific frameworks cited.

### PMBOK (Project Management Body of Knowledge)
- **Version**: [e.g., 7th Edition, 2021]
- **Relevant Sections**: [List sections referenced]
- **Key Concepts Applied**: [List concepts used in analysis]

### SCOR Model (Supply Chain Operations Reference)
- **Version**: [e.g., Version 13.0]
- **Relevant Processes**: [List processes referenced]
- **Key Concepts Applied**: [List concepts used]

### [Other Frameworks Used]
[Same format for each framework cited]

---

## Glossary of Domain Terms

> **Optional Section**: Include if domain-specific terminology used.

**[Term 1]**: [Definition in context of this analysis]

**[Term 2]**: [Definition in context of this analysis]

**[Term 3]**: [Definition in context of this analysis]

---

**Report Generated**: [Timestamp]
**Analysis Duration**: [Time taken]
**Analyst**: skill-editor-knowledge-engineer (Claude Opus 4.6)
