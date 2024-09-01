from pathlib import Path

from events import fetch_events, generate_icalendar
from mkdocs.config import Config


def on_pre_build(config: Config):
    print("INFO    -  Generating events.ics")
    Path(f"{config['theme'].dirs[0]}/events.ics").write_text(
        generate_icalendar(fetch_events())
    )
