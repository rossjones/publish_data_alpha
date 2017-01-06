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

var goToCreateTitle = function(browser) {
  return login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset');
};

var goToCreateOrg = function(browser) {
  return goToCreateTitle(browser)
    .clearSetValue('input[name=title]', 'Title of my dataset')
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    );
};

var goToCreateLicence = function(browser) {
  return goToCreateOrg(browser)
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence');
};


var goToCreateRegion = function(browser) {
  return goToCreateLicence(browser)
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area');
};

var goToCreateFrequency = function(browser) {
  return goToCreateRegion(browser)
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?');
};

var goToNotifications = function(browser) {
  return goToCreateFrequency(browser)
    .selectRadioButton('Every year (January to December)')
    .submitFormAndCheckNextTitle('Add a link')
    .clearSetValue('input[id=id_url]', 'http://example.com/file.csv')
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=period_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .submitFormAndCheckNextTitle('Get notifications');
};

var goToCheckPage = function(browser) {
  return goToNotifications(browser)
    .selectRadioButton('Yes')
    .submitFormAndCheckNextTitle('Check your dataset');
};



// ============ here start the tests ===========================================

var test_failed_login = function(browser) {
  extended(browser)
    .url(process.env.APP_SERVER_URL)
    .waitForElementVisible('body', waitTimeout)
    .assert.containsText('h1', 'Publish and update data')
    .clickOnLink('Sign in')
    .waitForElementVisible('main', waitTimeout)
    .assert.containsText('h1', 'Sign in')
    .clearSetValue('input[name=email]', 'foo@bar.baz')
    .clearSetValue('input[name=password]', 'qux')
    .submitFormAndCheckNextTitle('There was a problem signing you in')
    .end()
};

var test_create_happy_path = function (browser) {
  login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .clearSetValue('input[name=title]', 'Title of my dataset')
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every month')
    .submitFormAndCheckNextTitle('Add a link')
    .setValue('input[id=id_url]', 'http://example.com/data.csv')
    .setValue('input[id=id_title]', 'Title of this link')
    .setValue('input[id=period_month]', '12')
    .setValue('input[id=period_year]', '2016')
    .submitFormAndCheckNextTitle('Dataset links')
    .submitFormAndCheckNextTitle('Get notifications')
    .selectRadioButton('Yes')
    .submitFormAndCheckNextTitle('Check your dataset')
    .submitFormAndCheckNextTitle('Your dataset has been published')
    .end();
};

var test_create_missing_title = function (browser) {
  goToCreateTitle(browser)
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a valid title')
    .clearSetValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
};

var test_create_invalid_title = function (browser) {
  goToCreateTitle(browser)
    .clearSetValue('input[name=title]', '][;')
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a valid title')
    .clearSetValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
};

var test_create_missing_description = function (browser) {
  goToCreateTitle(browser)
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .clearSetValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a description')
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
};

var test_create_missing_summary = function (browser) {
  goToCreateTitle(browser)
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .clearSetValue('input[name=title]', 'Title of my dataset')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a summary')
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .end();
};

var test_create_missing_org = function (browser) {
  goToCreateOrg(browser)
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please choose which organisation will own this dataset')
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .end();
};

var test_create_omit_licence = function (browser) {
  goToCreateLicence(browser)
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please select a licence for your dataset')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .end();
};

var test_create_blank_other_licence = function (browser) {
  goToCreateLicence(browser)
    .selectRadioButton('Other:')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please type the name of your licence')
    .clearSetValue('input[id=id_licence_other]', 'other licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .end();
};

var test_create_omit_region = function (browser) {
  goToCreateRegion(browser)
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please select the area that your dataset covers')
    .selectRadioButton('England')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .end();
};

var test_create_omit_frequency = function (browser) {
  goToCreateFrequency(browser)
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please indicate how often this dataset is updated')
    .selectRadioButton('Every day')
    .submitFormAndCheckNextTitle('Add a link')
    .end();
};

var test_create_daily = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every day')
    .submitFormAndCheckNextTitle('Add a link')
    .clearSetValue('input[id=id_url]', 'http://example.com/file.csv')
    .clearSetValue('input[id=id_title]', 'First link')
    .submitFormAndCheckNextTitle('Dataset links')
    .end();
};

var test_create_weekly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every week')
    .submitFormAndCheckNextTitle('Add a link')
    .clearSetValue('input[id=id_url]', 'http://example.com/file.csv')
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=start_day]', '30')
    .clearSetValue('input[id=start_month]', '01')
    .clearSetValue('input[id=start_year]', '2012')
    .clearSetValue('input[id=end_day]', '30')
    .clearSetValue('input[id=end_month]', '01')
    .clearSetValue('input[id=end_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another file')
    .clearSetValue('input[id=id_url]', 'http://example.com/file2.csv')
    .clearSetValue('input[id=id_title]', 'Second link')
    .clearSetValue('input[id=start_day]', '30')
    .clearSetValue('input[id=start_month]', '01')
    .clearSetValue('input[id=start_year]', '2013')
    .clearSetValue('input[id=end_day]', '30')
    .clearSetValue('input[id=end_month]', '01')
    .clearSetValue('input[id=end_year]', '2014')
    .submitFormAndCheckNextTitle('Dataset links')
    .assert.containsText('table', 'First link')
    .assert.containsText('table', 'Second link')
    .end();
};

var test_create_monthly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every month')
    .submitFormAndCheckNextTitle('Add a link')
    .clearSetValue('input[id=id_url]', 'http://example.com/file.csv')
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=period_month]', '12')
    .clearSetValue('input[id=period_year]', '2012')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another file')
    .clearSetValue('input[id=id_url]', 'http://example.com/file2.csv')
    .clearSetValue('input[id=id_title]', 'Second link')
    .clearSetValue('input[id=period_month]', '12')
    .clearSetValue('input[id=period_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .assert.containsText('table', 'First link')
    .assert.containsText('table', 'Second link')
    .end();
};

var test_create_quarterly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every quarter')
    .submitFormAndCheckNextTitle('Add a link')
    .clearSetValue('input[id=id_url]', 'http://example.com/file.csv')
    .clearSetValue('input[id=id_title]', 'First link')
    .selectRadioButton('Q2 (July to September)')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another file')
    .clearSetValue('input[id=id_url]', 'http://example.com/file2.csv')
    .clearSetValue('input[id=id_title]', 'Second link')
    .selectRadioButton('Q3 (October to December)')
    .submitFormAndCheckNextTitle('Dataset links')
    .assert.containsText('table', 'First link')
    .assert.containsText('table', 'Second link')
    .end();
};

var test_create_never = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Never')
    .submitFormAndCheckNextTitle('Add a link')
    .end();
};

var test_create_yearly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every year (January to December)')
    .submitFormAndCheckNextTitle('Add a link')
    .clearSetValue('input[id=id_url]', 'http://example.com/file.csv')
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=period_year]', '2012')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another file')
    .clearSetValue('input[id=id_url]', 'http://example.com/file2.csv')
    .clearSetValue('input[id=id_title]', 'Second link')
    .clearSetValue('input[id=period_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .assert.containsText('table', 'First link')
    .assert.containsText('table', 'Second link')
    .end();
};

var test_create_omit_notifications = function (browser) {
  goToNotifications(browser)
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please specify if you\'d like to receive notifications')
    .end();
};

var test_create_omit_url = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every year (January to December)')
    .submitFormAndCheckNextTitle('Add a link')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a valid title')
    .checkError('Please provide a valid URL')
    .end();
};

var test_create_modify_after_check = function (browser) {
  goToCheckPage(browser)
    .clickOnLink('Change')
    .waitForElementVisible('h1', waitTimeout)
    .assert.containsText('h1', 'Create a dataset')
    .clearSetValue('input[name=title]', 'modified name')
    .submitFormAndCheckNextTitle('Check your dataset')
    .assert.containsText('body', 'modified name')
    .end();
};


var test_dashboard = function (browser) {
  login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .assert.containsText('main', 'Update datasets')
    .assert.containsText('main', 'Fix datasets')
    .end()
};


module.exports = {
  'Failed login': test_failed_login,
  'Create a dataset, happy path': test_create_happy_path,
  'Create a dataset, missing title' : test_create_missing_title,
  'Create a dataset, invalid title' : test_create_invalid_title,
  'Create a dataset, missing description' : test_create_missing_description,
  'Create a dataset, missing summary' : test_create_missing_summary,
  'Create a dataset, omit organisation' : test_create_missing_org,
  'Create a dataset, omit licence' : test_create_omit_licence,
  'Create a dataset, blank other licence' : test_create_blank_other_licence,
  'Create a dataset, omit region' : test_create_omit_region,
  'Create a dataset, omit frequency' : test_create_omit_frequency,
  'Create a dataset, frequency daily' : test_create_daily,
  'Create a dataset, frequency weekly' : test_create_weekly,
  'Create a dataset, frequency monthly' : test_create_monthly,
  'Create a dataset, frequency quarterly' : test_create_quarterly,
  'Create a dataset, frequency never' : test_create_never,
  'Create a dataset, frequency yearly' : test_create_yearly,
  'Create a dataset, omit notifications' : test_create_omit_notifications,
  'Create a dataset, omit url' : test_create_omit_url,
  'Create a dataset, modify after check' : test_create_modify_after_check,

  'Dashboard' : test_dashboard
};
