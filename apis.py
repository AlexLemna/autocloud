import requests
from requests import Response

import utils

STRICT_CHECKING = False


class _BaseAPI:
    NAME: str

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

    def _verify_token(self, url: str, print_results: bool = False) -> Response:
        resp = self.get(url)
        if print_results is True:
            if resp.ok:
                print(f"{self.NAME} API key verified.")
            else:
                print(f"ERROR! {self.NAME} API key NOT verified.")
        return resp


class Cloudflare(_BaseAPI):
    NAME = "Cloudflare"

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
        resp = self._verify_token(req_path, print_results=print_results)
        return resp


class Dynadot(_BaseAPI):
    NAME = "Dynadot"

    def __init__(self) -> None:
        self.ACCESS_TOKEN = utils.api_token("dynadot")
        self.BASE_URL = f"https://api.dynadot.com/api3.xml?key={self.ACCESS_TOKEN}"
        super().__init__(
            self.ACCESS_TOKEN,
            self.BASE_URL,
            {},  # no headers
        )

    def verify_token(self, print_results: bool = False) -> Response:
        # It doesn't seem like Dynadot has a specific 'verify token' API,
        # but the 'account_info' API should serve our purpose. I can't
        # imagine a case when a valid API key returns an invalid user account.
        req_path = self.BASE_URL + "&command=account_info"
        resp = self._verify_token(req_path, print_results=print_results)
        return resp


class Vultr(_BaseAPI):
    NAME = "Vultr"

    def __init__(self) -> None:
        self.ACCESS_TOKEN = utils.api_token("vultr")
        self.AUTHORIZATION_HEADER = {"Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        self.BASE_URL = "https://api.vultr.com/v2/"
        super().__init__(
            self.ACCESS_TOKEN,
            self.BASE_URL,
            self.AUTHORIZATION_HEADER,
        )

    def verify_token(self, print_results: bool = False) -> Response:
        # It doesn't seem like Vultr has a specific 'verify token' API,
        # but the 'account_info' API should serve our purpose. I can't
        # imagine a case when a valid API key returns an invalid user account.
        req_path = self.BASE_URL + "account"
        resp = self._verify_token(req_path, print_results=print_results)
        return resp
