from functools import lru_cache
from lxml import html
import requests
from slugify import slugify


__all__ = ('get_meetups',)


# Source: https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku_podle_po%C4%8Dtu_obyvatel
SORTED_CITY_SLUGS = [
    'praha-pyvo',
    'brno-pyvo',
    'ostrava-pyvo',
    'plzen-pyvo',
    'liberec-pyvo',
    'olomouc-pyvo',
    'ceske-budejovice-pyvo',
    'usti-nad-labem-pyvo',
    'hradec-pyvo',
    'pardubice-pyvo',
    'zlin-pyvo',
    'havirov-pyvo',
    'kladno-pyvo',
    'most-pyvo',
    'opava-pyvo',
    'frydek-mistek-pyvo',
    'karvina-pyvo',
    'jihlava-pyvo',
    'teplice-pyvo',
    'decin-pyvo',
    'karlovy-vary-pyvo',
]


@lru_cache()
def get_meetups(lang='cs'):
    return sort_by_city_size(scrape_meetups(lang))


def scrape_meetups(lang='cs'):
    """
    Ideally, pyvo.cz would have an API where we get all this info. Let's assume
    HTML API is good enough API for us now.
    """
    url = 'https://pyvo.cz/en/' if lang == 'en' else 'https://pyvo.cz/'
    res = requests.get(url, headers={'Accept-Charset': 'utf-8'})
    res.raise_for_status()

    root = html.fromstring(res.content.decode('utf-8'))
    root.make_links_absolute(res.url)

    for event in root.cssselect('#events .event'):
        try:
            yield {
                'name': event.cssselect('h3')[0].text_content().strip(),
                'url': event.cssselect('h3 a')[0].get('href'),
            }
        except IndexError:
            continue


@lru_cache()
def scrape_cities():
    res = requests.get(WIKI_URL)
    res.raise_for_status()
    root = html.fromstring(res.text)
    rows = root.cssselect('.wikitable tbody tr')
    return [row.cssselect('td')[1].text_content().strip() for row in rows[1:]]


def sort_by_city_size(meetups):
    """
    Sorts given iterable of meetups by the size of the city. While pyvo.cz
    lists the meetups according to when the closest event happens or happened,
    this doesn't make sense for python.cz where the meetups are listed just
    as a general overview. Also alphabetical sorting is pretty much just
    confusing for the visitor. It only makes sense to sort the meetups by the
    size of the city. The most populated cities have a larger probability
    that the visitor of the page is close to them, thus they deserve to be
    higher in the list.
    """
    # convert list [city1, city2, ...] into dict {city1: 0, city2: 1, ...}
    city_slugs = {city: n for n, city in enumerate(SORTED_CITY_SLUGS)}

    def key_func(meetup):
        slug = meetup['url'].rstrip('/').split('/')[-1]
        return city_slugs[slug]

    return sorted(meetups, key=key_func)
