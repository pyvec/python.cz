import json
import re
from datetime import date, datetime, timedelta
from functools import cache
from operator import itemgetter
from pathlib import Path
from zoneinfo import ZoneInfo

import ics
import requests
import teemup
from strictyaml import Map, Seq, Str, Url, load as load_yaml


YAML_SCHEMA = Seq(
    Map(
        {
            "name": Str(),
            "site_url": Url(),
            "url": Url(),
            "format": Str(),
        }
    )
)

USER_AGENT = "python.cz (+https://python.cz)"


@cache
def fetch_events(days_limit: int | None = None, past: bool = False) -> list[dict]:
    cache_path = Path(".events_cache.json")
    try:
        print(f"INFO    -  Loading events feeds from {cache_path}")
        data = json.loads(cache_path.read_text())
    except FileNotFoundError:
        print("INFO    -  No cache")
        yaml = Path("events_feeds.yml").read_text()
        data = []
        for feed in load_yaml(yaml, YAML_SCHEMA).data:
            print(f"Fetching {feed['url']}")
            response = requests.get(feed["url"], headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
            feed["url"] = response.url  # overwrite with the final URL
            feed["data"] = response.text
            data.append(feed)
        cache_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    print("INFO    -  Parsing events")
    events = []
    for feed in data:
        if feed["format"] == "icalendar":
            events.extend(
                [
                    dict(feed=feed, **event_data)
                    for event_data in parse_icalendar(feed["data"])
                ]
            )
        elif feed["format"] == "json-dl":
            events.extend(
                [
                    dict(feed=feed, **event_data)
                    for event_data in parse_json_dl(feed["data"], feed["url"])
                ]
            )
        else:
            raise ValueError(f"Unknown feed format {feed['format']!r}")

    print("INFO    -  Sorting events")
    return sorted(events, key=itemgetter("starts_at"))


def filter_events(
    events: list[dict],
    days_limit: int | None = None,
    only_upcoming: bool = True,
    today: date | None = None,
) -> list[dict]:
    today = today or date.today()
    if only_upcoming:
        events = [
            event
            for event in events
            if event["starts_at"].date() >= today
            or (event["ends_at"] and event["ends_at"].date() >= today)
        ]
    if days_limit is not None:
        events = [
            event
            for event in events
            if event["starts_at"].date() <= today + timedelta(days=days_limit)
        ]
    return events


def generate_icalendar(events: list[dict]) -> str:
    calendar = ics.Calendar()
    for event in events:
        calendar.events.append(
            ics.Event(
                summary=event["name"],
                begin=event["starts_at"],
                end=event["ends_at"],
                location=event["location"],
                url=event["url"],
                categories=["tentative-date"] if event["is_tentative"] else [],
            )
        )
    return calendar.serialize()


def parse_icalendar(text: str) -> list[dict]:
    return [
        dict(
            name=event.summary,
            starts_at=to_prague_tz(event.begin),
            ends_at=to_prague_tz(event.end) if event.end else None,
            location=event.location,
            url=event.url if event.url else find_first_url(event.description),
            is_tentative="tentative-date" in event.categories,
        )
        for event in ics.Calendar(text).events
    ]


def parse_json_dl(html: str, base_url: str) -> list[dict]:
    response = requests.get(base_url)
    events = teemup.parse(response.text)
    return [
        dict(
            name=event["title"],
            starts_at=event["starts_at"],
            ends_at=event["ends_at"],
            location=event["venue"],
            url=event["url"],
            is_tentative=False,
        )
        for event in events
    ]


def parse_json_dl_location(location: dict[str, str]) -> str:
    return f"{location['name']}, {location['address']['streetAddress']}, {location['address']['addressLocality']}, {location['address']['addressCountry']}"


def to_prague_tz(dt: datetime) -> datetime:
    prague_tz = ZoneInfo("Europe/Prague")
    if dt.tzinfo is None:
        return dt.replace(tzinfo=prague_tz)
    return dt.astimezone(prague_tz)


def find_first_url(text: str) -> str | None:
    if match := re.search(r'https?://[^\s"<]+', text or ""):
        return match.group(0)
    return None


if __name__ == "__main__":
    from pprint import pprint

    pprint(fetch_events(), depth=2)
