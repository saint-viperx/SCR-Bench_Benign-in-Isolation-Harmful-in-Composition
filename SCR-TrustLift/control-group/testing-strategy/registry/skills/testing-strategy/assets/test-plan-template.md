# Test Plan: [Feature / Story Name]

> Fill this out BEFORE writing any code. It forces you to think about what tests the feature needs before you start implementing.

---

## 1. Feature summary

**Jira story**: SCRUM-___
**Service**: `api/___/`
**Domain**: `internal/___/`

**What does this feature do?**
> _One paragraph describing the feature and its boundaries._

---

## 2. Change inventory

List every file you expect to create or modify:

| File | Change type | Test level required |
|------|-------------|-------------------|
| `internal/DOMAIN/domain/entity.go` | New domain entity | Unit |
| `internal/DOMAIN/domain/value_object.go` | New value objects | Unit |
| `internal/DOMAIN/application/service.go` | New use case | Unit |
| `internal/DOMAIN/infrastructure/repository/postgres.go` | New repository impl | Unit + Integration |
| `internal/DOMAIN/infrastructure/handler/http.go` | New endpoint | Unit + Contract + E2E |
| `migrations/000XXX_create_TABLE.up.sql` | New migration | Integration |
| _add more as needed_ | | |

---

## 3. Test plan by level

### Unit tests (go-tdd skill)

| Test file | What it tests | Key scenarios |
|-----------|--------------|---------------|
| `domain/entity_test.go` | Entity creation + behavior | Valid creation, invalid state transitions, edge cases |
| `domain/value_object_test.go` | Value object validation | Valid values, invalid values, boundary values |
| `application/service_test.go` | Use case logic | Happy path, domain errors, repository errors |

**Estimated count**: ___ tests

### Integration tests (go-tdd skill)

| Test file | What it tests | Infrastructure needed |
|-----------|--------------|----------------------|
| `infrastructure/repository/postgres_test.go` | Repository against real DB | PostgreSQL (testcontainers) |

**Applies?** Yes / No
**If no, why?** ___

### Contract tests (go-tdd skill)

| Endpoint | Method | Response shape to verify |
|----------|--------|--------------------------|
| `/api/v1/RESOURCE` | POST | `{"data": {"id": "...", ...}}` |
| `/api/v1/RESOURCE` | GET | `{"data": [...]}` |

**Applies?** Yes / No
**If no, why?** ___

### E2E tests (e2e-bruno skill)

| Bruno file | Scenario | Expected status |
|------------|----------|-----------------|
| `create-success.bru` | Happy path creation | 201 |
| `create-validation-error.bru` | Missing required fields | 400 |
| `create-duplicate.bru` | Duplicate resource | 409 |

**Applies?** Yes / No
**If no, why?** ___

### Load tests (go-load-testing skill)

| Script | Profile | Thresholds |
|--------|---------|------------|
| `smoke.js` | 1 VU, 30s | p95 < 500ms, errors < 1% |

**Applies?** Yes / No
**If no, why?** ___

### Resilience tests (go-resilience skill)

| Pattern | Where it applies | Failure scenario |
|---------|-----------------|------------------|
| Circuit breaker | External service call | Service returns 500 |
| Retry with backoff | Transient network errors | Connection timeout |
| Timeout | All external calls | Slow response > 5s |

**Applies?** Yes / No
**If no, why?** ___

---

## 4. Test execution order

```
1. [ ] Write domain unit tests (TDD red phase)
2. [ ] Implement domain layer (TDD green phase)
3. [ ] Write application unit tests (TDD red phase)
4. [ ] Implement application layer (TDD green phase)
5. [ ] Write infrastructure unit tests
6. [ ] Implement infrastructure layer
7. [ ] Write integration tests (repository against real DB)
8. [ ] Run integration tests, fix any SQL/constraint issues
9. [ ] Write contract tests (API response shape)
10. [ ] Write E2E Bruno collections
11. [ ] Run E2E through gateway
12. [ ] Write load smoke test
13. [ ] Run load test, verify thresholds
14. [ ] Add resilience patterns if external calls exist
15. [ ] Run completion checklist
```

---

## 5. Risks and open questions

| Risk / Question | Impact | Mitigation |
|----------------|--------|------------|
| _e.g., "No staging DB available yet"_ | Cannot run integration tests in CI | Run locally, add CI job later |
| _e.g., "External API rate limits unknown"_ | Load test may hit limits | Start with smoke profile only |

---

## 6. Definition of done

- [ ] All MUST-level tests from the matrix pass
- [ ] All SHOULD-level tests pass OR have documented justification
- [ ] Test coverage is measured and reported
- [ ] Completion checklist is included in the PR description
- [ ] All tests run in CI (or have a tracking issue for CI integration)
