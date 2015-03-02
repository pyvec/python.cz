# -*- coding: utf-8 -*-


from os import path

from flask import Flask


PACKAGE_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.realpath(path.join(PACKAGE_DIR, '..'))

GITHUB_URL = (
    'https://github.com/honzajavorek/python.cz/'
    'blob/master/{template_folder}/{filename}'
)
TRELLO_BOARD_ID = 'JHXkZGHZ'


app = Flask('web',
            static_folder=path.join(ROOT_DIR, 'files'),
            static_url_path='',
            template_folder=path.join(ROOT_DIR, 'pages'))

app.config.from_object(__name__)


from . import views  # NOQA
