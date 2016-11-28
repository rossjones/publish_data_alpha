apt-get update
apt-get install -qy  python3-dev python-virtualenv

mkdir -p /usr/lib/publishing
chown -R vagrant /usr/lib/publishing/
virtualenv -p /usr/bin/python3 /usr/lib/publishing
source /usr/lib/publishing/bin/activate


cd /vagrant
pip3 install -r requirements.txt
export DJANGO_SETTINGS_MODULE="publish_data.settings.dev"
cd src

# Retrieve govuk_template
mkdir -p assets
cd assets
GOVUK_TEMPLATE_VERSION=0.19.1
curl -kL "https://github.com/alphagov/govuk_template/releases/download/v${GOVUK_TEMPLATE_VERSION}/django_govuk_template-${GOVUK_TEMPLATE_VERSION}.tgz" | tar xz ./govuk_template

cd /vagrant/src
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
