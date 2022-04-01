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

    def get_total_clicks(self, bitlink):
        bitlink_without_scheme = parse_bitlink(bitlink)

        endpoint = f'bitlinks/{bitlink_without_scheme}/clicks/summary'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url)
        response.raise_for_status()
        total_clicks = response.json().get('total_clicks')
        return total_clicks


def validate_response(long_url):
    response = requests.get(url=long_url)
    response.raise_for_status()


def parse_bitlink(bitlink):
    parsed_bitlink = urllib.urlparse(bitlink)
    bitlink_without_scheme = parsed_bitlink.netloc + parsed_bitlink.path
    return bitlink_without_scheme


def is_bitlink(long_url):
    bitly_hostname = 'bit.ly'
    parsed_url = urllib.urlparse(long_url)
    if parsed_url.hostname == bitly_hostname:
        return True
    return False


def main(is_bitlink):
    if is_bitlink:
        bitlink = long_url
        total_clicks = bitly_instance.get_total_clicks(bitlink)
        print(f'По ссылке прошли: {total_clicks} раз(а)')
    else:
        bitlink = bitly_instance.create_bitlink(long_url)
        print(f'Битлинк: {bitlink}')


if __name__ == '__main__':
    bitly_instance = BitlyApi(token=GENERIC_ACCESS_TOKEN)
    user = bitly_instance.get_user()

    long_url = str(input('Введите ссылку: '))
    validate_response(long_url)
    is_bitlink = is_bitlink(long_url)
    main(is_bitlink)
