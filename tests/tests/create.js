var common = require('../common.js')

// ============ shortcut functions =============================================

var goToCreateTitle = function(browser) {
  return common.login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
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
    .clearSetValue('input[id=id_location1]', 'England')
    .clearSetValue('input[id=id_location2]', 'Wales')
    .submitFormAndCheckNextTitle('How often is this dataset updated?');
};

var goToDocumentation = function(browser) {
  return goToCreateFrequency(browser)
    .selectRadioButton('Every year (January to December)')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=period_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickAndCheckNextTitle(
      'Save and continue',
      'Do you have supporting documentation?'
    );
};

var goToNotifications = function(browser) {
  return goToDocumentation(browser)
    .selectRadioButton('Yes')
    .clearSetValue('input[id=id_title]', 'A document')
    .clearSetValue(
      'input[id=id_url]', 'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .submitFormAndCheckNextTitle('Dataset documentation')
    .clickAndCheckNextTitle('Save and continue', 'Get notifications')
};

var goToCheckPage = function(browser) {
  return goToNotifications(browser)
    .submitFormAndCheckNextTitle('Check your dataset');
};

var createDataset = function(browser) {
  return goToCheckPage()
    .submitFormAndCheckNextTitle('Your dataset has been published');
};



// ============ here start the tests ===========================================


var test_create_happy_path = function (browser) {
  var dataSetTitle = 'Test dataset ' + new Date();
  common.login(browser, process.env.USER_EMAIL, process.env.USER_PASSWORD)
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .clearSetValue('input[name=title]', dataSetTitle)
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .clearSetValue('input[id=id_location1]', 'England, Wales')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every month')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .setValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .setValue('input[id=id_title]', 'Title of this link')
    .setValue('input[id=period_month]', '12')
    .setValue('input[id=period_year]', '2016')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickAndCheckNextTitle(
      'Save and continue',
      'Do you have supporting documentation?'
    )
    .selectRadioButton('Yes')
    .setValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .setValue('input[id=id_title]', 'Title of this link')
    .submitFormAndCheckNextTitle('Dataset documentation')
    .clickAndCheckNextTitle('Save and continue', 'Get notifications')
    .selectRadioButton('Yes')
    .submitFormAndCheckNextTitle('Check your dataset')
    .assert.containsText('table', 'Open Government Licence')
    .submitFormAndCheckNextTitle('Your dataset has been published')
    .deleteLastCreatedDataset()
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
    .deleteLastCreatedDataset()
    .end();
};

var test_create_omit_licence = function (browser) {
  goToCreateLicence(browser)
    .submitFormAndCheckNextTitle('Choose an area')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_blank_other_licence = function (browser) {
  goToCreateLicence(browser)
    .selectRadioButton('Other:')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please type the name of your licence')
    .clearSetValue('input[id=id_licence_other]', 'other licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_omit_region = function (browser) {
  goToCreateRegion(browser)
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_region_autocomplete = function (browser) {
  goToCreateRegion(browser)
    .clearSetValue('input[id=id_location1]', 'Swa')
    .waitForElementVisible('div[role=listbox]', 5000)
    .assert.containsText('div[role=listbox]', 'Swansea (local authority)')
    .deleteLastCreatedDataset()
    .end();
};


var test_create_omit_frequency = function (browser) {
  goToCreateFrequency(browser)
    .submitFormAndCheckNextTitle('Do you have supporting documentation?')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_daily = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every day')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'First link')
    .submitFormAndCheckNextTitle('Dataset links')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_daily_omit_link = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every day')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .clearSetValue('input[id=id_title]', 'First link')
    .submitFormAndCheckNextTitle('There was a problem')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_daily_nolink = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every day')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('No')
    .submitFormAndCheckNextTitle('Do you have supporting documentation')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_weekly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every week')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=start_day]', '30')
    .clearSetValue('input[id=start_month]', '01')
    .clearSetValue('input[id=start_year]', '2012')
    .clearSetValue('input[id=end_day]', '30')
    .clearSetValue('input[id=end_month]', '01')
    .clearSetValue('input[id=end_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another link')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
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
    .deleteLastCreatedDataset()
    .end();
};

var test_create_monthly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every month')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=period_month]', '12')
    .clearSetValue('input[id=period_year]', '2012')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another link')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'Second link')
    .clearSetValue('input[id=period_month]', '12')
    .clearSetValue('input[id=period_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .assert.containsText('table', 'First link')
    .assert.containsText('table', 'Second link')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_quarterly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every quarter')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'First link')
    .selectRadioButton('Q2 (July to September)')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another link')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'Second link')
    .selectRadioButton('Q3 (October to December)')
    .clearSetValue('input[id=period_year]', '1984')
    .submitFormAndCheckNextTitle('Dataset links')
    .assert.containsText('table', 'First link')
    .assert.containsText('table', 'Second link')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_never = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Never')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_yearly = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every year (January to December)')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'First link')
    .clearSetValue('input[id=period_year]', '2012')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickOnLink('Add another link')
    .clearSetValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .clearSetValue('input[id=id_title]', 'Second link')
    .clearSetValue('input[id=period_year]', '2013')
    .submitFormAndCheckNextTitle('Dataset links')
    .assert.containsText('table', 'First link')
    .assert.containsText('table', 'Second link')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_omit_notifications = function (browser) {
  goToNotifications(browser)
    .submitFormAndCheckNextTitle('Check your dataset')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_omit_url = function (browser) {
  goToCreateFrequency(browser)
    .selectRadioButton('Every year (January to December)')
    .submitFormAndCheckNextTitle('Do you have a link to the data?')
    .selectRadioButton('Yes')
    .submitFormAndCheckNextTitle('There was a problem')
    .checkError('Please provide a valid title')
    .checkError('Please provide a valid URL')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_modify_title = function (browser) {
  goToCheckPage(browser)
    .clickOnLink('Change')
    .waitForElementVisible('h1', common.waitTimeout)
    .assert.containsText('h1', 'Change your dataset\'s details')
    .clearSetValue('input[name=title]', 'modified name')
    .submitFormAndCheckNextTitle('Check your dataset')
    .assert.containsText('body', 'modified name')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_modify_licence = function (browser) {
  goToCheckPage(browser)
    .click('a[href*="licence"]')
    .waitForElementVisible('h1', common.waitTimeout)
    .assert.containsText('h1', 'Choose a licence')
    .selectRadioButton('Other')
    .clearSetValue('input[id=id_licence_other]', 'my licence')
    .submitFormAndCheckNextTitle('Check your dataset')
    .waitForElementVisible('body', common.waitTimeout)
    .assert.containsText('body', 'my licence')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_remove_link = function (browser) {
  goToCheckPage(browser)
    .click('a[href*="files"]')
    .waitForElementVisible('h1', common.waitTimeout)
    .assert.containsText('h1', 'Dataset links')
    .clickAndCheckNextTitle('Delete', 'Dataset links')
    .clickAndCheckNextTitle('Save and continue', 'Check your dataset')
    .deleteLastCreatedDataset()
    .end();
};

var test_create_remove_doc = function (browser) {
  goToCheckPage(browser)
    .click('a[href*="documents"]')
    .waitForElementVisible('h1', common.waitTimeout)
    .assert.containsText('h1', 'Dataset documentation')
    .clickAndCheckNextTitle('Delete', 'Dataset documentation')
    .clickAndCheckNextTitle('Save and continue', 'Check your dataset')
    .deleteLastCreatedDataset()
    .end();
};

module.exports = {
  'Create a dataset, happy path': test_create_happy_path,
  'Create a dataset, missing title': test_create_missing_title,
  'Create a dataset, invalid title': test_create_invalid_title,
  'Create a dataset, missing description': test_create_missing_description,
  'Create a dataset, missing summary': test_create_missing_summary,
  'Create a dataset, omit organisation': test_create_missing_org,
  'Create a dataset, omit licence': test_create_omit_licence,
  'Create a dataset, blank other licence': test_create_blank_other_licence,
  'Create a dataset, omit region': test_create_omit_region,
  'Create a dataset, region autocomplete': test_create_region_autocomplete,
  'Create a dataset, omit frequency': test_create_omit_frequency,
  'Create a dataset, frequency daily': test_create_daily,
  'Create a dataset, frequency daily, no link': test_create_daily_nolink,
  'Create a dataset, frequency daily, omit link': test_create_daily_omit_link,
  'Create a dataset, frequency weekly': test_create_weekly,
  'Create a dataset, frequency monthly': test_create_monthly,
  'Create a dataset, frequency quarterly': test_create_quarterly,
  'Create a dataset, frequency never': test_create_never,
  'Create a dataset, frequency yearly': test_create_yearly,
  'Create a dataset, omit notifications': test_create_omit_notifications,
  'Create a dataset, omit url': test_create_omit_url,
  'Create a dataset, modify title': test_create_modify_title,
  'Create a dataset, modify licence': test_create_modify_licence,
  'Create a dataset, remove link after check': test_create_remove_link,
  'Create a dataset, remove doc after check': test_create_remove_doc
};
