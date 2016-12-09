# -*- coding: utf-8 -*-

from os import path

import yaml
from slugify import slugify

from . import ROOT_DIR, DATA_DIR, generate_filenames


glob_patterns = [
    path.join(DATA_DIR, '*.yaml'),
    path.join(DATA_DIR, '*.yml'),
    path.join(ROOT_DIR, '*.yaml'),
    path.join(ROOT_DIR, '*.yml'),
    path.join(ROOT_DIR, '.*.yaml'),
    path.join(ROOT_DIR, '.*.yml'),
]


def test_there_are_yaml_files_to_be_tested():
    assert len(list(generate_filenames(glob_patterns))) > 0


def _create_test(filename):
    def test():
        """Tests whether YAML data file is a valid YAML document."""
        with open(filename) as f:
            assert yaml.load(f.read())
    return test


for filename in generate_filenames(glob_patterns):
    slug = slugify(path.basename(filename), separator='_')
    fn_name = 'test_{}_is_valid'.format(slug)
    globals()[fn_name] = _create_test(filename)
