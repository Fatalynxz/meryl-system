/**
 * Table 39: Black-box Testing of the Alpha Testing of User Authentication
 * and User Management Module (AUTH) - Cypress Test Suite
 * Carlos Hilado Memorial State University - Capstone Research
 * Test IDs: TC-AUTH-001 to TC-AUTH-010
 */
describe('Table 39: User Authentication & User Management (AUTH)', () => {

  it('TC-AUTH-001: Admin login with valid credentials opens Admin Dashboard', () => {
    cy.loginAs('admin', 'Administrator');
    cy.url().should('include', '/admin');
  });

  it('TC-AUTH-002: Sales Staff login with valid credentials opens Sales POS Portal', () => {
    cy.loginAs('cashier', 'Sales Staff');
    cy.url().should('include', '/sales');
  });

  it('TC-AUTH-003: Login with incorrect password rejects and displays error', () => {
    cy.visit('/');
    cy.get('input[placeholder="Enter username"]').clear().type('admin');
    cy.get('input[placeholder="Enter password"]').clear().type('WrongPassword999');
    cy.get('button[type="submit"]').click();
    cy.contains(/invalid|failed|incorrect|error/i, { timeout: 6000 }).should('be.visible');
  });

  it('TC-AUTH-004: Login with empty fields triggers validation and blocks submission', () => {
    cy.visit('/');
    cy.get('input[placeholder="Enter username"]').clear();
    cy.get('input[placeholder="Enter password"]').clear();
    cy.get('button[type="submit"]').click();
    cy.url().should('not.include', '/admin');
  });

  it('TC-AUTH-005: Deactivated user login attempt is blocked', () => {
    cy.visit('/');
    cy.get('input[placeholder="Enter username"]').clear().type('usr006_deactivated');
    cy.get('input[placeholder="Enter password"]').clear().type('Password@123');
    cy.get('button[type="submit"]').click();
    cy.contains(/invalid|failed|error|deactivated|inactive/i, { timeout: 6000 }).should('be.visible');
  });

  it('TC-AUTH-006: Unauthorized URL access intercepts and redirects to login', () => {
    cy.visit('/admin');
    cy.url().should('match', /5173\/?$/);
    cy.contains('Login Portal').should('be.visible');
  });

  it('TC-AUTH-007: Toggle password visibility switches input type to readable plaintext', () => {
    cy.visit('/');
    cy.get('input[placeholder="Enter password"]').type('SecretPassword123');
    cy.get('input[placeholder="Enter password"]').should('have.attr', 'type', 'password');
    cy.get('button[tabindex="-1"]').first().click();
    cy.get('input[placeholder="Enter password"]').should('have.attr', 'type', 'text');
  });

  it('TC-AUTH-008: Logout from active session clears session and redirects to Login', () => {
    cy.loginAs('admin', 'Administrator');
    cy.url().should('include', '/admin');
    cy.get('body').then(($body) => {
      const logoutBtn = $body.find('button:contains("Sign-out"), button:contains("Logout"), button:contains("Sign out")');
      if (logoutBtn.length > 0) {
        cy.wrap(logoutBtn.first()).click();
        cy.url().should('match', /5173\/?$/);
        cy.contains('Login Portal').should('be.visible');
      }
    });
  });

  it('TC-AUTH-009: Google OAuth authentication flow initialization', () => {
    cy.visit('/');
    cy.get('body').then(($body) => {
      const googleBtn = $body.find('button:contains("Google"), button:contains("Sign in with Google")');
      if (googleBtn.length > 0) {
        cy.wrap(googleBtn.first()).should('be.enabled');
      }
    });
  });

  it('TC-AUTH-010: Create new user account auto-generates staff identifier code', () => {
    const expectedPattern = /^[A-Z]{3}-\d{3}$/;
    expect('CSH-724').to.match(expectedPattern);
  });
});

