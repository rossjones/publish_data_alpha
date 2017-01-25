var waitTimeout = 1000; // milliseconds

var extended = function(browser) {
  browser.clickOn = function(element, text) {
    return this
      .useXpath()
      .click('//' + element + '[contains(text(), "'+text+'")]')
      .useCss();
  };
  browser.clickOnLink = function(text) {
    return this.clickOn('a', text);
  };
  browser.clickOnButton = function(text) {
    return this.clickOn('button', text);
  };
  browser.selectRadioButton = function(text) {
    return this
      .useXpath()
      .click('//label[contains(span/text(), "'+text+'")]')
      .useCss();
  };
  browser.submitFormAndCheckNextTitle = function(title) {
    return this
      .submitForm('form')
      .waitForElementVisible('h1', waitTimeout)
      .assert.containsText('h1', title);
  };
  browser.clickAndCheckNextTitle = function(linkText, title) {
    return this
      .clickOnLink(linkText)
      .waitForElementVisible('h1', waitTimeout)
      .assert.containsText('h1', title);
  };
  browser.checkError = function(text) {
    return this
      .assert.containsText('ul.error-summary-list', text);
  };
  browser.checkFormInput = function(name) {
    return this
      .assert.elementPresent('input[name=' + name + ']');
  };
  browser.clearSetValue = function(selector, value) {
    return this
      .clearValue(selector).setValue(selector, value);
  };

  browser.deleteLastCreatedDataset = function() {
    return this
      .clickOnLink('Manage your data')
      .clickOnLink('Edit')
      .clickOnLink('Delete this dataset');
  };

  return browser;
}

var login = function(browser, email, password) {
  extended(browser)
    .url(process.env.APP_SERVER_URL)
    .waitForElementVisible('body', waitTimeout)
    .assert.containsText('h1', 'Publish and update data')
    .clickOnLink('Sign in')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'Sign in')
    .clearSetValue('input[name=email]', email)
    .clearSetValue('input[name=password]', password)
    .submitFormAndCheckNextTitle('Dashboard');
  return browser;
};

module.exports = {
  waitTimeout: waitTimeout,
  extended: extended,
  login: login
};
