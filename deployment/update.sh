#!/bin/sh

# Update of app source code, dependencies installation, app restart
#
# This script is designed to be remotely executed by TravisCI build
# as part of automatic continuous deployment.

# This script should be executed remotely on the production machine.
if [ "$USER" != "app" ]; then
    exit
fi

# clear existing source code
rm -rf /srv/app

# get latest code
git clone --progress --depth=1 https://github.com/pyvec/python.cz /srv/app

# install dependencies
/srv/venv/bin/pip install -r /srv/app/requirements.txt

# restart the app
supervisorctl restart app
