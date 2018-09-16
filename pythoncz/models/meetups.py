import requests
from lxml import html
from slugify import slugify


__all__ = ('get_meetups',)


WIKI_URL = ('https://cs.wikipedia.org/wiki/'
            'Seznam_m%C4%9Bst_v_%C4%8Cesku_podle_po%C4%8Dtu_obyvatel')


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
    res = requests.get(WIKI_URL)
    res.raise_for_status()

    root = html.fromstring(res.content.decode('utf-8'))
    rows = root.cssselect('.wikitable tbody tr')
    rows.pop(0)

    city_slugs = [
        slugify(row.cssselect('td')[0].text_content().strip()) + '-pyvo'
        for row in rows
    ]

    # fix discrepancies
    city_slugs[city_slugs.index('hradec-kralove-pyvo')] = 'hradec-pyvo'

    def key_func(meetup):
        slug = meetup['url'].rstrip('/').split('/')[-1]
        return city_slugs.index(slug)

    return sorted(meetups, key=key_func)
