from pathlib import Path

import ics

from pythoncz.models.events import preprocess_ical


def test_preprocess_ical():
    path = Path(__file__).parent / 'invalid_ical.ics'
    lines = preprocess_ical(path.read_text())

    calendar = ics.Calendar(lines)

    assert calendar
    assert calendar.events[0]

    # there are two alarms in the file, one type AUDIO and one type NONE
    # NONE has to be removed because ics can't parse it
    # the other one should not be removed
    assert len(calendar.events[0].alarms) == 1
    assert calendar.events[0].alarms[0].action == "AUDIO"
