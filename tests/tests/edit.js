var common = require('../common.js')

// ============ shortcut functions =============================================

var createDataset = function (browser) {
  return common.login(
      browser,
      process.env.USER_EMAIL, process.env.USER_PASSWORD
  )
    .clickAndCheckNextTitle('Create a dataset', 'Create a dataset')
    .clearSetValue('input[name=title]', 'My dataset')
    .clearSetValue('textarea[name=summary]', 'Summary of my dataset')
    .clearSetValue('textarea[name=description]', 'Description of my dataset')
    .submitFormAndCheckNextTitle(
      'Choose the organisation you are publishing for'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose a geographical area')
    .clearSetValue('input[id=id_location1]', 'England')
    .clearSetValue('input[id=id_location2]', 'Wales')
    .submitFormAndCheckNextTitle('How frequently is this dataset updated?')
    .selectRadioButton('Monthly')
    .submitFormAndCheckNextTitle('Add a link')
    .setValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .setValue('input[id=id_title]', 'Title of this link')
    .setValue('input[id=period_month]', '12')
    .setValue('input[id=period_year]', '2016')
    .submitFormAndCheckNextTitle('Links to your data')
    .clickAndCheckNextTitle(
      'Save and continue',
      'Add a link to supporting documents'
    )
    .setValue(
      'input[id=id_url]',
      'https://data.gov.uk/data/site-usage/data_all.csv'
    )
    .setValue('input[id=id_title]', 'Title of this link')
    .submitFormAndCheckNextTitle('Links to supporting documents')
    .clickAndCheckNextTitle('Save and continue', 'Get notifications')
    .selectRadioButton('Yes')
    .submitFormAndCheckNextTitle('Check your dataset')
    .submitFormAndCheckNextTitle('Your dataset has been published')
};


// ============ here start the tests ===========================================

var test_edit_title = function (browser) {
  createDataset(browser)
    .clickAndCheckNextTitle('Edit', 'Edit ‘My dataset’')
    .click('a[href*="edit"]')
    .clearSetValue('input[name=title]', 'Corrected title')
    .submitFormAndCheckNextTitle('Edit ‘Corrected title’')
    .submitFormAndCheckNextTitle('Your dataset has been edited')
    .assert.containsText('td', 'Corrected title')
    .deleteLastCreatedDataset()
    .end();
};

var test_edit_location = function (browser) {
  createDataset(browser)
    .clickAndCheckNextTitle('Edit', 'Edit ‘My dataset’')
    .click('a[href*="location"]')
    .assert.visible('#add1')
    .assert.hidden('#add2')
    .clearSetValue('input[id=id_location1]', 'London')
    .clickOnLink('Enter another area')
    .assert.hidden('#add1')
    .assert.visible('#add2')
    .clearSetValue('input[id=id_location2]', 'Paris')
    .clickOnLink('Remove')
    .clickOnLink('Enter another area')
    .clearSetValue('input[id=id_location2]', 'Berlin')
    .submitFormAndCheckNextTitle('Edit ‘My dataset’')
    .submitFormAndCheckNextTitle('Your dataset has been edited')
    .clickOnLink('Edit')
    .click('a[href*="location"]')
    .assert.valueContains('input[id=id_location1]', 'Paris')
    .assert.valueContains('input[id=id_location2]', 'Berlin')
    .assert.valueContains('input[id=id_location3]', '')
    .assert.hidden('#id_location3')
    .deleteLastCreatedDataset()
    .end();
};


module.exports = {
  'Edit a dataset title ': test_edit_title,
  'Edit a dataset location, ': test_edit_location
};
