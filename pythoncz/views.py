# -*- coding: utf-8 -*-


from flask import (render_template as _render_template, url_for,
                   redirect, request)

from . import app, cs_sort
from .models import trello, business, photos, yaml_files


# Templating

def render_template(filename, **kwargs):
    kwargs['template_url'] = app.config['TEMPLATES_DIR_URL'] + filename
    return _render_template(filename, **kwargs)


@app.context_processor
def inject_context():
    return {
        'debug': app.debug,
        'config': app.config,
        'url': request.url,
        'lang': 'cs',
    }


# Regular views

@app.route('/')
def index_cs():
    return render_template('index_cs.html',
                           photo_url=photos.get_random_url())


@app.route('/en')
def index_en():
    return render_template('index_en.html',
                           photo_url=photos.get_random_url(), lang='en')


@app.route('/zapojse')
def get_involved_cs():
    trello_board_id = app.config['TRELLO_BOARD_ID']
    context = {
        'trello_board': trello.get_board(trello_board_id),
        'trello_board_url': 'https://trello.com/b/{}/'.format(trello_board_id),
    }
    return render_template('get_involved_cs.html', **context)


@app.route('/zacatecnici')
def beginners_cs():
    return render_template('beginners_cs.html',
                           courses=yaml_files.get('courses'))


@app.route('/prace')
def jobs_cs():
    return render_template('jobs_cs.html',
                           business_groups=business.get_groups(),
                           job_boards=get_job_boards())


@app.route('/en/jobs')
def jobs_en():
    return render_template('jobs_en.html',
                           business_groups=business.get_groups(),
                           job_boards=get_job_boards(),
                           lang='en')


def get_job_boards():
    job_boards = yaml_files.get('job_boards')
    key_func = cs_sort.get_key_fn()
    job_boards.sort(key=lambda board: key_func(board['name']))
    return job_boards


# Redirects of legacy stuff

@app.route('/index.html')
def index_legacy():
    return redirect(url_for('index'), code=301)


@app.route('/english.html')
def index_en_legacy():
    return redirect(url_for('index_en'), code=301)


@app.route('/pyladies/', defaults={'target': ''})
@app.route('/pyladies/<path:target>')
def pyladies(target):
    return redirect('http://pyladies.cz/' + target, code=301)


@app.route('/talks/<path:target>')
def talks(target):
    base_url = 'https://github.com/pyvec/talks-archive/raw/master/'
    return redirect(base_url + target, code=301)
