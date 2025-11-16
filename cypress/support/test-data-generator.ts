// Test Data Generator - Generates random test cases with Jira IDs

export interface TestData {
    username: string;
    password: string;
    email?: string;
    expectedResult?: string;
}

export interface TestCase {
    id: string;
    url: string;
    description: string;
    testSteps: string[];
    testData: TestData;
}

export interface TestCases {
    [key: string]: TestCase;
}

/**
 * Generates random test cases for Cypress tests
 * @param count - Number of test cases to generate
 * @returns Object containing test cases indexed by their Jira ID
 */
export function generateTestCases(count: number = 5): TestCases {
    const testCases: TestCases = {};

    const descriptions = [
        'Verify login with valid credentials',
        'Verify login with invalid credentials',
        'Verify login with empty username',
        'Verify login with empty password',
        'Verify login with special characters',
        'Verify password field masking',
        'Verify forgot password link',
        'Verify remember me functionality'
    ];

    const usernames = ['testuser1', 'admin@test.com', 'john.doe', 'invalid_user', ''];
    const passwords = ['Password123!', 'wrongpass', '', 'test@123', '12345'];
    const expectedResults = ['success', 'error', 'validation_error'];

    for (let i = 0; i < count; i++) {
        const jiraId = `TEAM-${12300 + i}`;
        const descIndex = i % descriptions.length;

        testCases[jiraId] = {
            id: jiraId,
            url: 'https://www.nrsforu.com/iApp/rsc/login.x',
            description: descriptions[descIndex],
            testSteps: [
                'Navigate to login page',
                'Enter username',
                'Enter password',
                'Click login button',
                'Verify result'
            ],
            testData: {
                username: usernames[i % usernames.length],
                password: passwords[i % passwords.length],
                email: `test${i}@example.com`,
                expectedResult: expectedResults[i % expectedResults.length]
            }
        };
    }

    return testCases;
}

/**
 * Saves test cases to a JSON file
 * @param testCases - Test cases object to save
 * @param filePath - Path where to save the JSON file
 */
export function saveTestCasesToFile(testCases: TestCases, filePath: string = 'cypress/fixtures/test-cases.json'): void {
    cy.writeFile(filePath, testCases);
}

/**
 * Loads test cases from a JSON file
 * @param filePath - Path to the JSON file
 * @returns Promise containing test cases
 */
export function loadTestCasesFromFile(filePath: string = 'cypress/fixtures/test-cases.json'): Cypress.Chainable<TestCases> {
    return cy.readFile(filePath);
}
