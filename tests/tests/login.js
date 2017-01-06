var common = require('../common.js')

var test_login = function(browser) {
  common.extended(browser)
    .url(process.env.APP_SERVER_URL)
    .waitForElementVisible('body', common.waitTimeout)
    .assert.containsText('h1', 'Publish and update data')
    .clickOnLink('Sign in')
    .waitForElementVisible('main', common.waitTimeout)
    .assert.containsText('h1', 'Sign in')
    .clearSetValue('input[name=email]', process.env.USER_EMAIL)
    .clearSetValue('input[name=password]', process.env.USER_PASSWORD)
    .submitFormAndCheckNextTitle('Dashboard')
    .end();
};

var test_failed_login = function(browser) {
  common.extended(browser)
    .url(process.env.APP_SERVER_URL)
    .waitForElementVisible('body', common.waitTimeout)
    .assert.containsText('h1', 'Publish and update data')
    .clickOnLink('Sign in')
    .waitForElementVisible('main', common.waitTimeout)
    .assert.containsText('h1', 'Sign in')
    .clearSetValue('input[name=email]', 'foo@bar.baz')
    .clearSetValue('input[name=password]', 'qux')
    .submitFormAndCheckNextTitle('There was a problem signing you in')
    .end();
};


module.exports = {
  'Successful login': test_login,
  'Failed login': test_failed_login
}
