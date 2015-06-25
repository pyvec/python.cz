# -*- coding: utf-8 -*-


import os
import json

import icu


def get_groups(data_dir):
    path = os.path.join(data_dir, 'business.geojson')
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

    key_func = _get_czech_sort_key_func()
    for name, group in groups.items():
        group.sort(key=lambda point: key_func(point['name']))

    return groups


def _get_czech_sort_key_func():
    collator = icu.Collator.createInstance(icu.Locale('cs_CZ.UTF-8'))
    return collator.getSortKey


def _load_business_data(data_file):
    with open(data_file) as f:
        data = json.load(f)

    for feature in data['features']:
        point = feature['properties']

        geometry = feature.get('geometry')
        if geometry:
            point['coordinates'] = geometry['coordinates']

        yield point
