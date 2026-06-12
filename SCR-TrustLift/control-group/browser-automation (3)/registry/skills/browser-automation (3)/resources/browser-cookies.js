#!/usr/bin/env node

import puppeteer from 'puppeteer-core';
import { readFileSync, writeFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const args = process.argv.slice(2);
const flags = {
  domain: args.find(a => a.startsWith('--domain='))?.split('=')[1],
  format: args.find(a => a.startsWith('--format='))?.split('=')[1] || 'json',
  output: args.find(a => a.startsWith('--output='))?.split('=')[1]
};

async function getCookies() {
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

    // Get all cookies
    let cookies = await page.cookies();

    // Filter by domain if specified
    if (flags.domain) {
      cookies = cookies.filter(c => c.domain.includes(flags.domain));
    }

    // Format cookies
    let output;
    switch (flags.format) {
      case 'json':
        output = JSON.stringify(cookies, null, 2);
        break;

      case 'netscape':
        // Netscape cookie format for wget/curl
        output = '# Netscape HTTP Cookie File\n';
        cookies.forEach(c => {
          output += `${c.domain}\t${c.httpOnly ? 'TRUE' : 'FALSE'}\t${c.path}\t${c.secure ? 'TRUE' : 'FALSE'}\t${Math.floor(c.expires || 0)}\t${c.name}\t${c.value}\n`;
        });
        break;

      case 'header':
        // Cookie header format
        output = cookies.map(c => `${c.name}=${c.value}`).join('; ');
        break;

      default:
        throw new Error(`Unknown format: ${flags.format}. Use: json, netscape, or header`);
    }

    // Output to file or stdout
    if (flags.output) {
      writeFileSync(flags.output, output);
      console.log(JSON.stringify({
        success: true,
        path: flags.output,
        count: cookies.length,
        message: `${cookies.length} cookies saved to ${flags.output}`
      }, null, 2));
    } else {
      console.log(output);
    }

    await browser.disconnect();

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      suggestion: error.message.includes('Cannot find browser')
        ? 'Start browser first with browser-start.js'
        : 'Check that the page is loaded'
    }, null, 2));
    process.exit(1);
  }
}

getCookies();
