module.exports = {
  'Create a dataset' : function (browser) {
    browser
      .url(process.env.APP_SERVER_URL)
      .waitForElementVisible('h1', 1000)
      .assert.containsText(
        'h1',
        'Publish and update data for your organisation'
      )
      .click('a.button-get-started')
      .waitForElementVisible('main', 1000)
      .assert.containsText('h1', 'Sign in')
      .setValue('input[name=email]', process.env.USER_EMAIL)
      .setValue('input[name=password]', process.env.USER_PASSWORD)
      .submitForm('form')
      .end();
  }
};
