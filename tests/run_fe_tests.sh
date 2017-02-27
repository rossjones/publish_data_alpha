#!/bin/bash

# Where to find the app, and how to log in
export APP_SERVER_URL=http://localhost:8010
export USER_EMAIL=test-co@localhost
export USER_PASSWORD=password

# Various executables needed to run tests
export SELENIUM=${HOME}/bin/selenium-server-standalone-3.0.1.jar
export GECKO_DRIVER=${HOME}/bin/geckodriver
export PHANTOM_JS=${HOME}/bin/phantomjs
export CHROME_DRIVER=${HOME}/bin/chromedriver

# Which browser to use for tests (phantomjs, geckodriver or chrome)
export BROWSER_NAME=phantomjs

export DJANGO_SETTINGS_MODULE=publish_data.settings.test

# start test server
cd ../src
echo Starting test server at $APP_SERVER_URL
./manage.py runserver 0.0.0.0:8010 > /dev/null 2>&1 &
PID=$!

# run all tests
cd ../tests
nightwatch || true

# flush db
#cd ../src
#./manage.py flush --no-input # FIXME - flush only datasets

# kill test server
echo Stopping test server
pkill -TERM -P $PID
