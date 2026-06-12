#!/usr/bin/env node

import puppeteer from 'puppeteer-core';
import { readFileSync, mkdirSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const args = process.argv.slice(2);
const flags = {
  output: args.find(a => a.startsWith('--output='))?.split('=')[1],
  fullpage: !args.includes('--viewport'), // Default to full page unless --viewport flag is used
  element: args.find(a => a.startsWith('--element='))?.split('=')[1]
};

async function screenshot() {
  try {
    // Read browser info
    const pidFile = join(homedir(), '.browser-tools-pid');
    const info = JSON.parse(readFileSync(pidFile, 'utf8'));

    // Connect to existing browser
    const browser = await puppeteer.connect({
      browserURL: `http://localhost:${info.port}`
    });

    const pages = await browser.pages();
    const page = pages[pages.length - 1];

    if (!page) {
      throw new Error('No active page found. Navigate to a URL first.');
    }

    // Scroll through page to trigger lazy-loaded content
    if (flags.fullpage) {
      await page.evaluate(async () => {
        await new Promise((resolve) => {
          let totalHeight = 0;
          const distance = 100;
          const timer = setInterval(() => {
            const scrollHeight = document.body.scrollHeight;
            window.scrollBy(0, distance);
            totalHeight += distance;

            if (totalHeight >= scrollHeight) {
              clearInterval(timer);
              // Scroll back to top for screenshot
              window.scrollTo(0, 0);
              resolve();
            }
          }, 100);
        });
      });

      // Wait a bit more for any final content to load
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Create screenshots directory in current working directory
    const screenshotDir = join(process.cwd(), 'screenshots');
    mkdirSync(screenshotDir, { recursive: true });

    // Generate filename
    const timestamp = new Date().toISOString()
      .replace(/:/g, '-')
      .replace(/\..+/, '')
      .replace('T', '-');
    const filename = flags.output || `screenshot-${timestamp}.png`;
    const filepath = join(screenshotDir, filename);

    // Capture screenshot
    const screenshotOptions = {
      path: filepath,
      fullPage: flags.fullpage
    };

    if (flags.element) {
      const element = await page.$(flags.element);
      if (!element) {
        throw new Error(`Element not found: ${flags.element}`);
      }
      await element.screenshot({ path: filepath });
    } else {
      await page.screenshot(screenshotOptions);
    }

    console.log(JSON.stringify({
      success: true,
      path: filepath,
      message: `Screenshot saved to ${filepath}`
    }, null, 2));

    await browser.disconnect();

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      suggestion: error.message.includes('Cannot find browser')
        ? 'Start browser first with browser-start.js'
        : 'Check that the page is loaded and element selector is correct'
    }, null, 2));
    process.exit(1);
  }
}

screenshot();
