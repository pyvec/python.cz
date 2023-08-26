from pathlib import Path
from mkdocs.config import Config

from hooks.events import fetch_events, generate_icalendar


def on_pre_build(config: Config):
    print('INFO    -  Generating events.ics')
    Path('overrides/events.ics').write_text(generate_icalendar(fetch_events()))
