apt-get update
apt-get install -qy  python3-dev python-virtualenv

# Install a recent Elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.2.deb
dpkg -i elasticsearch-5.1.2.deb

mkdir -p /usr/lib/publishing
chown -R vagrant /usr/lib/publishing/
virtualenv -p /usr/bin/python3 /usr/lib/publishing
source /usr/lib/publishing/bin/activate


cd /vagrant
pip3 install -r requirements.txt
export DJANGO_SETTINGS_MODULE="publish_data.settings.dev"
cd src

# Uncomment if you want to retrieve govuk_template instead of using the included one
#mkdir -p assets
#cd assets
#GOVUK_TEMPLATE_VERSION=0.19.1
#curl -kL "https://github.com/alphagov/govuk_template/releases/download/v${GOVUK_TEMPLATE_VERSION}/django_govuk_template-${GOVUK_TEMPLATE_VERSION}.tgz" | tar xz ./govuk_template

# uncomment if you want to compile govuk_elements yourself instead of using the included one
# Need a recent version of node. Linux distros can be a little late
cd /vagrant
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -

# to compile the SCSS
npm install govuk-elements-sass gulp gulp-sass
gulp styles

