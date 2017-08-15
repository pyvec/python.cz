#!/bin/sh

# Update of app source code, dependencies installation, app restart
#
# This script is designed to be remotely executed by TravisCI build
# as part of automatic continuous deployment.
#
# WARNING!
# If you change contents of this file, then you need to update it manually
# on server as it won't be able to 'update itself'.

# This script should be executed remotely on the production machine.
if [ "$USER" != "app" ]; then
    exit
fi

# clear existing source code
rm -rf /srv/app

# get latest code
git clone --progress --depth=1 --branch=master https://github.com/pyvec/python.cz /srv/app

# install dependencies
/srv/venv/bin/pip install -U pip
/srv/venv/bin/pip install /srv/app

# restart the app
supervisorctl restart app
