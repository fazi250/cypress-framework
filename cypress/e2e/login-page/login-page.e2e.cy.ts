import { generateTestCases, saveTestCasesToFile, type TestCases } from '../../support/test-data-generator';

const testCases: TestCases = generateTestCases(5);

describe('Login Page Tests', () => {
  before(() => {
    saveTestCasesToFile(testCases, 'cypress/fixtures/generated-test-cases.json');
  });

  it(testCases['TEAM-12300'].description, () => {
    cy.visit('https://www.nrsforu.com/iApp/rsc/myInvestmentPlannerDecisionEntry.x')
    cy.extractMainDOM()
  });
});
