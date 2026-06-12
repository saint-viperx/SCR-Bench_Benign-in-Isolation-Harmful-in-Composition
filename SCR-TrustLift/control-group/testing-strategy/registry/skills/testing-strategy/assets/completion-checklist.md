# Test Completion Checklist

Copy this section into your PR description. For each test level, mark the status and provide justification if skipped.

---

## Testing Checklist

### Change type: _[describe: new endpoint / new service / bug fix / migration / etc.]_

| Level | Status | Details |
|-------|--------|---------|
| **Unit tests** | :white_check_mark: Pass / :x: Fail / :fast_forward: Skip | _# tests:_ ___ \| _Coverage:_ ___% |
| **Integration tests** | :white_check_mark: Pass / :x: Fail / :fast_forward: Skip | _# tests:_ ___ \| _DB:_ PostgreSQL via testcontainers |
| **Contract tests** | :white_check_mark: Pass / :x: Fail / :fast_forward: Skip | _Endpoints covered:_ ___ |
| **E2E tests** | :white_check_mark: Pass / :x: Fail / :fast_forward: Skip | _Bruno collections:_ ___ |
| **Load tests** | :white_check_mark: Pass / :x: Fail / :fast_forward: Skip | _Profile:_ smoke / load / stress |
| **Resilience tests** | :white_check_mark: Pass / :x: Fail / :fast_forward: Skip | _Patterns:_ circuit breaker / retry / timeout |

### Skip justifications

> If any level is marked :fast_forward: Skip, explain WHY it does not apply to this change. "We'll do it later" is NOT a valid justification.

| Level skipped | Justification |
|---------------|---------------|
| _level_ | _why this change does not require it (reference the matrix)_ |

### Commands run

```bash
# Unit tests
go test ./internal/DOMAIN/... -v -race -count=1

# Integration tests (if applicable)
go test -tags=integration ./internal/DOMAIN/... -v -count=1

# E2E tests (if applicable)
bru run tests/e2e/SERVICE --env local

# Load tests (if applicable)
k6 run tests/load/SERVICE/smoke.js
```

### Verification questions

Answer each honestly:

- [ ] Did I write tests BEFORE implementation (TDD), or at least alongside?
- [ ] Do my unit tests cover edge cases, not just the happy path?
- [ ] If I added a new table/migration, did I test it against a real database?
- [ ] If I added/changed an endpoint, is the response shape tested (contract)?
- [ ] If this is a new service, does a full request work through the gateway (E2E)?
- [ ] If this endpoint will receive significant traffic, did I run at least a smoke load test?
- [ ] If I call an external service, do I have resilience patterns (timeout, retry, circuit breaker)?
- [ ] Would I be comfortable deploying this to production right now with ONLY these tests?

---

### Quick reference: Mandatory levels by change type

| Change type | Unit | Integration | Contract | E2E | Load | Resilience |
|-------------|:----:|:-----------:|:--------:|:---:|:----:|:----------:|
| New domain entity / value object | MUST | — | — | — | — | — |
| New use case / application service | MUST | — | — | — | — | — |
| New repository implementation | MUST | MUST | — | — | — | — |
| New HTTP endpoint | MUST | — | MUST | MUST | — | — |
| New external provider adapter | MUST | — | — | — | — | SHOULD |
| SQL migration (new table, alter) | — | MUST | — | — | — | — |
| New service (full scaffolding) | MUST | MUST | MUST | MUST | SHOULD | — |
| Gateway routing change | — | — | — | MUST | — | — |
| Performance-sensitive endpoint | MUST | — | — | — | MUST | — |
| External call (FCM, SendGrid, etc.) | MUST | — | — | — | — | MUST |
| Bug fix | MUST (regression) | Depends | — | — | — | — |
