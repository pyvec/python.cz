from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from mkdocs.config import Config
import requests


def on_post_build(config: Config):
    site_dir = Path(config['site_dir'])

    print("INFO    -  Generating redirects")
    # https://developers.google.com/search/docs/advanced/crawling/301-redirects
    redirects = {
        'pyladies/s001-install/index.html': 'https://pyladies.cz/v1/s001-install/',
        'pyladies/s002-hello-world/index.html': 'https://pyladies.cz/v1/s002-hello-world/',
        'pyladies/s003-looping/index.html': 'https://pyladies.cz/v1/s003-looping/',
        'pyladies/s004-strings/index.html': 'https://pyladies.cz/v1/s004-strings/',
        'pyladies/s005-modules/index.html': 'https://pyladies.cz/v1/s005-modules/',
        'pyladies/s006-lists/index.html': 'https://pyladies.cz/v1/s006-lists/',
        'pyladies/s007-cards/index.html': 'https://pyladies.cz/v1/s007-cards/',
        'pyladies/s008-cards2/index.html': 'https://pyladies.cz/v1/s008-cards2/',
        'pyladies/s009-git/index.html': 'https://pyladies.cz/v1/s009-git/',
        'pyladies/s010-data/index.html': 'https://pyladies.cz/v1/s010-data/',
        'pyladies/s011-dicts/index.html': 'https://pyladies.cz/v1/s011-dicts/',
        'pyladies/s012-pyglet/index.html': 'https://pyladies.cz/v1/s012-pyglet/',
        'pyladies/s014-class/index.html': 'https://pyladies.cz/v1/s014-class/',
        'pyladies/s015-asteroids/index.html': 'https://pyladies.cz/v1/s015-asteroids/',
        'pyladies/s016-micropython/index.html': 'https://pyladies.cz/v1/s016-micropython/',
    }
    for src, dst in redirects.items():
        path = Path(f"{site_dir}/{src}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"""
            <!DOCTYPE html>
            <html lang="cs">
                <head>
                    <meta charset="utf-8">
                    <title>Přesměrování</title>
                    <link rel="canonical" href="{dst}">
                    <meta http-equiv="refresh" content="0; {dst}">
                    <script>window.location.replace('{dst}');</script>
                </head>
                <body>
                    <h1>Přesměrování</h1>
                    <p>To, co tady bylo, je teď jinde: <a href="{dst}">{dst}</a></p>
                </body>
            </html>
        """.strip())

    print("INFO    -  Generating talks archive redirects")
    path = Path(f"{site_dir}/404.html")
    path.write_text("""
        <!DOCTYPE html>
        <html lang="cs">
            <head>
                <meta charset="utf-8">
                <title>404</title>
                <script>
                    pdfs = [
                        /talks-archive\\/([^.]+)\\.pdf$/
                    ].forEach(function (pdf) {
                        const match = window.location.pathname.match(pdf);
                        if (match) {
                            const path = match[1];
                            const url = 'https://raw.githubusercontent.com/pyvec/talks-archive/master/' + path + '.pdf';
                            window.location.replace(url);
                        }
                    });
                </script>
            </head>
            <body>
                <h1>404</h1>
            </body>
        </html>
    """.strip())

