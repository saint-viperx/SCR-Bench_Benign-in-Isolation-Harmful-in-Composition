---
name: browser-automation
description: Automate browser interactions including form filling, clicking, typing, navigation, and screenshot capture. Use this skill when testing web apps, automating uploads, or validating UI on TikTok, YouTube, or other web platforms.
---

# 🌐 Browser Automation Skill

## Use Cases
- TikTok video upload automation
- Form auto-fill testing
- UI validation with screenshots
- Multi-step workflow automation

---

## Workflow

### 1. Page Navigation
```javascript
// Navigate and wait for load
await page.goto('https://example.com');
await page.waitForSelector('.target-element');
```

### 2. Element Interaction
```javascript
// Click
await page.click('button[type="submit"]');

// Type with delay
await page.type('input[name="title"]', 'Video Title', { delay: 100 });

// Select dropdown
await page.select('select#category', 'entertainment');
```

### 3. File Upload
```javascript
// Upload file
const input = await page.$('input[type="file"]');
await input.uploadFile('/path/to/video.mp4');
```

### 4. Wait Strategies
```javascript
// Wait for network idle
await page.waitForNavigation({ waitUntil: 'networkidle0' });

// Wait for specific element
await page.waitForSelector('.success-message', { timeout: 30000 });

// Wait for text
await page.waitForFunction(() => 
  document.body.textContent.includes('Upload complete')
);
```

### 5. Screenshot & Validation
```javascript
// Full page screenshot
await page.screenshot({ path: 'result.png', fullPage: true });

// Element screenshot
const element = await page.$('.preview');
await element.screenshot({ path: 'preview.png' });
```

---

## Decision Tree

```
Browser task?
├── Login required? → Use saved cookies/session
├── Upload file? → waitForSelector → uploadFile → waitForNavigation
├── Fill form? → Loop through fields with type()
├── Validate result? → Take screenshot + check text
└── Multi-step? → Break into sequential waits
```

---

## Best Practices

| ✅ ทำ | ❌ ไม่ทำ |
|------|---------|
| ใช้ waitForSelector ก่อน interact | Hardcode delays |
| Handle popup/modal cases | Assume elements always exist |
| Take screenshots on error | Ignore timeout errors |
| Use retry logic for flaky elements | Give up after 1 try |

---

## TikTok-Specific Tips

1. **Video upload element**: `input[type="file"][accept="video/*"]`
2. **Title field**: `div[contenteditable="true"]`
3. **Post button**: Look for specific button text/aria-label
4. **Wait for processing**: Check for progress indicator
