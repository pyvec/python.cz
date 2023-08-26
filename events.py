from datetime import date, datetime, timedelta
import json
from operator import itemgetter
from pathlib import Path

import pytz
import extruct
import ics
from mkdocs.config import Config
import requests
from strictyaml import load as load_yaml, Map, Str, Seq, Url


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

TIMELINE_LIMIT_DAYS = 60


def on_post_build(config: Config | None = None):
    cache_path = Path(".events_cache.json")
    try:
        print(f"Loading events feeds from {cache_path}")
        data = json.loads(cache_path.read_text())
    except FileNotFoundError:
        print("No cache")
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

    print("Parsing events")
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

    print("Filtering and sorting events")
    today = date.today()
    timeline_limit = today + timedelta(days=TIMELINE_LIMIT_DAYS)
    events = sorted(
        (
            event
            for event in events
            if (
                event["starts_at"].date() >= today
                or (event["ends_at"] and event["ends_at"].date() >= today)
            )
            and event["starts_at"].date() <= timeline_limit
        ),
        key=itemgetter("starts_at"),
    )
    for event in events:
        print(event["starts_at"], event["name"])


def parse_icalendar(text: str):
    return [
        dict(
            name=event.summary,
            starts_at=to_prague_tz(event.begin),
            ends_at=to_prague_tz(event.end) if event.end else None,
            location_raw=event.location,
            url=event.url,
        )
        for event in ics.Calendar(text).events
    ]


def parse_json_dl(html: str, base_url: str):
    data = extruct.extract(html, base_url, syntaxes=["json-ld"])
    return [
        dict(
            name=item["name"],
            starts_at=to_prague_tz(datetime.fromisoformat(item["startDate"])),
            ends_at=to_prague_tz(datetime.fromisoformat(item["endDate"])),
            location_raw=parse_json_dl_location(item["location"]),
            url=item["url"],
        )
        for item in data["json-ld"]
        if item["@type"] == "Event" and base_url in item["url"]
    ]


def parse_json_dl_location(location: dict[str, str]) -> str:
    return f"{location['name']}, {location['address']['streetAddress']}, {location['address']['addressLocality']}, {location['address']['addressCountry']}"


def to_prague_tz(dt: datetime) -> datetime:
    prague_tz = pytz.timezone("Europe/Prague")
    if dt.tzinfo is None:
        return dt.replace(tzinfo=prague_tz)
    return dt.astimezone(prague_tz)


if __name__ == "__main__":
    on_post_build()
