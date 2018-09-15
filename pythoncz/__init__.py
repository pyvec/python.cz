import os

import yaml
from flask import Flask
from flask_frozen import Freezer


ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')

GITHUB_URL = 'https://github.com/pyvec/python.cz'
GITHUB_EDIT_URL = GITHUB_URL + '/edit/master/pythoncz'

TEMPLATES_DIR_URL = GITHUB_EDIT_URL + '/templates/'
BUSINESS_LIST_URL = GITHUB_EDIT_URL + '/static/data/business.geojson'
BEGINNERS_DATA_URL = GITHUB_EDIT_URL + '/static/data/beginners.yml'
EVENTS_DATA_URL = GITHUB_EDIT_URL + '/static/data/events_feeds.yml'
JOBS_DATA_URL = GITHUB_EDIT_URL + '/static/data/jobs.yml'

PYVEC_ACCOUNT_URL = (
    'https://www.fio.cz/scgi-bin/hermes/'
    'dz-transparent.cgi?ID_ucet=2600260438'
)
GET_INVOLVED_URL = (
    'https://github.com/pulls?utf8=%E2%9C%93&q=is%3Aopen+org%3Apyvec'
)

GITHUB_ORGANIZATIONS = ('pyvec', 'pyladiescz')
GOOGLE_ANALYTICS_CODE = 'UA-1316071-13'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
CACHE_DIR = os.getenv('CACHE_DIR') or os.path.join(ROOT_DIR, 'cache')


app = Flask('pythoncz')


with open(os.path.join(app.static_folder, 'data', 'events_feeds.yml')) as f:
    app.config['CZECH_PYTHON_EVENTS_CALENDAR_URL'] = next(filter(
        lambda feed: feed['name'] == 'Czech Python Events',
        yaml.safe_load(f.read())['feeds']
    ))['url']


freezer = Freezer(app)

app.config.from_object(__name__)


from . import views  # NOQA
