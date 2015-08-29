# -*- coding: utf-8 -*-


from flask import Flask


GITHUB_URL = 'https://github.com/honzajavorek/python.cz'
GITHUB_EDIT_URL = GITHUB_URL + '/edit/master/pythoncz'

TEMPLATES_DIR_URL = GITHUB_EDIT_URL + '/templates/'
BUSINESS_LIST_URL = GITHUB_EDIT_URL + '/static/data/business.geojson'
COURSES_LIST_URL = GITHUB_EDIT_URL + '/static/data/courses.yml'
JOB_BOARDS_LIST_URL = GITHUB_EDIT_URL + '/static/data/job_boards.yml'

PYVEC_ACCOUNT_URL = (
    'https://www.fio.cz/scgi-bin/hermes/'
    'dz-transparent.cgi?ID_ucet=2600260438'
)

TRELLO_BOARD_ID = 'JHXkZGHZ'
GOOGLE_ANALYTICS_CODE = 'UA-1316071-13'


app = Flask('pythoncz')
app.config.from_object(__name__)


from . import views  # NOQA
