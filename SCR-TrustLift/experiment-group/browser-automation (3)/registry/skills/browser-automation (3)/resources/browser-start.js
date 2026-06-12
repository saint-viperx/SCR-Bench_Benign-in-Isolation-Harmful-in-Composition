#!/usr/bin/env node

import puppeteer from 'puppeteer-core';
import { execSync } from 'child_process';
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { homedir, platform } from 'os';
import { join } from 'path';

const args = process.argv.slice(2);
const flags = {
  profile: args.includes('--profile'),
  headless: args.includes('--headless'),
  port: args.find(a => a.startsWith('--port='))?.split('=')[1] || '9222'
};

// Find Chrome executable based on OS
function getChromeExecutable() {
  const plat = platform();

  if (plat === 'darwin') {
    return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  } else if (plat === 'linux') {
    const paths = ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'];
    for (const p of paths) {
      if (existsSync(p)) return p;
    }
  } else if (plat === 'win32') {
    return 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  }

  throw new Error(`Could not find Chrome executable for platform: ${plat}`);
}

// Get Chrome profile directory
function getProfilePath() {
  const plat = platform();
  const home = homedir();

  if (plat === 'darwin') {
    return join(home, 'Library/Application Support/Google/Chrome/Default');
  } else if (plat === 'linux') {
    return join(home, '.config/google-chrome/Default');
  } else if (plat === 'win32') {
    return join(process.env.LOCALAPPDATA, 'Google', 'Chrome', 'User Data', 'Default');
  }

  throw new Error(`Could not determine profile path for platform: ${plat}`);
}

async function startBrowser() {
  try {
    const executablePath = getChromeExecutable();
    const launchOptions = {
      executablePath,
      headless: flags.headless,
      args: [
        `--remote-debugging-port=${flags.port}`,
        '--no-first-run',
        '--no-default-browser-check'
      ]
    };

    // Add profile directory if requested
    if (flags.profile) {
      const profilePath = getProfilePath();
      const tempProfile = join(homedir(), '.browser-tools-temp-profile');

      // Copy profile to temp location
      try {
        mkdirSync(tempProfile, { recursive: true });

        if (platform() === 'win32') {
          // Windows-specific copy
          execSync(`xcopy "${profilePath}" "${tempProfile}" /E /I /H /Y`, { stdio: 'ignore' });
        } else {
          // Mac/Linux rsync
          execSync(`rsync -a "${profilePath}/" "${tempProfile}/"`, { stdio: 'ignore' });
        }

        launchOptions.userDataDir = tempProfile;
      } catch (err) {
        console.error(`Warning: Could not copy profile: ${err.message}`);
      }
    }

    const browser = await puppeteer.launch(launchOptions);
    const wsEndpoint = browser.wsEndpoint();

    // Store browser info for other scripts
    const pidFile = join(homedir(), '.browser-tools-pid');
    const info = {
      pid: browser.process()?.pid,
      wsEndpoint,
      port: flags.port,
      startedAt: new Date().toISOString()
    };

    writeFileSync(pidFile, JSON.stringify(info, null, 2));

    // Output connection info
    console.log(JSON.stringify({
      success: true,
      port: flags.port,
      wsEndpoint,
      message: `Browser started on port ${flags.port}`
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      suggestion: 'Check that Chrome is installed and the executable path is correct'
    }, null, 2));
    process.exit(1);
  }
}

startBrowser();
