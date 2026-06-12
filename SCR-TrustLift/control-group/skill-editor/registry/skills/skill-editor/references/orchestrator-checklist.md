# Orchestrator Best Practices Evaluation Checklist

**Version**: 1.0
**Usage**: Phase 2 agents fill in this checklist when the target skill is detected as an orchestrator.

## Target Information

- **Skill Name**: ___
- **Target Type**: [ ] New orchestrator | [ ] Existing orchestrator modification
- **Architecture Type**: [ ] Phase-based | [ ] Stage-based | [ ] Event-driven | [ ] Other: ___

---

## REQUIRED Patterns (evaluated by best-practices-reviewer)

| # | Pattern | Status | Evidence |
|---|---------|--------|----------|
| 1 | Delegation Mandate | [ ] PRESENT [ ] PARTIAL [ ] ABSENT | _citation_ |
| 2 | State Anchoring | [ ] PRESENT [ ] PARTIAL [ ] ABSENT | _citation_ |
| 3 | Tool Selection Table | [ ] PRESENT [ ] PARTIAL [ ] ABSENT | _citation_ |
| 4 | Error Handling (Structured) | [ ] PRESENT [ ] PARTIAL [ ] ABSENT | _citation_ |
| 5 | Timeout Configuration | [ ] PRESENT [ ] PARTIAL [ ] ABSENT | _citation_ |
| 6 | Session Management | [ ] PRESENT [ ] PARTIAL [ ] ABSENT | _citation_ |

**REQUIRED Score**: ___/6

---

## RECOMMENDED Patterns (evaluated by knowledge-engineer)

| # | Pattern | Status | Evidence |
|---|---------|--------|----------|
| 7 | Handoff Schema | [ ] PRESENT [ ] PARTIAL [ ] ABSENT [ ] N/A | _citation_ |
| 8 | Pre-Flight Validation | [ ] PRESENT [ ] PARTIAL [ ] ABSENT [ ] N/A | _citation_ |
| 9 | Mode Selection | [ ] PRESENT [ ] PARTIAL [ ] ABSENT [ ] N/A | _citation_ |
| 10 | Handoff Frontmatter | [ ] PRESENT [ ] PARTIAL [ ] ABSENT [ ] N/A | _citation_ |

**RECOMMENDED Score**: ___/4 (excluding N/A)

N/A is valid when an architectural mismatch exists (e.g., event-driven orchestrator lacks sequential phases for Mode Selection).

---

## OPTIONAL Patterns (noted but not scored)

| # | Pattern | Status | Notes |
|---|---------|--------|-------|
| 11 | Quality Gate Override | [ ] PRESENT [ ] ABSENT | _optional notes_ |

---

## Assessment Rubric

| Level | Criteria |
|-------|----------|
| **Exemplary** | 6/6 REQUIRED AND 3+/4 RECOMMENDED |
| **Strong** | 6/6 REQUIRED AND 1-2/4 RECOMMENDED |
| **Adequate** | 6/6 REQUIRED AND 0/4 RECOMMENDED |
| **Needs Improvement** | 4-5/6 REQUIRED |
| **Critical Gaps** | <4/6 REQUIRED |

**Overall Assessment**: ___

---

## Notes

- For **existing orchestrators**: PARTIAL with a working variant is acceptable. Do NOT recommend replacing working implementations with standard templates unless the variant has known issues.
- For **new orchestrators**: ABSENT REQUIRED patterns should be flagged for inclusion in the implementation plan.
- **Sanity check**: If 0/6 REQUIRED patterns are present, reconsider whether the target is actually an orchestrator. This may indicate a false positive in detection.
- **Evidence citations**: One sentence per pattern citing the specific section, line range, or feature that demonstrates presence/absence.
