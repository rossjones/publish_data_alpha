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
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
