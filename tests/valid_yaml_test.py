# -*- coding: utf-8 -*-

from os import path

import pytest
import yaml

from . import ROOT_DIR, DATA_DIR, generate_filenames


glob_patterns = [
    path.join(DATA_DIR, '*.yaml'),
    path.join(DATA_DIR, '*.yml'),
    path.join(ROOT_DIR, '*.yaml'),
    path.join(ROOT_DIR, '*.yml'),
    path.join(ROOT_DIR, '.*.yaml'),
    path.join(ROOT_DIR, '.*.yml'),
]

filenames = list(generate_filenames(glob_patterns))


def test_there_are_yaml_files_to_be_tested():
    assert len(filenames) > 0


@pytest.mark.parametrize('filename', filenames)
def test_yaml_file_is_valid(filename):
    """Tests whether YAML data file is a valid YAML document."""
    with open(filename) as f:
        assert yaml.load(f.read())
