import requests
from bs4 import BeautifulSoup


CITIES_LINKS = {
    'copenhagen': 'http://salah.dk',
    'aarhus': 'http://aa.salah.dk',
    'odense': 'http://o.salah.dk',
    'malmo': 'http://m.salah.dk',
}


def parse_city_page(city='copenhagen'):
    """Load the page and extract prayer times for the given city."""
    result = []
    response = requests.get(CITIES_LINKS[city])
    if response.ok:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        for prayer in soup.findAll('div', {'id': 'salah'}):
            prayer_time = prayer.findNext('div', {'id': 'tid'})
            prayer_str = '{}: {}'.format(
                prayer.getText(),
                prayer_time.getText()
            )
            result.append(prayer_str)
    return ', '.join(result)
