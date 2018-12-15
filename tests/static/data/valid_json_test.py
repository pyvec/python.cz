import json
from pathlib import Path

import pytest


project_dir = Path(__file__).parent / '../../..'
paths = list(project_dir.rglob('*.*json'))
assert len(paths) > 0


@pytest.mark.parametrize('path', [
    pytest.param(path, id=str(path.relative_to(project_dir)))
    for path in paths
])
def test_json_file_is_valid(path):
    """Tests whether JSON data file is a valid JSON document."""
    with path.open() as f:
        assert json.load(f)
