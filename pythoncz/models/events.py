from pathlib import Path

import yaml
import requests
import ics
import arrow


feeds_datafile = Path(__file__).parents[1] / "static/data/events_feed.yml"

feeds = yaml.safe_load(feeds_datafile.read_text())["feeds"]


def load_events(ical_url):
    try:
        response = requests.get(ical_url)
    except Exception as e:
        raise ValueError(f"Could not load iCal feed from {ical_url}") from e

    if response.status_code != 200:
        raise ValueError(f"Could not load iCal feed from {ical_url}, status code {response.status_code}")

    # Google includes VALARM ACTION:NONE which ics can't parse
    lines = response.text.splitlines()
    new_lines = []

    i = 0

    try:
        while i < len(lines):
            if lines[i] != "BEGIN:VALARM" or lines[i+1].replace("ACTION:", "") in {"DISPLAY", "AUDIO"}:
                new_lines.append(lines[i])
                i += 1
                continue

            while lines[i] != "END:VALARM":
                i += 1

            i += 1
    except IndexError:
        raise ValueError("Can't preprocess iCal file to remove ACTION:NONE")

    calendar = ics.Calendar(new_lines)

    return calendar.events


data = []
now = arrow.now("Europe/Prague")


for feed in feeds:
    data.extend(
        {"feed": feed, "event": event} for event in load_events(feed["ical"]) if event.begin > now
    )

data.sort(key=lambda e: e["event"].begin)


def get_calendar():
    events = [e["event"] for e in data]

    calender = ics.Calendar(events=events)

    return calender
