import { LoginPage } from '../../pages/login-page/login-page.po';
import { generateTestCases, saveTestCasesToFile, type TestCases } from '../../support/test-data-generator';

const loginPage = new LoginPage();

// Generate test cases when file is loaded
const testCases: TestCases = generateTestCases(5);

describe('Login Page Tests', () => {
  before(() => {
    // Save generated test cases to JSON file for reference
    saveTestCasesToFile(testCases, 'cypress/fixtures/generated-test-cases.json');
  });

  // Example: Access specific test case by ID
  it(testCases['TEAM-12300'].description, () => {
    cy.visit(testCases['TEAM-12300'].url);
    const testData = testCases['TEAM-12300'].testData;
    cy.get('[name="username"]').type(testData.username);
    cy.get('[name="password"]').type(testData.password);
    cy.log(`Test executed with username: ${testData.username}`);
  });
});
