/// <reference types="cypress" />

declare namespace Cypress {
  interface SuiteConfigOverrides {
    /**
     * Tag(s) for the test suite. Use with @cypress/grep to filter tests.
     * Can be a single tag string or an array of tag strings.
     * @example { tags: '@smoke' }
     * @example { tags: ['@smoke', '@regression'] }
     */
    tags?: string | string[];
  }

  interface TestConfigOverrides {
    /**
     * Tag(s) for the test. Use with @cypress/grep to filter tests.
     * Can be a single tag string or an array of tag strings.
     * @example { tags: '@smoke' }
     * @example { tags: ['@smoke', '@regression'] }
     */
    tags?: string | string[];
  }
}
