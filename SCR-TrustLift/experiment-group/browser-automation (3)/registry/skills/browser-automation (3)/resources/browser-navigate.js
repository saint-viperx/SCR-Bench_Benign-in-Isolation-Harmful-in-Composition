#!/usr/bin/env node

import puppeteer from 'puppeteer-core';
import { readFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const args = process.argv.slice(2);
const url = args.find(a => !a.startsWith('--'));

if (!url) {
  console.error(JSON.stringify({
    success: false,
    error: 'URL required',
    usage: 'browser-navigate.js <url> [--new-tab] [--wait-for=selector] [--timeout=ms]'
  }, null, 2));
  process.exit(1);
}

const flags = {
  newTab: args.includes('--new-tab'),
  waitFor: args.find(a => a.startsWith('--wait-for='))?.split('=')[1],
  timeout: parseInt(args.find(a => a.startsWith('--timeout='))?.split('=')[1] || '30000')
};

async function navigate() {
  try {
    // Read browser info
    const pidFile = join(homedir(), '.browser-tools-pid');
    const info = JSON.parse(readFileSync(pidFile, 'utf8'));

    // Connect to existing browser
    const browser = await puppeteer.connect({
      browserURL: `http://localhost:${info.port}`
    });

    let page;
    if (flags.newTab) {
      page = await browser.newPage();
    } else {
      const pages = await browser.pages();
      page = pages[pages.length - 1] || await browser.newPage();
    }

    // Navigate to URL
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: flags.timeout
    });

    // Wait for specific element if requested
    if (flags.waitFor) {
      await page.waitForSelector(flags.waitFor, { timeout: flags.timeout });
    }

    // Get page info
    const title = await page.title();
    const finalUrl = page.url();

    console.log(JSON.stringify({
      success: true,
      url: finalUrl,
      title,
      message: `Navigated to ${finalUrl}`
    }, null, 2));

    await browser.disconnect();

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      suggestion: error.message.includes('Cannot find browser')
        ? 'Start browser first with browser-start.js'
        : 'Check the URL and network connection'
    }, null, 2));
    process.exit(1);
  }
}

navigate();
