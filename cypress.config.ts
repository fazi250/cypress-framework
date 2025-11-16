import { defineConfig } from 'cypress';

export default defineConfig({
  defaultCommandTimeout: 20000,
  e2e: {
    setupNodeEvents(on: Cypress.PluginEvents, config: Cypress.PluginConfigOptions): Cypress.PluginConfigOptions {
      const { plugin } = require('@cypress/grep/plugin');
      plugin(config);
      on('task', {
        log(message: string): null {
          console.log(message);
          return null;
        }
      });
      return config;
    },
    specPattern: 'cypress/e2e/**/*.e2e.cy.ts',
    experimentalPromptCommand: true,
  },
});