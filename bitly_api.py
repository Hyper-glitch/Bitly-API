import json
import os
import urllib.parse as urllib

import requests


GENERIC_ACCESS_TOKEN = os.environ.get('GENERIC_ACCESS_TOKEN')


class BitlyApi:
    def __init__(self, token):
        self.base_url = 'https://api-ssl.bitly.com/v4/'
        self.OAuth_2 = {'Authorization': f'Bearer {token}'}
        self.session = requests.Session()
        self.session.headers.update(self.OAuth_2)

    def get_user(self):
        endpoint = 'user'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url)
        response.raise_for_status()
        return response.json()

    def create_bitlink(self, long_url):
        endpoint = 'bitlinks'
        body = json.dumps({'long_url': long_url})
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.post(url=url, headers=self.OAuth_2, data=body)
        response.raise_for_status()
        return response.json().get('link')

    def get_clicks_count(self, bitlink):
        bitlink_without_scheme = BitlyApi.parse_bitlink(bitlink)

        endpoint = f'bitlinks/{bitlink_without_scheme}/clicks/summary'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url)
        response.raise_for_status()
        clicks_count = response.json().get('total_clicks')
        return clicks_count

    @staticmethod
    def validate_url(long_url):
        response = requests.get(url=long_url)
        response.raise_for_status()

    @staticmethod
    def parse_bitlink(bitlink):
        parsed_bitlink = urllib.urlparse(bitlink)
        bitlink_without_scheme = parsed_bitlink.netloc + parsed_bitlink.path
        return bitlink_without_scheme


if __name__ == '__main__':
    long_url = str(input())

    bitly_instance = BitlyApi(token=GENERIC_ACCESS_TOKEN)
    user = bitly_instance.get_user()
    BitlyApi.validate_url(long_url=long_url)
    bitlink = bitly_instance.create_bitlink(long_url=long_url)
    clicks_count = bitly_instance.get_clicks_count(bitlink=bitlink)

    print(f'Битлинк {bitlink}\n', f'Количество кликов: {clicks_count}')
