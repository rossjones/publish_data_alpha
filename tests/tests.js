module.exports = {
  'Create a dataset' : function (browser) {
    browser
      .url('http://localhost:8000')
      .waitForElementVisible('h1', 1000)
      .assert.containsText(
        'h1',
        'Publish and update data for your organisation'
      )
      .click('a.button-get-started')
      .waitForElementVisible('main', 1000)
      .assert.containsText('h1', 'Sign in')
      .setValue('input[name=email]', 'a@b.c')
      .setValue('input[name=password]', 'foobar')
      .submitForm('form')
      .end();
  }
};
