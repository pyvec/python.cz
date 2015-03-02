# -*- coding: utf-8 -*-


from os import path

from flask import (render_template as _render_template, url_for,
                   redirect, request)

from . import app


# Templating

def render_template(filename, **kwargs):
    template_folder = app.template_folder
    template_folder = template_folder.replace(app.config['ROOT_DIR'], '')

    kwargs['github_url'] = app.config['GITHUB_URL'].format(
        template_folder=template_folder.strip('/'),
        filename=filename
    )
    return _render_template(filename, **kwargs)


@app.context_processor
def inject_context():
    return {
        'debug': app.debug,
        'url': path.join(app.config['ROOT_URL'], request.path)
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
