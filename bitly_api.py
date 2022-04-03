import json
import os
import urllib.parse as urllib

import requests


GENERIC_ACCESS_TOKEN = os.environ.get('GENERIC_ACCESS_TOKEN')
BITLY_HOSTNAME = 'bit.ly'
BASE_API_URL = 'https://api-ssl.bitly.com/v4/'
NOT_FOUND_STATUS_CODE = 404
FORBIDDEN_STATUS_CODE = 403


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

    def check_users_token(self) -> dict:
        """Send request to API's 'user' endpoint and return user's info in dict data structure."""
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
        bitlink_without_scheme = parse_long_url(bitlink)

        endpoint = f'bitlinks/{bitlink_without_scheme}/clicks/summary'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url)
        response.raise_for_status()
        total_clicks = response.json().get('total_clicks')
        return total_clicks

    def is_url_bitlink(self, long_url) -> bool:
        """Check if the url is a bitlink."""
        parsed_url = parse_long_url(long_url)
        endpoint = f'bitlinks/{parsed_url}'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url)
        status_code = response.status_code

        if status_code == NOT_FOUND_STATUS_CODE:
            return False
        elif response.ok:
            return True
        elif status_code == FORBIDDEN_STATUS_CODE:
            raise requests.RequestException.response


def validate_response(long_url):
    """Send get request and check response status, if it's OK , url validate, else raise exception."""
    response = requests.get(url=long_url)
    response.raise_for_status()


def parse_long_url(long_url) -> str:
    """Parse and return bitlink without a scheme."""
    parsed_url = urllib.urlparse(long_url)
    url_without_scheme = parsed_url.netloc + parsed_url.path
    return url_without_scheme


def main(long_url):
    """Start the main logic of the program."""
    bitly_instance = BitlyApi(token=GENERIC_ACCESS_TOKEN)
    bitly_instance.check_users_token()

    if bitly_instance.is_url_bitlink(long_url):
        total_clicks = bitly_instance.get_total_clicks(bitlink=long_url)
        print(f'По ссылке прошли: {total_clicks} раз(а)')
    else:
        bitlink = bitly_instance.create_bitlink(long_url)
        print(f'Битлинк: {bitlink}')


if __name__ == '__main__':
    long_url = str(input('Введите ссылку: '))
    validate_response(long_url)
    main(long_url)
