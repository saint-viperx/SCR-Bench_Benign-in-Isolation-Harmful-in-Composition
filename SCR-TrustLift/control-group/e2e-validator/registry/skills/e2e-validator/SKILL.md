---
name: e2e-validator
description: >
  This skill should be used when the work type is FRONTEND and visual verification
  is needed. Provides browser automation for screenshot comparison, responsive
  testing, and interactive element verification using Playwright or Puppeteer.
---

# E2E Browser Automation Skill

Visual verification of frontend changes using browser automation.

## Anthropic Best Practice

From "Code Execution with MCP": Use browser automation to visually verify frontend
implementations, catch visual regressions, and ensure interactive elements work.

## When to Use

This skill is automatically invoked when:
- `work_type == FRONTEND` in auto-context.yaml
- Task involves UI components
- Visual verification is required

## Prerequisites

Check project profile for browser automation setup:

```yaml
# .claude/project-profile.yaml
e2e:
  framework: playwright  # or puppeteer
  config_path: playwright.config.ts
  base_url: http://localhost:3000
```

## Browser Automation Protocol

### Step 1: Start Development Server

```bash
# Start the dev server in background
npm run dev &
DEV_PID=$!

# Wait for server to be ready
npx wait-on http://localhost:3000 --timeout 60000
```

### Step 2: Launch Browser

```typescript
// Playwright
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// Puppeteer
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
```

### Step 3: Navigate and Screenshot

```typescript
// Navigate to the component/page
await page.goto('http://localhost:3000/dashboard');

// Wait for content to load
await page.waitForSelector('[data-testid="dashboard"]');

// Take screenshot
await page.screenshot({
  path: '.claude/screenshots/dashboard.png',
  fullPage: true
});
```

## Screenshot Comparison

### Baseline Management

```
.claude/
  screenshots/
    baseline/          # Reference screenshots
      dashboard.png
      login.png
    current/           # Current run screenshots
      dashboard.png
      login.png
    diff/              # Visual differences
      dashboard-diff.png
```

### Comparison Output

```
┌─────────────────────────────────────────────────────────────┐
│ Visual Comparison Results                                   │
│                                                             │
│   Page: /dashboard                                          │
│   Baseline: .claude/screenshots/baseline/dashboard.png      │
│   Current: .claude/screenshots/current/dashboard.png        │
│                                                             │
│   Pixel difference: 0.5%                                    │
│   Threshold: 1%                                             │
│   Status: ✅ PASS                                           │
└─────────────────────────────────────────────────────────────┘
```

## Responsive Testing

Test at multiple viewport sizes:

```typescript
const viewports = [
  { width: 375, height: 667, name: 'mobile' },    // iPhone SE
  { width: 768, height: 1024, name: 'tablet' },   // iPad
  { width: 1280, height: 800, name: 'desktop' },  // Laptop
  { width: 1920, height: 1080, name: 'wide' },    // Wide monitor
];

for (const viewport of viewports) {
  await page.setViewportSize({ width: viewport.width, height: viewport.height });
  await page.screenshot({
    path: `.claude/screenshots/${viewport.name}-dashboard.png`
  });
}
```

### Responsive Output

```
┌─────────────────────────────────────────────────────────────┐
│ Responsive Testing Results                                  │
│                                                             │
│   Page: /dashboard                                          │
│                                                             │
│   ✅ mobile (375x667)                                       │
│   ✅ tablet (768x1024)                                      │
│   ✅ desktop (1280x800)                                     │
│   ✅ wide (1920x1080)                                       │
│                                                             │
│   All viewports rendered correctly.                         │
└─────────────────────────────────────────────────────────────┘
```

## Interactive Element Testing

Test buttons, forms, and interactions:

```typescript
// Test button click
await page.click('[data-testid="submit-button"]');
await page.waitForSelector('[data-testid="success-message"]');

// Test form submission
await page.fill('[data-testid="email-input"]', 'test@example.com');
await page.fill('[data-testid="password-input"]', 'password123');
await page.click('[data-testid="login-button"]');
await page.waitForNavigation();

// Verify navigation
expect(page.url()).toBe('http://localhost:3000/dashboard');
```

## Report Format

```markdown
## E2E Validation Report

### Summary
Visual verification complete for 5 pages across 4 viewports.

### Screenshots Captured
| Page | Mobile | Tablet | Desktop | Wide |
|------|--------|--------|---------|------|
| /login | ✅ | ✅ | ✅ | ✅ |
| /dashboard | ✅ | ✅ | ✅ | ✅ |
| /profile | ✅ | ✅ | ✅ | ✅ |
| /settings | ✅ | ✅ | ✅ | ✅ |
| /404 | ✅ | ✅ | ✅ | ✅ |

### Visual Differences
No visual regressions detected.

### Interactive Tests
| Test | Status |
|------|--------|
| Login form submission | ✅ PASS |
| Navigation menu toggle | ✅ PASS |
| Modal open/close | ✅ PASS |

### Screenshot Locations
All screenshots saved to `.claude/screenshots/current/`
```

## Integration with Parallel Orchestrator

When FRONTEND work type is detected, add e2e step after QA:

```yaml
# In parallel-orchestrator workflow
steps:
  - task_executor (TDD cycle)
  - qa_agent (independent verification)
  - e2e_validator (visual verification)  # Added for FRONTEND
  - integration (merge)
```

## Error Handling

### Dev Server Won't Start

```bash
# Check if port is in use
lsof -i :3000

# Kill existing process
kill $(lsof -t -i:3000)

# Retry
npm run dev &
```

### Screenshot Timeout

```typescript
// Increase timeout for slow pages
await page.waitForSelector('[data-testid="content"]', { timeout: 30000 });
```

### Visual Diff Too High

If pixel difference > threshold:
1. Check if change is intentional
2. If yes, update baseline
3. If no, investigate visual regression

## Cleanup

```bash
# Stop dev server
kill $DEV_PID

# Close browser
await browser.close();

# Archive screenshots
mv .claude/screenshots/current/* .claude/screenshots/archive/$(date +%Y%m%d)/
```

## Accessibility Testing (WCAG 2.1 AA)

Automated accessibility testing using axe-core.

### Why Accessibility Matters

- Legal compliance (ADA, Section 508)
- Better UX for all users
- SEO benefits
- Larger potential audience

### Setup

```bash
# Install axe-core for Playwright
npm install -D @axe-core/playwright
```

### Accessibility Test Protocol

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('should have no accessibility violations', async ({ page }) => {
  await page.goto('http://localhost:3000/dashboard');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### WCAG 2.1 AA Checks

| Category | What's Checked |
|----------|----------------|
| **Perceivable** | Alt text, color contrast, text resize |
| **Operable** | Keyboard navigation, focus visible, no seizures |
| **Understandable** | Labels, error messages, consistent UI |
| **Robust** | Valid HTML, ARIA usage |

### Common Violations

| Violation | Impact | Fix |
|-----------|--------|-----|
| Missing alt text | Critical | Add `alt` to all `<img>` |
| Low color contrast | Serious | Increase contrast ratio to 4.5:1 |
| Missing form labels | Serious | Add `<label>` or `aria-label` |
| Missing skip link | Moderate | Add skip to main content link |
| No focus indicator | Serious | Add `:focus` styles |

### Accessibility Report Format

```markdown
## Accessibility Report

### Summary
- **Pages tested:** 5
- **Total violations:** 3
- **Critical:** 0
- **Serious:** 2
- **Moderate:** 1

### Violations by Page

#### /dashboard
| Rule | Impact | Element | Fix |
|------|--------|---------|-----|
| color-contrast | serious | `.stat-label` | Increase contrast from 3.2:1 to 4.5:1 |

#### /login
| Rule | Impact | Element | Fix |
|------|--------|---------|-----|
| label | serious | `#password` | Add associated label element |
| focus-visible | moderate | `.submit-btn` | Add visible focus indicator |

### Passing Checks
- ✅ All images have alt text
- ✅ Heading hierarchy is correct
- ✅ Keyboard navigation works
- ✅ ARIA landmarks present
- ✅ Form inputs have descriptions

### Recommendations
1. **High:** Fix color contrast on stat labels
2. **High:** Add labels to login form inputs
3. **Medium:** Add focus indicators to buttons
```

### Console Output

```
═══════════════════════════════════════════════════════════════════
 ACCESSIBILITY AUDIT (WCAG 2.1 AA)
═══════════════════════════════════════════════════════════════════

 Pages: 5 | Violations: 3 | Critical: 0 | Serious: 2 | Moderate: 1

 ┌──────────────────────────────────────────────────────────────┐
 │ Page          │ Critical │ Serious │ Moderate │ Status      │
 ├──────────────────────────────────────────────────────────────┤
 │ /dashboard    │    0     │    1    │    0     │ ⚠️ ISSUES   │
 │ /login        │    0     │    1    │    1     │ ⚠️ ISSUES   │
 │ /profile      │    0     │    0    │    0     │ ✅ PASS     │
 │ /settings     │    0     │    0    │    0     │ ✅ PASS     │
 │ /404          │    0     │    0    │    0     │ ✅ PASS     │
 └──────────────────────────────────────────────────────────────┘

 Blocking: NO (no critical violations)
 Report: .claude/reports/accessibility-{timestamp}.md

═══════════════════════════════════════════════════════════════════
```

### Configuration

```yaml
# .claude/auto-config.yaml
accessibility:
  enabled: true
  standard: wcag21aa  # wcag2a | wcag2aa | wcag21aa
  block_on_critical: true
  block_on_serious: false  # Set true for strict mode
  skip_paths:
    - "/admin/*"  # Internal tools
    - "/debug/*"
  custom_rules:
    - no-positive-tabindex
    - landmark-one-main
```

### Integration with Workflow

Add to Phase 6 when work_type == FRONTEND:

```markdown
### 6.1.4 Accessibility Audit

**For FRONTEND work types:**

1. Run axe-core accessibility scan
2. Generate a11y report
3. Flag blocking issues (critical violations)

**Blocking Criteria:**
- Any critical violation → BLOCK
- Serious violations in new code → BLOCK (if strict mode)
```

## Additional Resources

### Reference Files

- **`references/viewport-sizes.md`** - Standard viewport dimensions
- **`references/comparison-tools.md`** - Pixel comparison libraries
- **`references/wcag-checklist.md`** - Full WCAG 2.1 AA checklist

## When NOT to Use This Skill

Do NOT use this skill when:
- Work type is BACKEND only
- No UI components changed
- Headless browser not available
- Test is API-only
- Internal admin tools (unless required)
