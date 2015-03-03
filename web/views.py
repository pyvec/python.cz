# -*- coding: utf-8 -*-


import requests
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
        'url': request.url,
    }


# Regular views

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index-en.html')
def index_en():
    return render_template('index-en.html')


@app.route('/zapojse')
def get_involved():
    # https://trello.com/docs/api/board/index.html#get-1-boards-board-id-lists
    # https://trello.com/1/boards/JHXkZGHZ/lists?cards=open

    board_id = app.config['TRELLO_BOARD_ID']
    url = 'https://trello.com/1/boards/{}/lists?cards=open'.format(board_id)

    resp = requests.get(url)
    trello_board = resp.json()

    trello_board = [sort_by_votes(l) for l in trello_board]
    return render_template('get_involved.html', trello_board=trello_board)


def sort_by_votes(trello_list):
    def card_key(card):
        return card['badges']['votes']

    cards = sorted(trello_list['cards'], key=card_key, reverse=True)
    trello_list['cards'] = cards
    return trello_list


# Legacy redirects

@app.route('/index.html')
def index_legacy():
    return redirect(url_for('index'), code=301)


@app.route('/english.html')
def index_en_legacy():
    return redirect(url_for('index_en'), code=301)
