# -*- coding: utf-8 -*-


import json
from os import path

from .helpers import get_test_cases, DATA_DIR


cases = get_test_cases([
    path.join(DATA_DIR, '*.*json'),
])


def test_there_are_json_files_to_be_tested():
    assert len(cases) > 0


for case in cases:
    def _test():
        """Tests whether JSON data file is a valid JSON document."""
        with open(case['filename']) as f:
            assert json.load(f)

    globals()[case['fn_name']] = _test
