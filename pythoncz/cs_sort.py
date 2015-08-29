# -*- coding: utf-8 -*-


import icu


def get_key_fn():
    collator = icu.Collator.createInstance(icu.Locale('cs_CZ.UTF-8'))
    return collator.getSortKey
