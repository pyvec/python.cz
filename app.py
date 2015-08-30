#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration for deploying python.cz on the rosti.cz hosting.

It should be easy to adapt to other kinds of WSGI-based hosting.


Instructions:
- Put this repo in /srv/app. You'll need to clear the previous contents:

        rm -rf /srv/app
        git clone https://github.com/honzajavorek/python.cz /srv/app

- Install everything:

        pip install -r requirements.txt

- Restart:

        supervisorctl restart app

"""


from pythoncz import app as application  # noqa
