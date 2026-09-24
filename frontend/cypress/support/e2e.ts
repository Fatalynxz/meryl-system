// Cypress E2E Support File
import './commands';

// Prevent uncaught application exceptions from failing tests
Cypress.on('uncaught:exception', (err, runnable) => {
  return false;
});

