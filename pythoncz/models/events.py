from pathlib import Path
from typing import List

import yaml
import requests
import ics
import arrow

from pythoncz import app

feeds_datafile = Path(app.root_path) / "static/data/events_feeds.yml"

data = []


def preprocess_ical(text: str) -> List[str]:
    """ Removes VALARM ACTION:NONE from the iCal file (included in some events from Google Calendar)
    """
    lines = text.splitlines()
    new_lines = []

    i = 0

    try:
        while i < len(lines):
            if lines[i] != "BEGIN:VALARM" or lines[i + 1].replace("ACTION:", "") in {"DISPLAY", "AUDIO"}:
                new_lines.append(lines[i])
                i += 1
                continue

            while lines[i] != "END:VALARM":
                i += 1

            i += 1
    except IndexError:
        raise ValueError("Can't preprocess iCal file to remove ACTION:NONE")

    return new_lines


def load_events(ical_url):
    try:
        response = requests.get(ical_url)
    except Exception as e:
        raise ValueError(f"Could not load iCal feed from {ical_url}") from e

    response.raise_for_status()

    ical = preprocess_ical(response.text)

    calendar = ics.Calendar(ical)

    return calendar.events


@app.before_first_request
def load_data():
    feeds = yaml.safe_load(feeds_datafile.read_text())["feeds"]

    now = arrow.now("Europe/Prague")

    for feed in feeds:
        data.extend(
            {"feed": feed, "event": event} for event in load_events(feed["ical"]) if event.begin > now
        )

    data.sort(key=lambda e: e["event"].begin)


def get_calendar():
    events = [e["event"] for e in data]

    calendar = ics.Calendar(events=events)

    return calendar
