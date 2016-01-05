# -*- coding: utf-8 -*-


import os
import json

import yaml
import czech_sort


from .. import app


__all__ = ('data',)


def _group_business_data(data):
    groups = {}
    for point in data:
        if point.get('company'):
            name = 'companies'
        else:
            name = 'individuals'

        groups.setdefault(name, [])
        groups[name].append(point)

    for name, group in groups.items():
        groups[name] = _sort_cs(group)

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


def _sort_cs(iterable, key='name'):
    def item_key(item):
        return czech_sort.key(item[key])
    return sorted(iterable, key=item_key)


# Data loaded on import time so file system is not read and YAML parsed
# on every request.


# jobs.yml
_path = os.path.join(app.static_folder, 'data', 'jobs.yml')
with open(os.path.join(_path)) as f:
    data = yaml.load(f.read())

data['job_boards'] = _sort_cs(data['job_boards'])
data['knowledge_tests'] = _sort_cs(data['knowledge_tests'])


# business.geojson
_path = os.path.join(app.static_folder, 'data', 'business.geojson')
data['business_groups'] = _group_business_data(_load_business_data(_path))
