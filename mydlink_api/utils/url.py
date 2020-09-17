import json
from urllib import parse

import requests


class Url:

    def __init__(self, proxy: str):
        self.TYPE_POST = 'post'
        self.TYPE_GET = 'get'
        self.proxies = None
        self.headers_get = {'User-Agent': 'Mozilla/5.0', 'connection': 'Keep-Alive', 'accept': '*/*', 'x-md-lang': 'de','x-md-app-ver': '02.00.01.75','x-md-os-type': 'android','x-md-os-version': '7.0'}
        self.headers_post = {'User-Agent': 'Mozilla/5.0', 'connection': 'Keep-Alive', 'accept': '*/*','Content-Type': 'application/json','x-md-lang': 'de','x-md-app-ver': '02.00.01.75','x-md-os-type': 'android','x-md-os-version': '7.0'}
        if proxy is not None:
            self.proxies = {'http': '{proxy}'.format(proxy=proxy),
                            'https': '{proxy}'.format(proxy=proxy)
                            }

    def get_request(self, url: str, type: str = "post", input_json: json = None) -> requests.Response:
        response = None
        try:
            if type is self.TYPE_POST:
                response = requests.post(url, headers=self.headers_post, proxies=self.proxies, json=input_json)
            elif type is self.TYPE_GET:
                response = requests.get(url, headers=self.headers_get, proxies=self.proxies)
        except Exception as e:
            print(str(e))
        return response

    @staticmethod
    def get_params(response: requests.Response) -> dict:
        url_params = dict
        if response is not None:
            for history in response.history:
                if history.status_code == 302:
                    url_params = parse.parse_qs(parse.urlparse(history.headers['Location']).query)
        return url_params

    @staticmethod
    def parse(value) -> json:
        try:
            return json.loads(value)
        except ValueError as e:
            print('invalid json: %s' % e)
            return None
