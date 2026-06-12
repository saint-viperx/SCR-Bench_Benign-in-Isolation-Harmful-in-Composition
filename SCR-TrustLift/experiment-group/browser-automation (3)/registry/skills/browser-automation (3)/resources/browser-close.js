#!/usr/bin/env node

import { readFileSync, unlinkSync, existsSync, rmSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const args = process.argv.slice(2);
const flags = {
  force: args.includes('--force')
};

async function closeBrowser() {
  try {
    const pidFile = join(homedir(), '.browser-tools-pid');

    if (!existsSync(pidFile)) {
      console.log(JSON.stringify({
        success: true,
        message: 'No browser running'
      }, null, 2));
      return;
    }

    // Read browser info
    const info = JSON.parse(readFileSync(pidFile, 'utf8'));
    const pid = info.pid;

    if (!pid) {
      throw new Error('No PID found in browser info file');
    }

    // Try graceful shutdown first
    try {
      process.kill(pid, 'SIGTERM');

      // Wait for process to exit (max 5 seconds)
      const startTime = Date.now();
      while (Date.now() - startTime < 5000) {
        try {
          process.kill(pid, 0); // Check if process exists
          await new Promise(resolve => setTimeout(resolve, 100));
        } catch {
          // Process has exited
          break;
        }
      }

      // Check if still running
      try {
        process.kill(pid, 0);
        // Still running, force kill if requested
        if (flags.force) {
          process.kill(pid, 'SIGKILL');
        } else {
          throw new Error('Browser did not shut down gracefully. Use --force to kill.');
        }
      } catch {
        // Process has exited successfully
      }

    } catch (error) {
      if (error.code === 'ESRCH') {
        // Process already dead
      } else {
        throw error;
      }
    }

    // Clean up PID file
    unlinkSync(pidFile);

    // Clean up temp profile if exists
    const tempProfile = join(homedir(), '.browser-tools-temp-profile');
    if (existsSync(tempProfile)) {
      rmSync(tempProfile, { recursive: true, force: true });
    }

    console.log(JSON.stringify({
      success: true,
      message: 'Browser closed successfully'
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      suggestion: 'Try using --force flag to forcefully kill the browser process'
    }, null, 2));
    process.exit(1);
  }
}

closeBrowser();
