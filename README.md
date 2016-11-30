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
./manage.py migrate
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
