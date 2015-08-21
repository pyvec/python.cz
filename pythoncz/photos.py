# -*- coding: utf-8 -*-


import os
from glob import glob

from flask import url_for


def get_urls(static_dir):
    path = os.path.join(static_dir, 'photos', '*.[jJ][pP][gG]')
    prefix = '{}/'.format(static_dir)

    return [
        url_for('static', filename=f.replace(prefix, ''))
        for f in glob(path)
    ]
