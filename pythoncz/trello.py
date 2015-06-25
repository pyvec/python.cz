# -*- coding: utf-8 -*-


import requests


def get_board(board_id):
    url = 'https://trello.com/1/boards/{}/lists?cards=open'.format(board_id)

    resp = requests.get(url)
    resp.raise_for_status()  # TODO better error handling
    board = resp.json()

    return [_sort_by_votes(list_) for list_ in board]


def _sort_by_votes(list_):
    def card_key(card):
        return card['badges']['votes']

    cards = sorted(list_['cards'], key=card_key, reverse=True)
    list_['cards'] = cards
    return list_
