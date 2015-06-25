# -*- coding: utf-8 -*-


from os import path

from flask import Flask


PACKAGE_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.realpath(path.join(PACKAGE_DIR, '..'))

GITHUB_URL = (
    'https://github.com/honzajavorek/python.cz/'
    'blob/master/{template_folder}/{filename}'
)
GITHUB_GEOJSON_URL = (
    'https://github.com/honzajavorek/python.cz/'
    'edit/master/files/data/jobs.geojson'
)
PYVEC_ACCOUNT_URL = (
    'https://www.fio.cz/scgi-bin/hermes/'
    'dz-transparent.cgi?ID_ucet=2600260438'
)

TRELLO_BOARD_ID = 'JHXkZGHZ'


app = Flask('web',
            static_folder=path.join(ROOT_DIR, 'files'),
            static_url_path='',
            template_folder=path.join(ROOT_DIR, 'pages'))

app.config.from_object(__name__)


from . import views  # NOQA
