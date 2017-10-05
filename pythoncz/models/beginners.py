import os

import yaml

from pythoncz.app import app


__all__ = ('data',)


# Data loaded on import time so file system is not read and YAML parsed
# on every request.
with open(os.path.join(app.static_folder, 'data', 'beginners.yml')) as f:
    data = yaml.load(f.read())
