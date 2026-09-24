/**
 * Test authentication helpers and session mocking for Playwright tests
 * Enables reliable testing of role-guarded routes and checkout flows
 */
import { Page } from '@playwright/test';

export const ADMIN_USER = {
  user_id: 'usr-admin-001',
  name: 'Juan Dela Cruz',
  username: 'admin',
  email: 'admin@merylshoes.com',
  role_id: '1',
  role_name: 'Administrator',
  status: 'Active',
  staff_code: 'ADM-001',
};

export const CASHIER_USER = {
  user_id: 'usr-cashier-002',
  name: 'Maria Santos',
  username: 'cashier',
  email: 'cashier@merylshoes.com',
  role_id: '2',
  role_name: 'Sales Staff',
  status: 'Active',
  staff_code: 'CSH-015',
};

export const INVENTORY_USER = {
  user_id: 'usr-inventory-003',
  name: 'Carlos Reyes',
  username: 'inventory',
  email: 'inventory@merylshoes.com',
  role_id: '3',
  role_name: 'Inventory Staff',
  status: 'Active',
  staff_code: 'INV-002',
};

export async function loginAsRole(page: Page, user: typeof ADMIN_USER, targetUrl?: string) {
  // Mock login API response
  await page.route('**/api/auth/login', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ ok: true, user }),
    });
  });

  // Mock /api/auth/me to return active user
  await page.route('**/api/auth/me', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ ok: true, user }),
    });
  });

  await page.goto('/');
  await page.fill('input[placeholder="Enter username"]', user.username);
  await page.fill('input[placeholder="Enter password"]', 'ValidPass123');
  await page.click('button[type="submit"]');

  const targetRegex = user.role_name.toLowerCase().includes('admin')
    ? /.*admin/
    : user.role_name.toLowerCase().includes('sales')
    ? /.*sales/
    : /.*inventory/;

  await page.waitForURL(targetRegex, { timeout: 10000 });

  if (targetUrl && !page.url().includes(targetUrl)) {
    await page.goto(targetUrl);
    await page.waitForLoadState('domcontentloaded');
  }
}

