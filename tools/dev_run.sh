source /usr/lib/publishing/bin/activate
cd /vagrant/src
export DJANGO_SETTINGS_MODULE="publish_data.settings.dev"
./manage.py runserver 0.0.0.0:8000
