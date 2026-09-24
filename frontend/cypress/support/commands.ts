/// <reference types="cypress" />

declare namespace Cypress {
  interface Chainable {
    loginAs(username: string, roleName: string): Chainable<void>;
  }
}

Cypress.Commands.add('loginAs', (username: string, roleName: string) => {
  cy.intercept('POST', '**/api/auth/login', {
    statusCode: 200,
    body: {
      ok: true,
      user: {
        user_id: `usr-${username}-01`,
        name: username.toUpperCase(),
        username: username,
        role_name: roleName,
        status: 'Active',
        email: `${username}@merylshoes.com`,
      },
    },
  }).as('loginMock');

  cy.intercept('GET', '**/api/auth/me', {
    statusCode: 200,
    body: {
      ok: true,
      user: {
        user_id: `usr-${username}-01`,
        name: username.toUpperCase(),
        username: username,
        role_name: roleName,
        status: 'Active',
        email: `${username}@merylshoes.com`,
      },
    },
  }).as('meMock');

  cy.visit('/');
  cy.get('input[placeholder="Enter username"]').clear().type(username);
  cy.get('input[placeholder="Enter password"]').clear().type('ValidPass123');
  cy.get('button[type="submit"]').click();

  const expectedPath = roleName.toLowerCase().includes('admin')
    ? '/admin'
    : roleName.toLowerCase().includes('sales')
    ? '/sales'
    : '/inventory';

  cy.url({ timeout: 10000 }).should('include', expectedPath);
});

