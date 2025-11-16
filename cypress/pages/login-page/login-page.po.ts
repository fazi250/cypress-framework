export class LoginPage {
  // Method to get the loading indicator inside the shadow DOM
  getLoadingIndicator() {
    return cy.get('bolt-waiting-indicator').shadow().find('.bolt-waiting-indicator-wc--spinner');
  }

  // Method to get the "Discover how" button
  getDiscoverHowButton() {
    return cy.get('a.button.nw-button--mint');
  }

  // Method to get the "Take the tour" button
  getTakeTheTourButton() {
    return cy.get('a[title="opens in a new window"][role="button"]');
  }

  // Method to get the "Enroll today" button
  getEnrollTodayButton() {
    return cy.get('a[title="opens in a new window"][role="button"][href="/iApp/rsc/enrollment.x"]');
  }

  // Method to get the "Find out how" button
  getFindOutHowButton() {
    return cy.get('a[href="/rsc-preauth/learn-about-retirement/close-to-or-living-in-retirement/articles/stay-in-your-plan"]');
  }

  // Method to get the "Create an account" button
  getCreateAccountButton() {
    return cy.get('a[href="/iApp/rsc/establishUserIdentify.x"]');
  }

  // Method to get the "Review our materials" button
  getReviewMaterialsButton() {
    return cy.get('a[href="/rsc-preauth/learn-about-retirement/"]');
  }

  // Method to get the "Cyber insights" link
  getCyberInsightsLink() {
    return cy.get('a[href="/rsc-preauth/forms-and-resources/cyber-security-center/"]');
  }

  // Method to get the "Webinars" link
  getWebinarsLink() {
    return cy.get('a[href="/rsc-preauth/learn-about-retirement/webinars/"]');
  }

  // Method to get the "Retirement planner" link
  getRetirementPlannerLink() {
    return cy.get('a[href="/rsc-preauth/tools-and-calculators/mirp-overview/"]');
  }
}