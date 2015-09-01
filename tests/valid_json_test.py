# -*- coding: utf-8 -*-


import json
from os import path
from glob import glob


def test_valid_json():
    """Tests whether all JSON data files are valid JSON documents."""

    test_dir = path.dirname(path.abspath(__file__))
    data_dir = path.join(test_dir, '..', 'static', 'data')

    count = 0
    for filename in glob(path.join(data_dir, '*.*json')):
        count += 1
        with open(filename) as f:
            assert json.load(f)

    assert count > 0
