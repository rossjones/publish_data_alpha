
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
```
