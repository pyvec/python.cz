# -*- coding: utf-8 -*-


from os import path
from glob import glob

from slugify import slugify


def get_test_cases(glob_patterns):
    cases = []
    for glob_pattern in glob_patterns:
        for filename in glob(glob_pattern):
            slug = slugify(path.basename(filename), separator='_')
            fn_name = 'test_{0}_is_valid'.format(slug)

            cases.append({
                'filename': filename,
                'slug': slug,
                'fn_name': fn_name,
            })
    return cases


TEST_DIR = path.dirname(path.abspath(__file__))
ROOT_DIR = path.abspath(path.join(TEST_DIR, '..'))
DATA_DIR = path.abspath(path.join(ROOT_DIR, 'pythoncz', 'static', 'data'))
