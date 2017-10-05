#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from pythoncz import app


if __name__ == '__main__':
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))

    app.config['SERVER_NAME'] = '{host}:{port}'.format(host=host, port=port)
    app.run(host=host, port=port, debug=True)
