var common = require('../common.js')

var before = function(browser) {
  console.log('Setting up...');
  common.login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD);
}

var test_dashboard = function (browser) {
  browser
    .assert.containsText('main', 'Update datasets')
    .assert.containsText('main', 'Fix datasets')
    .end()
};


module.exports = {
  before: before,
  'Dashboard': test_dashboard
};
