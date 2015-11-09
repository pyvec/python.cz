# -*- coding: utf-8 -*-


from os import path

import yaml

from .helpers import get_test_cases, DATA_DIR, ROOT_DIR


cases = get_test_cases([
    path.join(DATA_DIR, '*.yaml'),
    path.join(DATA_DIR, '*.yml'),
    path.join(ROOT_DIR, '*.yaml'),
    path.join(ROOT_DIR, '*.yml'),
    path.join(ROOT_DIR, '.*.yaml'),
    path.join(ROOT_DIR, '.*.yml'),
])


def test_there_are_yaml_files_to_be_tested():
    assert len(cases) > 0


for case in cases:
    def _test():
        """Tests whether YAML data file is a valid YAML document."""
        with open(case['filename']) as f:
            assert yaml.load(f.read())

    globals()[case['fn_name']] = _test
