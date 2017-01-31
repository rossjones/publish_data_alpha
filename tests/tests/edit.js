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
      'Which organisation are you publishing this dataset for?'
    )
    .selectRadioButton('Cabinet Office')
    .submitFormAndCheckNextTitle('Choose a licence')
    .selectRadioButton('Open Government Licence')
    .submitFormAndCheckNextTitle('Choose an area')
    .clearSetValue('input[id=id_location1]', 'England')
    .clearSetValue('input[id=id_location2]', 'Wales')
    .submitFormAndCheckNextTitle('How often is this dataset updated?')
    .selectRadioButton('Every month')
    .submitFormAndCheckNextTitle('Add a link')
    .setValue('input[id=id_url]', 'http://example.com/data.csv')
    .setValue('input[id=id_title]', 'Title of this link')
    .setValue('input[id=period_month]', '12')
    .setValue('input[id=period_year]', '2016')
    .submitFormAndCheckNextTitle('Dataset links')
    .clickAndCheckNextTitle('Save and continue', 'Add documentation')
    .setValue('input[id=id_url]', 'http://example.com/data.csv')
    .setValue('input[id=id_title]', 'Title of this link')
    .submitFormAndCheckNextTitle('Dataset documentation')
    .clickAndCheckNextTitle('Save and continue', 'Get notifications')
    .selectRadioButton('Yes')
    .submitFormAndCheckNextTitle('Check your dataset')
    .submitFormAndCheckNextTitle('Your dataset has been published')
};


// ============ here start the tests ===========================================

var test_edit_title = function (browser) {
  createDataset(browser)
    .clickAndCheckNextTitle('Edit', 'Edit ‘My dataset’')
    .clearSetValue('input[name=title]', 'Corrected title')
    .submitFormAndCheckNextTitle('Your dataset has been edited')
    .assert.containsText('td', 'Corrected title')
    .deleteLastCreatedDataset()
    .end();
};

var test_edit_location = function (browser) {
  createDataset(browser)
    .clickAndCheckNextTitle('Edit', 'Edit ‘My dataset’')
    .assert.visible('#add1')
    .assert.hidden('#add2')
    .clearSetValue('input[id=id_location1]', 'London')
    .clickOnLink('Add another area')
    .assert.hidden('#add1')
    .assert.visible('#add2')
    .clearSetValue('input[id=id_location2]', 'Paris')
    .clickOnLink('Remove')
    .clickOnLink('Add another area')
    .clearSetValue('input[id=id_location2]', 'Berlin')
    .submitFormAndCheckNextTitle('Your dataset has been edited')
    .clickOnLink('Edit')
    .assert.valueContains('input[id=id_location1]', 'Paris')
    .assert.valueContains('input[id=id_location2]', 'Berlin')
    .assert.valueContains('input[id=id_location3]', '')
    .assert.hidden('#id_location3')
    .clickOnLink('Delete this dataset')
    .end();
};


module.exports = {
  'Edit a dataset, ': test_edit_title,
  'Edit a dataset location, ': test_edit_location
};
