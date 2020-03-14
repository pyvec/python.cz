from pathlib import Path

import pytest
from ics import Calendar, Event

from pythoncz.models.events import (preprocess_ical, find_first_url,
                                    set_url_from_description)


def test_preprocess_ical():
    path = Path(__file__).parent / 'invalid_ical.ics'
    text = preprocess_ical(path.read_text())

    calendar = Calendar(text)
    events = list(calendar.events)

    assert calendar
    assert events[0]

    # there are two alarms in the file, one type AUDIO and one type NONE
    # NONE has to be removed because ics can't parse it
    # the other one should not be removed
    assert len(events[0].alarms) == 1
    assert events[0].alarms[0].action == "AUDIO"


@pytest.mark.parametrize('text,expected', [
    (None, None),
    ('', None),
    ('lorem ipsum dolor sit amet', None),
    ('https://python.cz', 'https://python.cz'),
    ('http://python.cz', 'http://python.cz'),
    ('lorem ipsum https://python.cz dolor sit amet', 'https://python.cz'),
    ('lorem https://python.cz ipsum https://pyvo.cz', 'https://python.cz'),
])
def test_find_first_url(text, expected):
    assert find_first_url(text) == expected


@pytest.mark.parametrize('event,expected_url', [
    (Event(), None),
    (Event(url='https://python.cz'), 'https://python.cz'),
    (Event(description='https://pyvo.cz', url='https://python.cz'),
     'https://python.cz'),
    (Event(description='https://pyvo.cz'), 'https://pyvo.cz'),
    (Event(description='''
        See: https://www.meetup.com/PyData-Prague/events/257775220

        Looking forward to see you!
     '''),
     'https://www.meetup.com/PyData-Prague/events/257775220'),
])
def test_set_url_from_description(event, expected_url):
    assert set_url_from_description(event).url == expected_url
