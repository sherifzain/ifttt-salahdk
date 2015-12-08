import json
import requests
from bs4 import BeautifulSoup


CITIES_LINKS = {
    'copenhagen': 'http://salah.dk',
    'aarhus': 'http://aa.salah.dk',
    'odense': 'http://o.salah.dk',
    'malmo': 'http://m.salah.dk',
}


def _publish_pb_notification(city, result):
    """Publish a notification to a pushbullet channel."""
    config = {}
    with open('config.json') as f:
        config = json.load(f)

    pb_url = 'https://api.pushbullet.com/v2/pushes'
    headers = {
        'Content-Type': 'application/json',
        'Access-Token': config['ACCESS_TOKEN'],
    }
    data = {
        'type': 'note',
        'title': 'Prayer times',
        'body': ', '.join(result),
        'channel_tag': 'salahdk-{}'.format(city),
    }
    response = requests.post(
        pb_url,
        data=json.dumps(data),
        headers=headers
    )
    if not response.ok:
        raise Exception('Could not publish to pushbullet')


def parse_city_page(event, context, city='copenhagen'):
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

    _publish_pb_notification(city, result)
