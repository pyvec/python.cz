#!/usr/bin/env python
from pythoncz import app, freezer


if __name__ == '__main__':
    from elsa import cli
    cli(app, freezer=freezer, base_url='https://python.cz')
