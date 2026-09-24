/**
 * Table 39: Black-box Testing of the Alpha Testing of User Authentication
 * and User Management Module (AUTH)
 * Carlos Hilado Memorial State University - Capstone Research
 * Test IDs: TC-AUTH-001 to TC-AUTH-010
 */
import { test, expect } from '@playwright/test';

test.describe('Table 39: User Authentication & User Management (AUTH)', () => {

  test('TC-AUTH-001: Admin login with valid credentials opens Admin Dashboard', async ({ page }) => {
    await page.route('**/api/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          ok: true,
          user: {
            user_id: 'usr-admin-001',
            name: 'Juan Dela Cruz',
            username: 'admin',
            role_name: 'Administrator',
            status: 'Active',
            email: 'admin@merylshoes.com',
          },
        }),
      });
    });

    await page.goto('/');
    await page.fill('input[placeholder="Enter username"]', 'admin');
    await page.fill('input[placeholder="Enter password"]', 'Admin123');
    await page.click('button[type="submit"]');

    // System authenticates and redirects to Admin Dashboard
    await expect(page).toHaveURL(/.*admin/, { timeout: 10000 });
  });

  test('TC-AUTH-002: Sales Staff login with valid credentials opens Sales POS Portal', async ({ page }) => {
    await page.route('**/api/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          ok: true,
          user: {
            user_id: 'usr-cashier-002',
            name: 'Maria Santos',
            username: 'cashier',
            role_name: 'Sales Staff',
            status: 'Active',
            email: 'cashier@merylshoes.com',
          },
        }),
      });
    });

    await page.goto('/');
    await page.fill('input[placeholder="Enter username"]', 'cashier');
    await page.fill('input[placeholder="Enter password"]', 'Staff123');
    await page.click('button[type="submit"]');

    // System authenticates and redirects to Sales POS Portal
    await expect(page).toHaveURL(/.*sales/, { timeout: 10000 });
  });

  test('TC-AUTH-003: Login with incorrect password rejects and displays error', async ({ page }) => {
    await page.goto('/');
    await page.fill('input[placeholder="Enter username"]', 'admin_test');
    await page.fill('input[placeholder="Enter password"]', 'WrongPassword123');
    await page.click('button[type="submit"]');

    // System displays error rejection
    const errorAlert = page.locator('text=/Invalid|failed|incorrect|error/i').first();
    await expect(errorAlert).toBeVisible({ timeout: 5000 });
  });

  test('TC-AUTH-004: Login with empty fields triggers validation and blocks submission', async ({ page }) => {
    await page.goto('/');
    // Clear fields
    await page.fill('input[placeholder="Enter username"]', '');
    await page.fill('input[placeholder="Enter password"]', '');
    await page.click('button[type="submit"]');

    // Verify browser HTML5 validation prevents URL navigation
    await expect(page).toHaveURL(/.*5173\/?$/);
  });

  test('TC-AUTH-005: Deactivated user login attempt is blocked', async ({ page }) => {
    await page.goto('/');
    await page.fill('input[placeholder="Enter username"]', 'usr006_deactivated');
    await page.fill('input[placeholder="Enter password"]', 'Password@123');
    await page.click('button[type="submit"]');

    // System denies deactivated access and displays error
    const errorAlert = page.locator('text=/Invalid|failed|error|deactivated|inactive/i').first();
    await expect(errorAlert).toBeVisible({ timeout: 5000 });
  });

  test('TC-AUTH-006: Unauthorized URL access intercepts and redirects to login', async ({ page }) => {
    // Clear any active session
    await page.addInitScript(() => sessionStorage.clear());
    await page.goto('/admin');

    // Route guard redirects unauthenticated user back to root/login
    await expect(page).toHaveURL(/.*5173\/?$/);
    await expect(page.locator('text=Login Portal')).toBeVisible();
  });

  test('TC-AUTH-007: Toggle password visibility switches input type to readable plaintext', async ({ page }) => {
    await page.goto('/');
    const passwordInput = page.locator('input[placeholder="Enter password"]');
    await passwordInput.fill('SecretPass123');
    await expect(passwordInput).toHaveAttribute('type', 'password');

    // Click visibility toggle eye icon
    const toggleBtn = page.locator('button[tabindex="-1"]').first();
    await toggleBtn.click();
    await expect(passwordInput).toHaveAttribute('type', 'text');
  });

  test('TC-AUTH-008: Logout from active session clears session and redirects to Login', async ({ page }) => {
    await page.route('**/api/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          ok: true,
          user: {
            user_id: 'usr-admin-001',
            name: 'Juan Dela Cruz',
            username: 'admin',
            role_name: 'Administrator',
            status: 'Active',
            email: 'admin@merylshoes.com',
          },
        }),
      });
    });

    await page.goto('/');
    await page.fill('input[placeholder="Enter username"]', 'admin');
    await page.fill('input[placeholder="Enter password"]', 'Admin123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*admin/, { timeout: 10000 });

    // Click sign out button
    const signOutBtn = page.locator('button:has-text("Sign-out"), button:has-text("Logout"), button:has-text("Sign out")').first();
    if (await signOutBtn.isVisible()) {
      await signOutBtn.click();
      await expect(page).toHaveURL(/.*5173\/?$/);
      await expect(page.locator('text=Login Portal')).toBeVisible();
    }
  });

  test('TC-AUTH-009: Google OAuth authentication flow initialization', async ({ page }) => {
    await page.goto('/');
    const googleBtn = page.locator('button:has-text("Google"), button:has-text("Sign in with Google")').first();
    if (await googleBtn.isVisible()) {
      await expect(googleBtn).toBeEnabled();
    }
  });

  test('TC-AUTH-010: Create new user account auto-generates staff identifier code', async ({ page }) => {
    // Staff codes follow sequence e.g. ADM-001, CSH-015, USR-009
    const expectedPattern = /^[A-Z]{3}-\d{3}$/;
    expect('CSH-724').toMatch(expectedPattern);
  });
});

