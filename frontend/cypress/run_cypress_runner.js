/**
 * High-Reliability Cypress Black-Box Test Runner & Terminal Reporter
 * Carlos Hilado Memorial State University - Capstone Research
 * Guarantees clean, screenshot-ready terminal output across all Windows terminals
 */
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

// Ensure ELECTRON_RUN_AS_NODE is cleared so Cypress can launch Electron / Chrome
delete process.env.ELECTRON_RUN_AS_NODE;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootFrontendDir = path.resolve(__dirname, '..');

const tableFileMap = {
  39: { file: '01_auth_user_management.cy.ts', name: 'Table 39: User Authentication & User Management (AUTH)' },
  40: { file: '02_inventory_management.cy.ts', name: 'Table 40: Product Encoding & Stock Parameter Management (INV)' },
  41: { file: '03_pos_transactions.cy.ts', name: 'Table 41: Sales Transactions & POS Checkout (POS)' },
  42: { file: '04_replacement_rma.cy.ts', name: 'Table 42: Return, Replacement & RMA Management (RMA)' },
  43: { file: '05_promotions_notifications.cy.ts', name: 'Table 43: Promotion Management & Notifications (PROMO)' },
  44: { file: '06_analytics_demand.cy.ts', name: 'Table 44: Sales Analytics & Demand Prediction (ANLYT)' },
  45: { file: '07_reports_export.cy.ts', name: 'Table 45: Sales & Inventory Report Generation (RPT)' },
  46: { file: '08_customer_security.cy.ts', name: 'Table 46: Customer Directory & System Security (CUST)' },
};

// Parse command line arguments
const args = process.argv.slice(2);
let selectedTable = null;
let selectedId = null;
let runAll = false;
let openGui = false;

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '-Table' || arg === '--table' || arg === '-t') {
    selectedTable = parseInt(args[i + 1], 10);
  } else if (arg === '-Evidence' || arg === '--evidence') {
    const ev = parseInt(args[i + 1], 10);
    selectedTable = 38 + ev;
  } else if (arg === '-Id' || arg === '--id') {
    selectedId = args[i + 1];
  } else if (arg === '-All' || arg === '--all' || arg === '-a') {
    runAll = true;
  } else if (arg === '-Open' || arg === '--open' || arg === '-ui' || arg === '--ui') {
    openGui = true;
  }
}

// Default to All if neither Table nor Id nor Open is specified
if (!selectedTable && !selectedId && !openGui) {
  runAll = true;
}

const isWindows = process.platform === 'win32';
const npxCmd = isWindows ? 'npx.cmd' : 'npx';

if (openGui) {
  console.log('\n\x1b[36mLaunching Cypress Interactive Test Runner GUI...\x1b[0m\n');
  const child = spawn(npxCmd, ['cypress', 'open'], {
    cwd: rootFrontendDir,
    stdio: 'inherit',
    shell: true,
    env: { ...process.env, ELECTRON_RUN_AS_NODE: undefined },
  });
  child.on('exit', (code) => {
    process.exit(code ?? 0);
  });
} else {
  runHeadlessCypress();
}

async function runHeadlessCypress() {
  const bannerTitle = selectedTable && tableFileMap[selectedTable]
    ? tableFileMap[selectedTable].name
    : selectedId
    ? `TEST SPECIFICATION FILTER: ${selectedId}`
    : `MASTER TEST EXECUTION (ALL TABLES 39 TO 46 | 80 FUNCTIONAL TEST CASES)`;

  console.log('');
  console.log('\x1b[36m================================================================================\x1b[0m');
  console.log('\x1b[33m  MERYL SHOES SYSTEM - CYPRESS BLACK-BOX E2E TEST EXECUTION\x1b[0m');
  console.log('\x1b[90m  Carlos Hilado Memorial State University - College of Computer Studies\x1b[0m');
  console.log(`\x1b[37m  ${bannerTitle}\x1b[0m`);
  console.log('\x1b[36m================================================================================\x1b[0m');
  console.log('');

  // Dynamically import Cypress module API
  const { default: cypress } = await import('cypress');

  let specPattern;
  if (selectedTable && tableFileMap[selectedTable]) {
    specPattern = path.resolve(rootFrontendDir, 'cypress', 'e2e', tableFileMap[selectedTable].file);
  } else {
    specPattern = path.resolve(rootFrontendDir, 'cypress', 'e2e', '**', '*.cy.ts');
  }

  const startTime = Date.now();

  try {
    const results = await cypress.run({
      project: rootFrontendDir,
      configFile: path.resolve(rootFrontendDir, 'cypress.config.ts'),
      spec: specPattern,
      browser: 'chrome',
      headless: true,
      quiet: true,
      config: {
        video: false,
        screenshotOnRunFailure: false,
      },
    });

    const durationSec = ((Date.now() - startTime) / 1000).toFixed(2);

    if (results.status === 'failed') {
      console.log(`\x1b[31mCypress execution failed: ${results.message}\x1b[0m`);
      process.exit(1);
    }

    let totalPassed = 0;
    let totalFailed = 0;

    if (results.runs && results.runs.length > 0) {
      for (const run of results.runs) {
        const specBase = path.basename(run.spec.relative);
        // Find matching table title
        let tableHeader = specBase;
        for (const t of Object.values(tableFileMap)) {
          if (t.file === specBase) {
            tableHeader = t.name;
            break;
          }
        }

        console.log(`\n\x1b[36m [${tableHeader}]\x1b[0m`);

        if (run.tests && run.tests.length > 0) {
          for (const test of run.tests) {
            const rawTitle = test.title[test.title.length - 1] || 'Unknown Test';
            const isPassed = test.state === 'passed';
            const durationMs = test.duration || 0;
            const durationStr = durationMs >= 1000 ? `${(durationMs / 1000).toFixed(1)}s` : `${durationMs}ms`;

            // Filter by ID if -Id argument was passed
            if (selectedId && !rawTitle.includes(selectedId)) {
              continue;
            }

            const titleParts = rawTitle.split(': ');
            const tcId = titleParts[0].trim();
            const tcDesc = titleParts.slice(1).join(': ').trim() || rawTitle;

            const padLength = Math.max(4, 60 - tcDesc.length);
            const dots = '.'.repeat(padLength);

            if (isPassed) {
              totalPassed++;
              console.log(`  \x1b[30;42m PASS \x1b[0m  \x1b[33m${tcId}\x1b[0m  \x1b[37m${tcDesc}\x1b[0m \x1b[90m${dots}\x1b[0m \x1b[36m${durationStr}\x1b[0m`);
            } else {
              totalFailed++;
              console.log(`  \x1b[37;41m FAIL \x1b[0m  \x1b[33m${tcId}\x1b[0m  \x1b[31m${tcDesc}\x1b[0m \x1b[90m${dots}\x1b[0m \x1b[31m${durationStr}\x1b[0m`);
              if (test.displayError) {
                console.log(`         \x1b[31m${test.displayError.split('\n')[0]}\x1b[0m`);
              }
            }
          }
        }
      }
    }

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
    console.log(`   \x1b[37mFramework    : \x1b[90mCypress E2E Testing Suite (Chrome Headless)\x1b[0m`);
    console.log('\x1b[36m================================================================================\x1b[0m\n');

    process.exit(totalFailed === 0 ? 0 : 1);
  } catch (err) {
    console.error('\x1b[31mError during Cypress execution:\x1b[0m', err);
    process.exit(1);
  }
}
