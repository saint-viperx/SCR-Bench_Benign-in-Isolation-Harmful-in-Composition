#!/usr/bin/env node

import puppeteer from 'puppeteer-core';
import { readFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const args = process.argv.slice(2);
let code = args.find(a => !a.startsWith('--'));

// Read from stdin if code is '-'
if (code === '-') {
  const chunks = [];
  process.stdin.on('data', chunk => chunks.push(chunk));
  await new Promise(resolve => process.stdin.on('end', resolve));
  code = Buffer.concat(chunks).toString('utf8');
}

if (!code) {
  console.error(JSON.stringify({
    success: false,
    error: 'JavaScript code required',
    usage: 'browser-eval.js "<code>" [--async] [--json] [--timeout=ms]'
  }, null, 2));
  process.exit(1);
}

const flags = {
  async: args.includes('--async'),
  json: args.includes('--json'),
  timeout: parseInt(args.find(a => a.startsWith('--timeout='))?.split('=')[1] || '30000')
};

async function evaluate() {
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

    // Wrap in async IIFE if --async flag present
    const execCode = flags.async
      ? `(async () => { ${code} })()`
      : code;

    // Execute JavaScript in page context
    const result = await page.evaluate(execCode);

    // Format output
    if (flags.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log(JSON.stringify({
        success: true,
        result
      }, null, 2));
    }

    await browser.disconnect();

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      stack: error.stack,
      suggestion: error.message.includes('Cannot find browser')
        ? 'Start browser first with browser-start.js'
        : 'Check your JavaScript syntax and ensure the page is loaded'
    }, null, 2));
    process.exit(1);
  }
}

evaluate();
