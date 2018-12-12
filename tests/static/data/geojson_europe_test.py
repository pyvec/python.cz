import json
from os import path

import pytest

from tests import ROOT_DIR, DATA_DIR, generate_filenames


BOUNDS = (
    (-28, 56),  # Azores (West), Novaya Zemlya (East)
    (34, 71),  # Gavdos (South), Nordkapp (North)
)


def generate_geojson_entries(filenames):
    for filename in filenames:
        with open(filename) as f:
            data = json.load(f)

        for feature in data['features']:
            yield {
                'filename': filename,
                'name': feature['properties']['name'],
                'geometry_type': feature['geometry']['type'],
                'coords': feature['geometry']['coordinates'],
            }


glob_patterns = [
    path.join(DATA_DIR, '*.geojson'),
    path.join(ROOT_DIR, '*.geojson'),
]

entries = list(generate_geojson_entries(generate_filenames(glob_patterns)))


def test_there_are_geojson_entries_to_be_tested():
    assert len(entries) > 0


@pytest.mark.parametrize('entry', entries)
def test_geojson_coords_are_in_europe(entry):
    """Tests whether entries in GeoJSON are in Europe. If this test failed
    for you, it's very likely because you have

        "coordinates": [50.0703272, 14.4006753]

    (which is Yemen) instead of

        "coordinates": [14.4006753, 50.0703272]

    (which is Prague) in your GeoJSON entry.
    """
    # For Point, convert list of coords to nested list
    if entry['geometry_type'] == 'Point':
        places = [entry['coords']]
    else:
        places = entry['coords']

    for place_coords in places:
        for i, coord in enumerate(place_coords):
            assert BOUNDS[i][0] < place_coords[i] < BOUNDS[i][1]
