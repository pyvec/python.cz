import os

from flask import Flask


app = Flask('pythoncz')
app.config.from_object('pythoncz.config')

if not app.debug:
    app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', 'python.cz')


from pythoncz import views  # NOQA
