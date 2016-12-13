[![Build Status](https://travis-ci.org/datagovuk/publish_data_alpha.svg)](https://travis-ci.org/datagovuk/publish_data_alpha)


# Publish Data

This repository contains the alpha-stage data publishing component of data.gov.uk.

## Development

To use this repository for development you should run the following tasks to setup the environment:

```bash
git clone <REPO>
cd publish_data_alpha
vagrant up
vagrant ssh
cd /vagrant/tools
sudo bash dev_setup.sh
. dev_run.sh
```

After a few minutes you should see the site at http://192.168.99.99:8000

Alternatively to just run on your machine with Sqlite3

``` bash
# Make and active a virtualenv for Python 3
git clone <REPO>
cd publish_data_alpha
pip install -r requirements.txt
cd src
export DJANGO_SETTINGS_MODULE="publish_data.settings.dev"
./manage.py migrate
./manage.py loaddata tasks
./manage.py loaddata stats
./manage.py runserver
```

### Configuration

To successfully run the server, you will require a local_settings.py file that is stored in ```src/publish_data/settings/local_settings.py```.  The file should have the following contents:

```python


# CKAN specific settings.
CKAN_HOST = "URL of a CKAN Server"
CKAN_ADMIN = "An administrators API Key"

# Username - test-co
CKAN_TEST_USER = "The API key of a test user"

```

## Importing test users

In order to put test users to use the service, you can run
```
./manage.py import_test_users -f users.json
```

The file should be structured as:
```
[
    {
      "username": "username",
      "email" : "email_address",
      "password": "password",
      "apikey": "apikey"
    }
]
```

### To create a migration

Create your model and then

```
cd src
./manage makemigrations <optional_app_name>
```

### To run migrations

```
cd src
./manage migrate
```


## Apps

In the src/ directory are the following apps:

    * publish_data - The main app repo containing settings and base templates/resources
    * userauth - Handle user authentication with pre-set users (and admin)


## Static assets (CSS, JS, images)

This application is built using [govuk_elements](https://github.com/alphagov/govuk_elements)
and [govuk_template](https://github.com/alphagov/govuk_template/).

Assets from those packages are already included in this repository.
Additionally the SCSS in `govuk_elements` is precompiled and the
resulting CSS is also included in the repository.

The reason assets are copied and pre-compiled here is to simplify
deployments.  That way, we're avoiding retrieving the `govuk_`
repositories, compiling the SASS (which would require installing
nodejs and npm), concatenating and minifying.

As a consequence, if changes are made to the javascript or SCSS files,
the developer will have to recompile locally. This will require
installing nodejs and npm, and running the following steps:

```
> npm install
> gulp styles
> gulp javascripts
```

If a new version of the `govuk` packages is needed, you will have to
copy and compile them again, and add the resulting files in this
repository.


## Acceptance testing

End-to-end tests can be found in the `tests` directory. They are run using
[nightwatch](http://nightwatchjs.com). To install nightwatch, use:
`npm install -g nightwatch`.

The variables at the top of the `Makefile` should be set to suit your
local environment.

Then you can just run `make test` to run the test suite.
