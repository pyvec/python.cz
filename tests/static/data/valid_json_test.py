import json
from os import path

import pytest

from tests import ROOT_DIR, DATA_DIR, generate_filenames


glob_patterns = [
    path.join(DATA_DIR, '*.*json'),
    path.join(ROOT_DIR, '*.*json'),
]

filenames = list(generate_filenames(glob_patterns))


def test_there_are_json_files_to_be_tested():
    assert len(filenames) > 0


@pytest.mark.parametrize('filename', filenames)
def test_json_file_is_valid(filename):
    """Tests whether JSON data file is a valid JSON document."""
    with open(filename) as f:
        assert json.load(f)
