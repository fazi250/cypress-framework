import { defineConfig } from 'cypress';
import { getLatestVerificationCode } from './cypress/support/puppeteer-stealth';
import { allureCypress } from 'allure-cypress/reporter';

export default defineConfig({
  defaultCommandTimeout: 20000,
  pageLoadTimeout: 120000,
  chromeWebSecurity: false,
  e2e: {
    setupNodeEvents(on: Cypress.PluginEvents, config: Cypress.PluginConfigOptions): Cypress.PluginConfigOptions {
      const { plugin } = require('@cypress/grep/plugin');
      plugin(config);
      on('task', {
        log(message: string): null {
          console.log(message);
          return null;
        },
        async fetchSmsCode(url: string): Promise<string | null> {
          try {
            const code = await getLatestVerificationCode(url);
            return code;
          } catch (error) {
            console.error('Error fetching SMS code:', error);
            return null;
          }
        }
      });
      allureCypress(on, config, {
        resultsDir: "allure-results",
      });
      return config;
    },
    specPattern: 'cypress/e2e/**/*.e2e.cy.ts',
    experimentalPromptCommand: true,
  },
});

//git add . ; git commit --amend --no-edit ; git push --force-with-lease
//npx cypress run --env grepTags="das",grepFilterSpecs=true