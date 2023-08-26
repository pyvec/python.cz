from urllib.parse import quote_plus
from jinja2 import Environment
from mkdocs.config import Config
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files

from hooks.events import fetch_events, filter_events


def on_page_markdown(
    markdown: str,
    page: Page,
    config: Config,
    files: Files,
) -> str:
    # Unfortunately this is aparently the only way to hide the navigation
    # on every page using the material theme. Solution described in
    # https://github.com/squidfunk/mkdocs-material/issues/3686 breaks
    # hamburger menu on small viewports.
    page.meta["hide"] = ["toc", "navigation"]

    print(f"INFO    -  Rendering jinja on {page.file.src_path}")
    env = Environment()
    env.filters["urlencode"] = quote_plus
    template = env.from_string(markdown)
    return template.render(
        events=filter_events(fetch_events(), days_limit=60, only_upcoming=True)
    )
