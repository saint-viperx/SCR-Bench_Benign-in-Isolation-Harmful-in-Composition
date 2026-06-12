# Pixel Comparison Tools for E2E Testing

## Overview

Visual regression testing compares screenshots to detect unintended changes. This reference covers the most popular pixel comparison libraries.

## Comparison Libraries

### 1. pixelmatch

Lightweight, fast, pure JavaScript.

| Feature | Value |
|---------|-------|
| npm | `pixelmatch` |
| Size | 5kb |
| Speed | Very fast |
| Output | Diff image |

```typescript
import pixelmatch from 'pixelmatch';
import { PNG } from 'pngjs';
import fs from 'fs';

const img1 = PNG.sync.read(fs.readFileSync('baseline.png'));
const img2 = PNG.sync.read(fs.readFileSync('current.png'));
const { width, height } = img1;
const diff = new PNG({ width, height });

const numDiffPixels = pixelmatch(
  img1.data,
  img2.data,
  diff.data,
  width,
  height,
  { threshold: 0.1 }  // 0-1, lower = more sensitive
);

fs.writeFileSync('diff.png', PNG.sync.write(diff));
console.log(`Different pixels: ${numDiffPixels}`);
```

### 2. looks-same

Yandex's comparison tool with anti-aliasing detection.

| Feature | Value |
|---------|-------|
| npm | `looks-same` |
| Anti-aliasing | Yes |
| Tolerance | Configurable |
| Output | Diff image + report |

```typescript
import looksSame from 'looks-same';

const result = await looksSame('baseline.png', 'current.png', {
  tolerance: 5,               // Color tolerance (0-255)
  ignoreAntialiasing: true,   // Ignore anti-aliasing differences
  ignoreCaret: true,          // Ignore text cursor
});

if (!result.equal) {
  await looksSame.createDiff({
    reference: 'baseline.png',
    current: 'current.png',
    diff: 'diff.png',
    highlightColor: '#ff00ff',
  });
}
```

### 3. jest-image-snapshot

Jest integration for snapshot testing.

| Feature | Value |
|---------|-------|
| npm | `jest-image-snapshot` |
| Integration | Jest |
| Threshold | Percentage |
| Output | Diff in test reports |

```typescript
import { toMatchImageSnapshot } from 'jest-image-snapshot';

expect.extend({ toMatchImageSnapshot });

test('visual regression', async () => {
  const screenshot = await page.screenshot();

  expect(screenshot).toMatchImageSnapshot({
    failureThreshold: 0.01,        // 1% pixel difference allowed
    failureThresholdType: 'percent',
    customSnapshotsDir: '__snapshots__',
    customDiffDir: '__diffs__',
  });
});
```

### 4. Playwright Built-in

Native Playwright screenshot comparison.

| Feature | Value |
|---------|-------|
| Integration | Playwright |
| Config | playwright.config.ts |
| Output | HTML report |

```typescript
import { test, expect } from '@playwright/test';

test('visual comparison', async ({ page }) => {
  await page.goto('/dashboard');

  // Full page screenshot
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100,          // Allow up to 100 different pixels
    threshold: 0.2,              // Per-pixel threshold
    animations: 'disabled',       // Disable CSS animations
  });

  // Element screenshot
  const header = page.locator('header');
  await expect(header).toHaveScreenshot('header.png');
});
```

### 5. reg-suit

Full visual regression testing platform.

| Feature | Value |
|---------|-------|
| npm | `reg-suit` |
| Storage | S3, GCS, or local |
| CI Integration | Yes |
| Report | HTML dashboard |

```bash
# Initialize
npx reg-suit init

# Run comparison
npx reg-suit run
```

```json
// regconfig.json
{
  "core": {
    "workingDir": ".reg",
    "actualDir": "screenshots/current",
    "expectedDir": "screenshots/baseline",
    "diffDir": "screenshots/diff"
  },
  "plugins": {
    "reg-keygen-git-hash-plugin": {},
    "reg-notify-github-plugin": {}
  }
}
```

## Comparison Matrix

| Tool | Speed | Accuracy | CI Ready | Report | Learning Curve |
|------|-------|----------|----------|--------|----------------|
| pixelmatch | Fast | Good | Manual | Diff image | Low |
| looks-same | Medium | Excellent | Manual | Diff + JSON | Low |
| jest-image-snapshot | Medium | Good | Yes | Jest report | Low |
| Playwright | Fast | Good | Yes | HTML report | Low |
| reg-suit | Slow | Excellent | Yes | Dashboard | Medium |

## Recommended Setup

### For Playwright Projects

Use built-in `toHaveScreenshot()`:

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
    },
  },
  snapshotDir: './__snapshots__',
});
```

### For Jest Projects

Use jest-image-snapshot:

```typescript
// jest.setup.ts
import { toMatchImageSnapshot } from 'jest-image-snapshot';

expect.extend({ toMatchImageSnapshot });
```

### For Custom Solutions

Use pixelmatch for speed or looks-same for accuracy:

```typescript
// comparison-utils.ts
import pixelmatch from 'pixelmatch';
import { PNG } from 'pngjs';

export async function compareScreenshots(
  baseline: string,
  current: string,
  threshold: number = 0.01
): Promise<{ match: boolean; diffPercent: number; diffPath?: string }> {
  const img1 = PNG.sync.read(fs.readFileSync(baseline));
  const img2 = PNG.sync.read(fs.readFileSync(current));

  const { width, height } = img1;
  const totalPixels = width * height;
  const diff = new PNG({ width, height });

  const numDiffPixels = pixelmatch(
    img1.data, img2.data, diff.data,
    width, height, { threshold: 0.1 }
  );

  const diffPercent = numDiffPixels / totalPixels;
  const match = diffPercent <= threshold;

  let diffPath: string | undefined;
  if (!match) {
    diffPath = `diff-${Date.now()}.png`;
    fs.writeFileSync(diffPath, PNG.sync.write(diff));
  }

  return { match, diffPercent, diffPath };
}
```

## Threshold Guidelines

| Scenario | Recommended Threshold |
|----------|----------------------|
| Pixel-perfect design | 0.001 (0.1%) |
| Standard UI testing | 0.01 (1%) |
| Responsive layouts | 0.02 (2%) |
| Dynamic content | 0.05 (5%) |
| Animation-heavy pages | 0.1 (10%) |

## Best Practices

### 1. Disable Animations

```typescript
// Playwright
await page.addStyleTag({
  content: `
    *, *::before, *::after {
      animation: none !important;
      transition: none !important;
    }
  `
});
```

### 2. Wait for Stability

```typescript
// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for specific element
await page.waitForSelector('[data-loaded="true"]');

// Wait for fonts
await page.evaluate(() => document.fonts.ready);
```

### 3. Mask Dynamic Content

```typescript
// Playwright masking
await expect(page).toHaveScreenshot({
  mask: [
    page.locator('.timestamp'),
    page.locator('.avatar'),
    page.locator('[data-testid="random-content"]'),
  ],
});
```

### 4. Consistent Environment

```typescript
// Set consistent viewport
await page.setViewportSize({ width: 1280, height: 720 });

// Set consistent timezone
await page.emulateTimezone('UTC');

// Set consistent color scheme
await page.emulateMedia({ colorScheme: 'light' });
```

## Diff Output Format

```
.claude/screenshots/
├── baseline/
│   └── dashboard.png
├── current/
│   └── dashboard.png
└── diff/
    └── dashboard-diff.png
```

### Console Output

```
┌─────────────────────────────────────────────────────────────┐
│ Visual Comparison Results                                   │
│                                                             │
│   Baseline: .claude/screenshots/baseline/dashboard.png      │
│   Current: .claude/screenshots/current/dashboard.png        │
│                                                             │
│   Pixel difference: 0.5%                                    │
│   Threshold: 1%                                             │
│   Status: ✅ PASS                                           │
│                                                             │
│   Changed regions: 2                                        │
│   - Header logo (minor)                                     │
│   - Footer timestamp (expected)                             │
└─────────────────────────────────────────────────────────────┘
```

## Resources

- [pixelmatch](https://github.com/mapbox/pixelmatch)
- [looks-same](https://github.com/gemini-testing/looks-same)
- [jest-image-snapshot](https://github.com/americanexpress/jest-image-snapshot)
- [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
- [reg-suit](https://reg-viz.github.io/reg-suit/)
