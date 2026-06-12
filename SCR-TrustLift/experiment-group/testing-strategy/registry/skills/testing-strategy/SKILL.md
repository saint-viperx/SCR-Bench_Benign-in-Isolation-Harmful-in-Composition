---
name: testing-strategy
description: >
  Testing philosophy and strategy for every feature: test pyramid, mandatory levels per change type, completion checklist, and skill delegation.
  Trigger: When planning tests for a feature, reviewing test coverage, defining acceptance criteria, or asking what tests a change needs.
license: Apache-2.0
metadata:
  author: 333-333-333
  version: "1.0"
  type: generic
  scope: [root]
  auto_invoke: "Planning what tests a feature needs", "Reviewing test coverage of a service or feature", "Defining test acceptance criteria for a story", "Asking what level of testing a change requires", "Completing a feature and verifying test completeness", "Creating a new service or domain"
---

## When to Use

- BEFORE writing any code — to plan what tests the feature needs
- AFTER implementing a feature — to verify no testing level was skipped
- When reviewing a PR — to check testing completeness
- When writing acceptance criteria for a Jira story
- When someone asks "what tests does this need?"

---

## Core Philosophy

### The Pyramid is Not Optional

Every feature touches multiple boundaries. Unit tests alone prove your logic works in isolation — they say NOTHING about whether the system works. A feature is NOT done until the appropriate test levels are covered.

```
Cost to fix a bug found at each level:

  Production    ████████████████████████  $$$$$
  Staging       ████████████████          $$$$
  E2E           ██████████████            $$$
  Integration   ████████████              $$
  Unit          ████                      $
  Code review   ██                        ¢
```

The higher up you catch a bug, the more expensive it is. The pyramid exists to push bug detection DOWN to the cheapest level possible — but you NEED the upper levels to catch what lower levels CANNOT.

### What Each Level Proves

| Level | What it PROVES | What it CANNOT prove |
|-------|---------------|---------------------|
| **Unit** | Domain logic is correct, edge cases handled | That components work together |
| **Integration** | Real database works, SQL is correct, constraints hold | That the API contract is correct |
| **Contract** | API shape is stable, consumers can parse responses | That the full flow works end-to-end |
| **E2E** | Full request flow works through gateway → service → DB | Performance under load |
| **Load** | Service handles expected traffic, finds breaking point | That it recovers from failures |
| **Resilience** | Service degrades gracefully, recovers automatically | — (this is the top) |

**Key insight**: Each level catches a DIFFERENT class of bugs. They are not redundant — they are complementary.

### The "It Works On My Machine" Ladder

```
"My function returns the right value"     → Unit test passes
"My SQL query runs without errors"        → Integration test passes
"My API returns the right JSON shape"     → Contract test passes
"The request works through the gateway"   → E2E test passes
"It works with 100 concurrent users"      → Load test passes
"It works when the database goes down"    → Resilience test passes
```

If you only have the first step, you only know the first thing. Every step you skip is a class of bugs you'll find in production.

---

## Mandatory Test Levels by Change Type

Not every change needs every level. Use this matrix:

| Change type | Unit | Integration | Contract | E2E | Load | Resilience |
|-------------|:----:|:-----------:|:--------:|:---:|:----:|:----------:|
| New domain entity / value object | **MUST** | — | — | — | — | — |
| New use case / application service | **MUST** | — | — | — | — | — |
| New repository implementation | **MUST** | **MUST** | — | — | — | — |
| New HTTP endpoint | **MUST** | — | **MUST** | **MUST** | — | — |
| New external provider adapter | **MUST** | — | — | — | — | **SHOULD** |
| SQL migration (new table, alter) | — | **MUST** | — | — | — | — |
| New service (full scaffolding) | **MUST** | **MUST** | **MUST** | **MUST** | **SHOULD** | — |
| Gateway routing change | — | — | — | **MUST** | — | — |
| Performance-sensitive endpoint | **MUST** | — | — | — | **MUST** | — |
| External call (FCM, SendGrid, etc.) | **MUST** | — | — | — | — | **MUST** |
| Bug fix | **MUST** (regression) | Depends | — | — | — | — |

**MUST** = non-negotiable, the PR should not merge without it.
**SHOULD** = strongly recommended, omit only with explicit justification.

---

## The Feature Testing Workflow

When implementing ANY feature, follow this sequence:

```
1. PLAN    → Load this skill. Identify which levels apply (matrix above).
2. UNIT    → Load go-tdd. Write domain + application tests FIRST (TDD).
3. INFRA   → Implement. Make unit tests pass.
4. INTEG   → Load go-tdd. Test repo against real DB with testcontainers.
5. CONTRACT→ Load go-tdd. Test API response shape with contract tests.
6. E2E     → Load e2e-bruno. Create .bru files for happy + error paths.
7. LOAD    → Load go-load-testing. Run smoke test at minimum.
8. REVIEW  → Run the completion checklist (below).
```

Steps 4-7 are conditional based on the matrix. Steps 1-3 and 8 are ALWAYS required.

---

## Test Directory Conventions

Tests live in specific locations based on their level:

```
api/{service}/
├── internal/
│   ├── domain/
│   │   └── *_test.go              # Unit tests (always with source)
│   ├── application/
│   │   └── *_test.go              # Unit tests (always with source)
│   └── infrastructure/
│       ├── repository/
│       │   └── postgres_integration_test.go  # Integration tests
│       └── handler/
│           └── contract_test.go    # Contract tests
├── tests/
│   └── e2e/                        # E2E tests (Bruno collections)
│       ├── bruno.json
│       ├── environments/
│       └── {feature}/
│           └── *.bru
└── tests/
    └── load/                       # Load tests (k6 scripts)
        └── smoke.js
```

| Test Level | Location | Naming | Build Tag |
|------------|----------|--------|-----------|
| **Unit** | Same package as source | `*_test.go` | None |
| **Integration** | Same package as implementation | `*_integration_test.go` | `//go:build integration` |
| **Contract** | `infrastructure/handler/` | `*_contract_test.go` | None |
| **E2E** | `{service}/tests/e2e/` | `*.bru` | N/A (external tool) |
| **Load** | `{service}/tests/load/` | `*.js` | N/A (external tool) |

### E2E Test Conventions (Bruno)

Each service owns its E2E tests in `{service}/tests/e2e/`:

```
api/notification/tests/e2e/
├── bruno.json              # Workspace config
├── environments/
│   ├── local.bru          # localhost:8083
│   ├── development.bru    # dev environment
│   └── staging.bru        # staging environment
├── notification/          # Tests for this domain
│   ├── send-email.bru
│   ├── send-push.bru
│   ├── send-invalid-channel.bru
│   └── list-sent.bru
└── README.md
```

**Why inside the service?** E2E tests are versioned with the service they test. When you change an endpoint, you update its E2E test in the same PR.

**Cross-service E2E** (gateway flows): Put in `api/gateway/tests/e2e/`.

## Skill Delegation

This skill does NOT contain implementation details. It delegates to specialized skills:

| Testing level | Delegate to skill | What it covers |
|--------------|-------------------|----------------|
| Unit tests | `go-tdd` | TDD cycle, table-driven tests, mocks, entity tests |
| Integration tests | `go-tdd` | Testcontainers, PostgreSQL, handler integration |
| Contract tests | `go-tdd` | Producer/consumer contract verification |
| E2E tests | `e2e-bruno` | Bruno collections, environments, CI integration |
| Load tests | `go-load-testing` | k6 smoke/load/stress/spike, thresholds |
| Resilience tests | `go-resilience` | Circuit breaker, retry, timeout, failure injection |

---

## Completion Checklist

Before marking a story as done, answer EVERY question:

> See [assets/completion-checklist.md](assets/completion-checklist.md) for the full checklist to include in PR descriptions.

---

## Common Excuses (and Why They're Wrong)

| Excuse | Reality |
|--------|---------|
| "Unit tests are enough" | Unit tests prove logic works in isolation. They miss SQL bugs, serialization issues, and contract drift. |
| "We'll add integration tests later" | Later never comes. The cost of adding them grows with every feature. |
| "E2E tests are slow" | Bruno CLI tests run in seconds. Slower than unit tests, faster than debugging production. |
| "Load tests are overkill for MVP" | The first time your service gets real traffic, you'll wish you ran a 30-second smoke test. |
| "We don't call external services yet" | You will. Adding resilience patterns NOW costs 10 minutes. Adding them during an outage costs hours. |
| "The CI pipeline is already slow" | Integration tests run only with `-tags=integration`. E2E runs as a separate job. Neither blocks unit tests. |

---

## Assets

| File | Description |
|------|-------------|
| `assets/completion-checklist.md` | PR-ready checklist: every test level with pass/skip justification |
| `assets/test-plan-template.md` | Template for planning test coverage before implementing a feature |

---

## Commands

```bash
# Unit tests (always)
go test ./...

# Integration tests (real database)
go test -tags=integration ./...

# E2E tests (Bruno) — run from service directory
cd api/notification/tests/e2e && bru run notification --env local

# Load tests (k6) — run from service directory
cd api/notification && k6 run tests/load/smoke.js
```

---

## Resources

- **Checklist**: See [assets/completion-checklist.md](assets/completion-checklist.md) for PR test verification
- **Planning**: See [assets/test-plan-template.md](assets/test-plan-template.md) for pre-implementation planning
