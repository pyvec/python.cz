# -*- coding: utf-8 -*-


import os
import json

from .. import app, cs_sort


def get_groups():
    path = os.path.join(app.static_folder, 'data', 'business.geojson')
    return _group_business_data(_load_business_data(path))


def _group_business_data(data):
    groups = {}
    for point in data:
        if point.get('company'):
            name = 'companies'
        else:
            name = 'individuals'

        groups.setdefault(name, [])
        groups[name].append(point)

    key_func = cs_sort.get_key_fn()
    for name, group in groups.items():
        group.sort(key=lambda point: key_func(point['name']))

    return groups


def _load_business_data(data_file):
    with open(data_file) as f:
        data = json.load(f)

    for feature in data['features']:
        point = feature['properties']

        geometry = feature.get('geometry')
        if geometry:
            point['coordinates'] = geometry['coordinates']

        yield point
