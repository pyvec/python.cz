# -*- coding: utf-8 -*-

import json
from os import path
from glob import glob

from slugify import slugify

from . import ROOT_DIR, DATA_DIR, generate_filenames


BOUNDS = (
    (-28, 56), # Azores (West), Novaya Zemlya (East)
    (34, 71), # Gavdos (South), Nordkapp (North)
)


glob_patterns = [
    path.join(DATA_DIR, '*.*json'),
    path.join(ROOT_DIR, '*.*json'),
]


def test_there_are_json_files_to_be_tested():
    assert len(list(generate_filenames(glob_patterns))) > 0


def _create_test(coords):
    def test():
        """Tests whether entries in GeoJSON are in Europe. If this test failed
        for you, it's very likely because you have

            "coordinates": [50.0703272, 14.4006753]

        (which is Yemen) instead of

            "coordinates": [14.4006753, 50.0703272]

        (which is Prague) in your GeoJSON entry.
        """
        for i, coord in enumerate(coords):
            assert BOUNDS[i][0] < coords[i] < BOUNDS[i][1]
    return test


for filename in generate_filenames(glob_patterns):
    filename_slug = slugify(path.basename(filename), separator='_')

    with open(filename) as f:
        data = json.load(f)

    for feature in data['features']:
        name = feature['properties']['name']
        coords = feature['geometry']['coordinates']

        feature_slug = slugify(name, separator='_')
        fn_name = 'test_{}_{}_is_in_europe'.format(filename_slug, feature_slug)

        globals()[fn_name] = _create_test(coords)
