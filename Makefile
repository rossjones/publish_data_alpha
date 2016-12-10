# Where to find the app, and how to log in
export APP_SERVER_URL=http://localhost:8000
export USER_EMAIL=a@b.c
export USER_PASSWORD=foobar

# Various executables needed to run tests
export SELENIUM=$(HOME)/bin/selenium-server-standalone-3.0.1.jar
export GECKO_DRIVER=$(HOME)/bin/geckodriver
export PHANTOM_JS=$(HOME)/bin/phantomjs
export CHROME_DRIVER=$(HOME)/bin/chromedriver

# Which browser to use for tests (phantomjs, geckodriver or chrome)
export BROWSER_NAME=phantomjs


all:
	@echo "Usage:"
	@echo "  $(MAKE) test : run the end-to-end test suite"


test:
	@echo "Make sure that:"
	@echo "- the app server is running locally at $(APP_SERVER_URL)"
	@echo "- the variables at the top of the Makefile are correctly set"
	@echo
	@echo -n "Press Return to continue "
	@read dummy
	@cd tests && nightwatch
