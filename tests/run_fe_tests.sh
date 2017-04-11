#!/bin/bash

# Where to find the app, and how to log in
export APP_SERVER_URL=http://localhost:8010
export USER_EMAIL=test-co@localhost
export ADMIN_USER_EMAIL=test-admin@localhost
export USER_PASSWORD=password

# Various executables needed to run tests
export SELENIUM=${HOME}/bin/selenium-server-standalone-3.2.0.jar
export GECKO_DRIVER=${HOME}/bin/geckodriver
export PHANTOM_JS=${HOME}/bin/phantomjs
export CHROME_DRIVER=${HOME}/bin/chromedriver

# Which browser to use for tests (phantomjs, geckodriver or chrome)
export BROWSER_NAME=phantomjs

export DJANGO_SETTINGS_MODULE=publish_data.settings.test

# Prefix for all test titles
export TEST_TITLE_PREFIX='TEST-'


trap kill_server SIGINT

function kill_server() {
    # kill test server
    echo Stopping test server
    pkill -TERM -P $PID
}


# start test server
cd ../src
echo Starting test server at $APP_SERVER_URL
rm db.sqlite3
./manage.py migrate
./manage.py loaddata datasets/fixtures/organisations.json.gz
./manage.py import_test_users < ../tests/test-users.json
./manage.py loaddata locations

./manage.py runserver 0.0.0.0:8010 > /dev/null 2>&1 &
PID=$!

sleep 5
# run all tests
cd ../tests
nightwatch || true

# flush db
cd ../src
./manage.py delete_datasets --yes $TEST_TITLE_PREFIX

kill_server
exit 0
