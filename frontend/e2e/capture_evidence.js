/**
 * Automatic Screenshot Capture Utility for Playwright Evidence
 * Captures high-resolution PNGs of test execution reports and saves them
 * to evidence_screenshots/playwright/ ready for manuscript insertion.
 */
import { chromium } from '@playwright/test';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function captureEvidence() {
  const outputDir = path.resolve(__dirname, '../../evidence_screenshots/playwright');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const reportPath = path.resolve(__dirname, '../playwright-report/index.html');
  if (!fs.existsSync(reportPath)) {
    console.error('Playwright report not found. Please run tests first.');
    process.exit(1);
  }

  console.log('Launching browser to capture Playwright HTML Report Evidence...');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  await page.goto(`file://${reportPath}`);
  await page.waitForTimeout(1000);

  // Capture master overview report
  const masterPath = path.join(outputDir, 'Blackbox_Playwright_Full_Report.png');
  await page.screenshot({ path: masterPath, fullPage: true });
  console.log(`Saved master evidence: ${masterPath}`);

  await browser.close();
  console.log('All evidence screenshots generated successfully!');
}

captureEvidence().catch(err => {
  console.error('Error capturing evidence:', err);
  process.exit(1);
});

