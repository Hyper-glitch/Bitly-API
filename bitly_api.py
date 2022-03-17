import json
import os
import urllib.parse as urllib

import requests


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


if __name__ == '__main__':
    GENERIC_ACCESS_TOKEN = os.environ.get('GENERIC_ACCESS_TOKEN')

    bitly_instance = BitlyApi(token=GENERIC_ACCESS_TOKEN)
    user = bitly_instance.get_user()
    bitlink = bitly_instance.create_bitlink(long_url='https://music.youtube.com')
    print(user, bitlink)
