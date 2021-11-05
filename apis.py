import requests
from requests import Response

import utils

STRICT_CHECKING = False


class _BaseAPI:
    def __init__(
        self, token, base_url: str, auth_header: dict, *other_headers: dict
    ) -> None:
        self.token = token
        self.base_url = base_url
        if other_headers:
            self.headers = auth_header
            for header in other_headers:
                self.headers |= header
        else:
            self.headers = auth_header

    def _get_url(self, text: str) -> str:
        if STRICT_CHECKING:
            if self.base_url in text:
                return text
            else:
                return self.base_url + text
        else:
            if "://" in text:
                return text
            else:
                return self.base_url + text

    def get(self, url: str) -> Response:
        _url = self._get_url(url)
        _r = requests.get(url=_url, headers=self.headers)
        return _r

    def post(self, url: str, data: dict) -> Response:
        _url = self._get_url(url)
        _r = requests.post(url=_url, data=data, headers=self.headers)
        return _r

    def put(self, url: str, data: dict) -> Response:
        _url = self._get_url(url)
        _r = requests.put(url=_url, data=data, headers=self.headers)
        return _r

    def delete(self, url: str) -> Response:
        _url = self._get_url(url)
        _r = requests.delete(url=_url, headers=self.headers)
        return _r

    def head(self, url: str) -> Response:
        _url = self._get_url(url)
        _r = requests.head(url=_url, headers=self.headers)
        return _r

    def options(self, url: str) -> Response:
        _url = self._get_url(url)
        _r = requests.options(url=_url, headers=self.headers)
        return _r


class Cloudflare(_BaseAPI):
    def __init__(self) -> None:
        self.ACCESS_TOKEN = utils.api_token("cloudflare")
        self.AUTHORIZATION_HEADER = {"Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        self.CONTENT_TYPE_HEADER = {"Content-Type": "application/json"}
        self.BASE_URL = "https://api.cloudflare.com/client/v4/"
        super().__init__(
            self.ACCESS_TOKEN,
            self.BASE_URL,
            self.AUTHORIZATION_HEADER,
            self.CONTENT_TYPE_HEADER,
        )

    def verify_token(self, print_results: bool = False) -> Response:
        req_path = self.BASE_URL + "user/tokens/verify"
        resp = self.get(req_path)
        if print_results is True:
            if resp.ok:
                print("Cloudflare API key verified.")
            else:
                print("ERROR! Cloudflare API key NOT verified.")
        return resp


class Dynadot(_BaseAPI):
    def __init__(self) -> None:
        self.ACCESS_TOKEN = utils.api_token("dynadot")


class Vultr(_BaseAPI):
    def __init__(self) -> None:
        self.ACCESS_TOKEN = utils.api_token("vultr")
        self.AUTHORIZATION_HEADER = {"Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        self.BASE_URL = "https://api.vultr.com/v2/instances"
        super().__init__(
            self.ACCESS_TOKEN,
            self.BASE_URL,
            self.AUTHORIZATION_HEADER,
        )
