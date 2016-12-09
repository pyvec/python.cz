# -*- coding: utf-8 -*-

import json
from os import path

from slugify import slugify

from . import ROOT_DIR, DATA_DIR, generate_filenames


glob_patterns = [
    path.join(DATA_DIR, '*.*json'),
    path.join(ROOT_DIR, '*.*json'),
]


def test_there_are_json_files_to_be_tested():
    assert len(list(generate_filenames(glob_patterns))) > 0


def _create_test(filename):
    def test():
        """Tests whether JSON data file is a valid JSON document."""
        with open(filename) as f:
            assert json.load(f)
    return test


for filename in generate_filenames(glob_patterns):
    slug = slugify(path.basename(filename), separator='_')
    fn_name = 'test_{}_is_valid'.format(slug)
    globals()[fn_name] = _create_test(filename)
