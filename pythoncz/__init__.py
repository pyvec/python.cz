# -*- coding: utf-8 -*-


from os import path

from flask import Flask


PACKAGE_DIR = path.dirname(path.realpath(__file__))
DATA_DIR = path.join(PACKAGE_DIR, 'static', 'data')

GITHUB_URL = 'https://github.com/honzajavorek/python.cz'
TEMPLATE_URL = GITHUB_URL + '/blob/master/pythoncz/templates/{filename}'
BUSINESS_LIST_URL = GITHUB_URL + '/edit/master/pythoncz/data/business.geojson'

PYVEC_ACCOUNT_URL = (
    'https://www.fio.cz/scgi-bin/hermes/'
    'dz-transparent.cgi?ID_ucet=2600260438'
)
TRELLO_BOARD_ID = 'JHXkZGHZ'


app = Flask('pythoncz')
app.config.from_object(__name__)


from . import views  # NOQA
