import os
import random
from glob import glob

from flask import url_for

from pythoncz.app import app


__all__ = ('get_random_url', 'get_random_urls')


# Created on import time so file system is not read on every request.
_photos = glob(os.path.join(app.static_folder, 'photos', '*.[jJ][pP][gG]'))


def get_urls():
    # List of URLs cannot be created during import time because
    # creating of an URL needs Flask's application context.
    prefix = '{}/'.format(app.static_folder)
    return [
        url_for('static', filename=photo.replace(prefix, ''))
        for photo in _photos
    ]


def get_random_url():
    return random.choice(get_urls())


def get_random_urls(number):
    return random.sample(get_urls(), number)
