# Standard Viewport Sizes for E2E Testing

## Mobile Devices

| Device | Width | Height | Pixel Ratio |
|--------|-------|--------|-------------|
| iPhone SE | 375 | 667 | 2 |
| iPhone 12/13 | 390 | 844 | 3 |
| iPhone 12/13 Pro Max | 428 | 926 | 3 |
| Samsung Galaxy S21 | 360 | 800 | 3 |
| Google Pixel 5 | 393 | 851 | 2.75 |

## Tablets

| Device | Width | Height | Pixel Ratio |
|--------|-------|--------|-------------|
| iPad Mini | 768 | 1024 | 2 |
| iPad Pro 11" | 834 | 1194 | 2 |
| iPad Pro 12.9" | 1024 | 1366 | 2 |
| Samsung Galaxy Tab | 800 | 1280 | 1.5 |

## Desktop

| Size | Width | Height | Description |
|------|-------|--------|-------------|
| Small laptop | 1280 | 800 | MacBook 13" |
| Laptop | 1440 | 900 | MacBook 15" |
| Desktop | 1920 | 1080 | Full HD |
| Wide desktop | 2560 | 1440 | 2K monitor |

## Recommended Test Set

For balanced coverage, test these 4 viewports:

```typescript
const viewports = [
  { width: 375, height: 667, name: 'mobile', device: 'iPhone SE' },
  { width: 768, height: 1024, name: 'tablet', device: 'iPad Mini' },
  { width: 1280, height: 800, name: 'laptop', device: 'MacBook 13"' },
  { width: 1920, height: 1080, name: 'desktop', device: 'Full HD' },
];
```

## Breakpoint Alignment

Common CSS breakpoints:

| Framework | xs | sm | md | lg | xl | 2xl |
|-----------|----|----|----|----|----|----|
| Tailwind CSS | 0 | 640 | 768 | 1024 | 1280 | 1536 |
| Bootstrap 5 | 0 | 576 | 768 | 992 | 1200 | 1400 |
| Material UI | 0 | 600 | 900 | 1200 | 1536 | - |

## Playwright Device Presets

```typescript
import { devices } from '@playwright/test';

// Use built-in device presets
const projects = [
  { name: 'mobile', use: devices['iPhone 13'] },
  { name: 'tablet', use: devices['iPad Pro 11'] },
  { name: 'desktop', use: { viewport: { width: 1280, height: 800 } } },
];
```
