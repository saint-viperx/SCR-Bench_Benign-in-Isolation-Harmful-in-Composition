# WCAG 2.1 AA Checklist for E2E Testing

## Overview

This checklist covers WCAG 2.1 Level AA requirements for automated and manual accessibility testing.

## 1. Perceivable

Content must be presentable to users in ways they can perceive.

### 1.1 Text Alternatives

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Non-text content has text alternative | 1.1.1 | All `<img>` have `alt` attribute | `image-alt` |
| Decorative images have empty alt | 1.1.1 | Decorative `<img>` have `alt=""` | `image-alt` |
| Complex images have long description | 1.1.1 | Charts/graphs have `aria-describedby` | `image-alt` |
| Icons have accessible names | 1.1.1 | Icon buttons have `aria-label` | `button-name` |

### 1.2 Time-based Media

| Criterion | ID | Test | Manual Check |
|-----------|-----|------|--------------|
| Captions for prerecorded audio | 1.2.2 | Videos have captions | Yes |
| Audio description for video | 1.2.5 | Important visual content described | Yes |
| Sign language (AAA) | 1.2.6 | Optional enhancement | Yes |

### 1.3 Adaptable

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Info and relationships | 1.3.1 | Proper heading hierarchy | `heading-order` |
| Meaningful sequence | 1.3.2 | DOM order matches visual order | `tabindex` |
| Sensory characteristics | 1.3.3 | No reliance on shape/color alone | Manual |
| Orientation | 1.3.4 | Works in portrait and landscape | E2E viewport test |
| Input purpose | 1.3.5 | Form fields have `autocomplete` | `autocomplete-valid` |

### 1.4 Distinguishable

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Color contrast (normal text) | 1.4.3 | 4.5:1 ratio minimum | `color-contrast` |
| Color contrast (large text) | 1.4.3 | 3:1 ratio for 18pt+ or 14pt+ bold | `color-contrast` |
| Resize text | 1.4.4 | Page usable at 200% zoom | E2E zoom test |
| Images of text | 1.4.5 | Use real text, not images | Manual |
| Contrast (non-text) | 1.4.11 | UI components 3:1 contrast | `color-contrast` |
| Text spacing | 1.4.12 | Content readable with increased spacing | E2E test |
| Content on hover/focus | 1.4.13 | Tooltips dismissible & hoverable | Manual |

## 2. Operable

UI components must be operable.

### 2.1 Keyboard Accessible

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Keyboard | 2.1.1 | All functions work via keyboard | `keyboard` |
| No keyboard trap | 2.1.2 | Can tab away from all elements | `focus-trap` |
| Keyboard shortcuts | 2.1.4 | Single-key shortcuts can be disabled | Manual |

### 2.2 Enough Time

| Criterion | ID | Test | Manual Check |
|-----------|-----|------|--------------|
| Timing adjustable | 2.2.1 | Can extend/disable time limits | Yes |
| Pause, stop, hide | 2.2.2 | Auto-updating content pausable | Yes |

### 2.3 Seizures and Physical Reactions

| Criterion | ID | Test | Manual Check |
|-----------|-----|------|--------------|
| Three flashes | 2.3.1 | No content flashes >3x/second | Yes |

### 2.4 Navigable

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Bypass blocks | 2.4.1 | Skip to main content link | `bypass` |
| Page titled | 2.4.2 | Descriptive `<title>` | `document-title` |
| Focus order | 2.4.3 | Logical tab sequence | `tabindex` |
| Link purpose | 2.4.4 | Links describe destination | `link-name` |
| Multiple ways | 2.4.5 | Site search or sitemap available | Manual |
| Headings and labels | 2.4.6 | Descriptive headings | `empty-heading` |
| Focus visible | 2.4.7 | Visible focus indicator | `focus-visible` |

### 2.5 Input Modalities

| Criterion | ID | Test | Manual Check |
|-----------|-----|------|--------------|
| Pointer gestures | 2.5.1 | Complex gestures have alternatives | Yes |
| Pointer cancellation | 2.5.2 | Can cancel pointer actions | Yes |
| Label in name | 2.5.3 | Accessible name includes visible text | `label-content-name-mismatch` |
| Motion actuation | 2.5.4 | Motion-triggered actions have alternatives | Yes |

## 3. Understandable

Content must be understandable.

### 3.1 Readable

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Language of page | 3.1.1 | `<html lang="...">` present | `html-has-lang` |
| Language of parts | 3.1.2 | `lang` on foreign text | `valid-lang` |

### 3.2 Predictable

| Criterion | ID | Test | Manual Check |
|-----------|-----|------|--------------|
| On focus | 3.2.1 | No context change on focus | Yes |
| On input | 3.2.2 | No unexpected context change | Yes |
| Consistent navigation | 3.2.3 | Nav in same location | Yes |
| Consistent identification | 3.2.4 | Same icons/labels for same functions | Yes |

### 3.3 Input Assistance

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Error identification | 3.3.1 | Errors clearly described | Manual |
| Labels or instructions | 3.3.2 | Form fields have labels | `label` |
| Error suggestion | 3.3.3 | Suggestions for fixing errors | Manual |
| Error prevention | 3.3.4 | Confirm/review before submit | Manual |

## 4. Robust

Content must be robust for various user agents.

### 4.1 Compatible

| Criterion | ID | Test | axe-core Rule |
|-----------|-----|------|---------------|
| Parsing | 4.1.1 | Valid HTML | `duplicate-id` |
| Name, role, value | 4.1.2 | Custom controls have ARIA | `aria-roles` |
| Status messages | 4.1.3 | Status updates use `role="status"` | `aria-live` |

## Automated Test Coverage

### axe-core Tags

```typescript
// Full WCAG 2.1 AA coverage
const tags = ['wcag2a', 'wcag2aa', 'wcag21aa'];

// Best practices (beyond WCAG)
const extendedTags = ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'];
```

### Playwright Integration

```typescript
import AxeBuilder from '@axe-core/playwright';

const results = await new AxeBuilder({ page })
  .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
  .exclude('.third-party-widget')  // Exclude known issues
  .analyze();

// Check for violations
if (results.violations.length > 0) {
  console.log('Accessibility violations found:', results.violations);
}
```

## Violation Impact Levels

| Level | Block Merge? | Action Required |
|-------|--------------|-----------------|
| Critical | Yes | Must fix before merge |
| Serious | Configurable | Should fix, may block in strict mode |
| Moderate | No | Should fix, warning only |
| Minor | No | Consider fixing |

## Manual Testing Checklist

These cannot be fully automated:

- [ ] Screen reader announces content logically
- [ ] Keyboard navigation is intuitive
- [ ] Focus indicator is clearly visible
- [ ] Error messages are helpful
- [ ] Time limits can be extended
- [ ] Animations can be paused
- [ ] Content is understandable
- [ ] Forms are easy to complete

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [Playwright Accessibility](https://playwright.dev/docs/accessibility-testing)
