/**
 * High-Reliability Black-Box Test Runner & Terminal Reporter
 * Guarantees 100% accurate test parsing across all Windows terminals
 * Reads structured Playwright JSON output with zero regex decoding errors.
 */
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootFrontendDir = path.resolve(__dirname, '..');

const tableFileMap = {
  39: { file: '01_auth_user_management.spec.ts', name: 'Table 39: User Authentication & Access Control (AUTH)' },
  40: { file: '02_inventory_management.spec.ts', name: 'Table 40: Product Encoding & Stock Management (INV)' },
  41: { file: '03_pos_transactions.spec.ts', name: 'Table 41: Sales Transactions & POS Checkout (POS)' },
  42: { file: '04_replacement_rma.spec.ts', name: 'Table 42: Replacement & Damaged Item Recording (RMA)' },
  43: { file: '05_promotions_notifications.spec.ts', name: 'Table 43: Promotion Management & Email Notifications (PROMO)' },
  44: { file: '06_analytics_demand.spec.ts', name: 'Table 44: Sales Analytics & Demand Prediction (ANLYT)' },
  45: { file: '07_reports_export.spec.ts', name: 'Table 45: Sales & Inventory Report Generation (RPT)' },
  46: { file: '08_customer_security.spec.ts', name: 'Table 46: Customer Directory & System Security (CUST)' },
};

// Parse command line args
const args = process.argv.slice(2);
let selectedTable = null;
let selectedId = null;
let runAll = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '-Table' || args[i] === '--table') {
    selectedTable = parseInt(args[i + 1], 10);
  } else if (args[i] === '-Evidence' || args[i] === '--evidence') {
    const ev = parseInt(args[i + 1], 10);
    selectedTable = 38 + ev; // Evidence 1 -> Table 39, Evidence 2 -> Table 40, etc.
  } else if (args[i] === '-Id' || args[i] === '--id') {
    selectedId = args[i + 1];
  } else if (args[i] === '-All' || args[i] === '--all') {
    runAll = true;
  }
}

const bannerTitle = selectedTable && tableFileMap[selectedTable]
  ? tableFileMap[selectedTable].name
  : selectedId
  ? `TEST SPECIFICATION: ${selectedId}`
  : `MASTER TEST EXECUTION (ALL TABLES 39 TO 46 | 80 FUNCTIONAL TEST CASES)`;

console.log('');
console.log('\x1b[36m================================================================================\x1b[0m');
console.log('\x1b[33m  MERYL SHOES SYSTEM - PLAYWRIGHT BLACK-BOX E2E TEST EXECUTION\x1b[0m');
console.log('\x1b[90m  Carlos Hilado Memorial State University - College of Computer Studies\x1b[0m');
console.log(`\x1b[37m  ${bannerTitle}\x1b[0m`);
console.log('\x1b[36m================================================================================\x1b[0m');
console.log('');

// Prepare Playwright CLI arguments
const playwrightCliArgs = ['playwright', 'test'];

if (selectedTable && tableFileMap[selectedTable]) {
  playwrightCliArgs.push(`e2e/specs/${tableFileMap[selectedTable].file}`);
}

if (selectedId) {
  playwrightCliArgs.push('-g', selectedId);
}

const tempJsonFile = path.resolve(rootFrontendDir, '.playwright-output.json');
playwrightCliArgs.push(`--reporter=json`);

const isWindows = process.platform === 'win32';
const npxCmd = isWindows ? 'npx.cmd' : 'npx';

const startTime = Date.now();
const child = spawn(npxCmd, playwrightCliArgs, {
  cwd: rootFrontendDir,
  shell: true,
  env: { ...process.env, CI: '1' },
});

let jsonBuffer = '';
child.stdout.on('data', (data) => {
  jsonBuffer += data.toString();
});

child.stderr.on('data', (data) => {
  // Ignore stderr logs like webServer info
});

child.on('close', (code) => {
  const durationSec = ((Date.now() - startTime) / 1000).toFixed(2);
  let parsed = null;

  try {
    // Find the JSON object starting from the first '{'
    const startIdx = jsonBuffer.indexOf('{');
    const endIdx = jsonBuffer.lastIndexOf('}');
    if (startIdx !== -1 && endIdx !== -1) {
      parsed = JSON.parse(jsonBuffer.substring(startIdx, endIdx + 1));
    }
  } catch (err) {
    console.error('Failed to parse test results:', err.message);
  }

  if (!parsed || !parsed.suites) {
    console.log('\x1b[31mError: No test results were generated.\x1b[0m');
    process.exit(1);
  }

  let totalPassed = 0;
  let totalFailed = 0;

  function traverseSuites(suiteList) {
    for (const suite of suiteList) {
      if (suite.title && (suite.title.startsWith('Table') || suite.title.includes('Table '))) {
        console.log(`\n\x1b[36m [${suite.title}]\x1b[0m`);
      }

      if (suite.specs && suite.specs.length > 0) {
        for (const spec of suite.specs) {
          const testObj = spec.tests?.[0];
          const result = testObj?.results?.[0];
          const isPassed = spec.ok && result?.status === 'passed';
          const durationMs = result?.duration ?? 0;
          const durationStr = durationMs >= 1000 ? `${(durationMs / 1000).toFixed(1)}s` : `${durationMs}ms`;

          // Split test ID from title
          const titleParts = spec.title.split(': ');
          const tcId = titleParts[0].trim();
          const tcDesc = titleParts.slice(1).join(': ').trim() || spec.title;

          const padLength = Math.max(4, 60 - tcDesc.length);
          const dots = '.'.repeat(padLength);

          if (isPassed) {
            totalPassed++;
            console.log(`  \x1b[30;42m PASS \x1b[0m  \x1b[33m${tcId}\x1b[0m  \x1b[37m${tcDesc}\x1b[0m \x1b[90m${dots}\x1b[0m \x1b[36m${durationStr}\x1b[0m`);
          } else {
            totalFailed++;
            console.log(`  \x1b[37;41m FAIL \x1b[0m  \x1b[33m${tcId}\x1b[0m  \x1b[31m${tcDesc}\x1b[0m \x1b[90m${dots}\x1b[0m \x1b[31m${durationStr}\x1b[0m`);
          }
        }
      }

      if (suite.suites && suite.suites.length > 0) {
        traverseSuites(suite.suites);
      }
    }
  }

  traverseSuites(parsed.suites);

  const totalTested = totalPassed + totalFailed;
  console.log('');
  console.log('\x1b[90m--------------------------------------------------------------------------------\x1b[0m');
  console.log('\x1b[37m Execution Summary:\x1b[0m');
  if (totalFailed === 0 && totalTested > 0) {
    console.log(`   \x1b[37mStatus       : \x1b[32mALL PASSED (100% Pass Rate)\x1b[0m`);
  } else {
    console.log(`   \x1b[37mStatus       : \x1b[33m${totalPassed} Passed, ${totalFailed} Failed\x1b[0m`);
  }
  console.log(`   \x1b[37mTotal Tests  : \x1b[36m${totalPassed} / ${totalTested} passed\x1b[0m`);
  console.log(`   \x1b[37mDuration     : \x1b[90m${durationSec}s\x1b[0m`);
  console.log(`   \x1b[37mFramework    : \x1b[90mPlaywright E2E Test Engine (Chromium)\x1b[0m`);
  console.log('\x1b[36m================================================================================\x1b[0m\n');
});

