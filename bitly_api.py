import json
import os
import urllib.parse as urllib

import requests


GENERIC_ACCESS_TOKEN = os.environ.get('GENERIC_ACCESS_TOKEN')
BITLY_HOSTNAME = 'bit.ly'
BASE_API_URL = 'https://api-ssl.bitly.com/v4/'


class BitlyApi:
    """Class for creating Bitly API instance."""
    def __init__(self, token):
        """Initiate Bitly API instance.
        Args:
            token: personal access token for authorization to Bitly API.
        """
        self.base_url = BASE_API_URL
        self.OAuth_2 = {'Authorization': f'Bearer {token}'}
        self.session = requests.Session()
        self.session.headers.update(self.OAuth_2)

    def get_user(self) -> dict:
        """Send request to API's 'user' endpoint and return user info in dict data structure."""
        endpoint = 'user'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url)
        response.raise_for_status()
        return response.json()

    def create_bitlink(self, long_url) -> str:
        """Send request to API's 'bitlinks' endpoint and return bitlink."""
        endpoint = 'bitlinks'
        body = json.dumps({'long_url': long_url})
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.post(url=url, headers=self.OAuth_2, data=body)
        response.raise_for_status()
        return response.json().get('link')

    def get_total_clicks(self, bitlink) -> int:
        """Send request to API's to get total clicks on bitlink return total clicks count."""
        bitlink_without_scheme = parse_bitlink(bitlink)

        endpoint = f'bitlinks/{bitlink_without_scheme}/clicks/summary'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url)
        response.raise_for_status()
        total_clicks = response.json().get('total_clicks')
        return total_clicks


def validate_response(long_url):
    """Send get request and check response status, if it's OK , url validate, else raise exception."""
    response = requests.get(url=long_url)
    response.raise_for_status()


def parse_bitlink(bitlink) -> str:
    """Parse and return bitlink without a scheme."""
    parsed_bitlink = urllib.urlparse(bitlink)
    bitlink_without_scheme = parsed_bitlink.netloc + parsed_bitlink.path
    return bitlink_without_scheme


def is_url_bitlink(long_url) -> bool:
    """Check if the url is a bitlink."""
    parsed_url = urllib.urlparse(long_url)
    if parsed_url.hostname == BITLY_HOSTNAME:
        return True
    return False


def main(long_url):
    """Start the main logic of the program."""
    bitly_instance = BitlyApi(token=GENERIC_ACCESS_TOKEN)
    bitly_instance.get_user()

    is_bitlink = is_url_bitlink(long_url)
    if is_bitlink:
        bitlink = long_url
        total_clicks = bitly_instance.get_total_clicks(bitlink)
        print(f'По ссылке прошли: {total_clicks} раз(а)')
    else:
        bitlink = bitly_instance.create_bitlink(long_url)
        print(f'Битлинк: {bitlink}')


if __name__ == '__main__':
    long_url = str(input('Введите ссылку: '))
    validate_response(long_url)
    main(long_url)
