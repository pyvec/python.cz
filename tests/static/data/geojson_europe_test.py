import json
from pathlib import Path

import pytest


BOUNDS = (
    (-28, 56),  # Azores (West), Novaya Zemlya (East)
    (34, 71),  # Gavdos (South), Nordkapp (North)
)


path = Path(__file__).parent / '../../../pythoncz/static/data/business.geojson'
with path.open() as f:
    features = json.load(f)['features']
assert len(features) > 0


@pytest.mark.parametrize('feature', [
    pytest.param(feature, id=feature['properties']['name'])
    for feature in features
])
def test_geojson_coords_are_in_europe(feature):
    """Tests whether entries in GeoJSON are in Europe. If this test failed
    for you, it's very likely because you have

        "coordinates": [50.0703272, 14.4006753]

    (which is Yemen) instead of

        "coordinates": [14.4006753, 50.0703272]

    (which is Prague) in your GeoJSON entry.
    """
    # For Point, convert list of coords to nested list
    geometry_type = feature['geometry']['type']
    coords = feature['geometry']['coordinates']
    places = [coords] if geometry_type == 'Point' else coords

    for place_coords in places:
        for i, coord in enumerate(place_coords):
            assert BOUNDS[i][0] < place_coords[i] < BOUNDS[i][1]
