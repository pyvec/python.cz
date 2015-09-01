# -*- coding: utf-8 -*-


import yaml
from os import path
from glob import glob


def test_valid_json():
    """Tests whether all YAML data files are valid YAML documents."""

    test_dir = path.dirname(path.abspath(__file__))
    data_dir = path.join(test_dir, '..', 'static', 'data')

    count = 0
    for filename in glob(path.join(data_dir, '*.yml')):
        count += 1
        with open(filename) as f:
            assert yaml.load(f.read())

    assert count > 0
