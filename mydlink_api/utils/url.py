import json
import requests
import urllib3
from urllib import parse


class Url:

    def __init__(self, proxy: str, disable_unverified_https_warn: bool = True):
        self.STATUS_CODE_SUCCESS = 200
        self.TYPE_POST = 'post'
        self.TYPE_GET = 'get'
        self.proxies = None
        self.headers_get = {'User-Agent': 'Mozilla/5.0', 'connection': 'Keep-Alive', 'accept': '*/*', 'x-md-lang': 'de',
                            'x-md-app-ver': '02.00.01.75', 'x-md-os-type': 'android', 'x-md-os-version': '7.0'}
        self.headers_post = {'User-Agent': 'Mozilla/5.0', 'connection': 'Keep-Alive', 'accept': '*/*',
                             'Content-Type': 'application/json', 'x-md-lang': 'de', 'x-md-app-ver': '02.00.01.75',
                             'x-md-os-type': 'android', 'x-md-os-version': '7.0'}
        self.headers_stream = {'User-Agent': 'Mozilla/5.0', 'connection': 'Keep-Alive', 'accept': '*/*',
                               'x-md-lang': 'de', 'x-md-app-ver': '02.00.01.75', 'x-md-os-type': 'android',
                               'x-md-os-version': '7.0', 'Content-Type': 'application/x-mpegURL; charset=utf-8'}

        if proxy is not None:
            self.proxies = {'http': '{proxy}'.format(proxy=proxy),
                            'https': '{proxy}'.format(proxy=proxy)
                            }
        if disable_unverified_https_warn:
            urllib3.disable_warnings()

    def get_request(self, url: str, request_type: str = "post", input_json: json = None) -> requests.Response:
        response = None
        try:
            if request_type is self.TYPE_POST:
                response = requests.post(url, headers=self.headers_post, proxies=self.proxies, json=input_json,
                                         verify=False)
            elif request_type is self.TYPE_GET:
                response = requests.get(url, headers=self.headers_get, proxies=self.proxies, verify=False)
        except Exception as e:
            print(str(e))
        return response

    def stream_file(self, url):
        chunks = []
        with requests.get(url, headers=self.headers_stream, proxies=self.proxies, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                chunks.append(chunk)

        full_content = b''.join(chunks)
        return full_content

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
