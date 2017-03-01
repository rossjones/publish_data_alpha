var common = require('../common.js')

var beforeEach = function(browser) {
  common.login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD);
}

var test_dashboard = function(browser) {
  browser
    .assert.containsText('main', 'Update datasets')
    .assert.containsText('main', 'Fix datasets')
    .end()
};

var test_dashboard_show_hide = function(browser) {
  browser
    .assert.visible('section:first-of-type table tr:nth-of-type(3)')
    .assert.hidden('section:first-of-type table tr:nth-of-type(5)')
    .click('section:first-of-type a.toggle')
    .assert.visible('section:first-of-type table tr:nth-of-type(3)')
    .assert.visible('section:first-of-type table tr:nth-of-type(5)')
    .click('section:first-of-type a.toggle')
    .assert.visible('section:first-of-type table tr:nth-of-type(3)')
    .assert.hidden('section:first-of-type table tr:nth-of-type(5)')
    .end();
};

module.exports = {
  'beforeEach': beforeEach,
  'Dashboard': test_dashboard,
  'Dashboard show/hide section': test_dashboard_show_hide
};
