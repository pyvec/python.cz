from os import path
from glob import glob


TEST_DIR = path.dirname(path.abspath(__file__))
ROOT_DIR = path.abspath(path.join(TEST_DIR, '..'))
DATA_DIR = path.abspath(path.join(ROOT_DIR, 'pythoncz', 'static', 'data'))


def generate_filenames(glob_patterns):
    for glob_pattern in glob_patterns:
        for filename in glob(glob_pattern):
            yield filename
