from jinja2 import Environment
from mkdocs.config import Config
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files

from hooks.events import fetch_events


def on_page_markdown(
    markdown: str,
    page: Page,
    config: Config,
    files: Files,
) -> str:
    print(f'INFO    -  Rendering jinja on {page.file.src_path}')
    env = Environment()
    template = env.from_string(markdown)
    return template.render(events=fetch_events())
