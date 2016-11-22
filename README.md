[![Build Status](https://travis-ci.org/datagovuk/publish_data_alpha.svg)](https://travis-ci.org/datagovuk/publish_data_alpha)


# Publish Data

This repository contains the alpha-stage data publishing component of data.gov.uk.

## Development

To use this repository for development you should run the following tasks:

```bash
git clone <REPO>
cd publish_data_alpha
vagrant up
vagrant ssh
cd /vagrant/tools
sudo bash dev_setup.sh
# Make a cup of tea

# Edit your bashrc or bash_profile to have
export DJANGO_SETTINGS_MODULE="publish_data.settings.dev”

cd src
./manage migrate
./manage runserver
```

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



