# -*- coding: utf-8 -*-


import os
import random
from glob import glob

from flask import url_for

from .. import app


__all__ = ('get_random_url',)


# Created on import time so file system is not read on every request.
_photos = glob(os.path.join(app.static_folder, 'photos', '*.[jJ][pP][gG]'))


def get_random_url():
    # List of URLs cannot be created during import time because
    # creating of an URL needs Flask's application context.
    prefix = '{}/'.format(app.static_folder)
    urls = [
        url_for('static', filename=photo.replace(prefix, ''))
        for photo in _photos
    ]

    return random.choice(urls)
