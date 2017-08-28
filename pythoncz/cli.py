import os

import click
from flask.cli import FlaskGroup


def create_app(info):
    """
    Development server wrapper so FLASK_APP and FLASK_DEBUG aren't necessary
    by default, see http://flask.pocoo.org/docs/latest/cli/
    """
    from pythoncz.app import app
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def main():
    """This is a management script for the pythoncz application"""
    os.environ['FLASK_DEBUG'] = os.getenv('FLASK_DEBUG', '1')
