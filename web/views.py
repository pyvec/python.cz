# -*- coding: utf-8 -*-


from os import path

from flask import (render_template as _render_template, url_for,
                   redirect, request)

from . import app


GITHUB_URL = (
    'https://github.com/honzajavorek/python.cz/'
    'blob/master/{template_folder}/{filename}'
)


# Templating

def render_template(filename, **kwargs):
    template_folder = app.template_folder
    template_folder = template_folder.replace(app.config['ROOT_DIR'], '')

    kwargs['github_url'] = GITHUB_URL.format(
        template_folder=template_folder,
        filename=filename
    )
    return _render_template(filename, **kwargs)


@app.context_processor
def inject_context():
    return {
        'debug': app.debug,
        'url': 'http://python.cz' + request.path
    }


# Regular views

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index-en.html')
def index_en():
    return render_template('index-en.html')


# Legacy redirects

@app.route('/index.html')
def index_legacy():
    return redirect(url_for('index'), code=301)


@app.route('/english.html')
def index_en_legacy():
    return redirect(url_for('index_en'), code=301)
