# -*- coding: utf-8 -*-


import os

import yaml

from .. import app


def get(name):
    path = os.path.join(app.static_folder, 'data', name + '.yml')
    with open(path) as f:
        return yaml.load(f.read()).get(name)
