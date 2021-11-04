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

    def get(self, url: str):
        url = self._get_url(url)

    def post(self, url: str, data: dict):
        url = self._get_url(url)

    def put(self, url: str, data: dict):
        url = self._get_url(url)

    def delete(self, url: str):
        url = self._get_url(url)

    def head(self, url: str):
        url = self._get_url(url)

    def options(self, url: str):
        url = self._get_url(url)


class Cloudflare(_BaseAPI):
    ACCESS_TOKEN = utils.api_token("cloudflare")
    AUTHORIZATION_HEADER = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    CONTENT_TYPE_HEADER = {"Content-Type": "application/json"}
    BASE_URL = "https://api.cloudflare.com/client/v4/"

    def __init__(self) -> None:
        super().__init__(
            self.ACCESS_TOKEN,
            self.BASE_URL,
            self.AUTHORIZATION_HEADER,
            self.CONTENT_TYPE_HEADER,
        )


class Dynadot(_BaseAPI):
    ACCESS_TOKEN = utils.api_token("dynadot")


class Vultr(_BaseAPI):
    ACCESS_TOKEN = utils.api_token("vultr")
    AUTHORIZATION_HEADER = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    BASE_URL = "https://api.vultr.com/v2/instances"

    def __init__(self) -> None:
        super().__init__(
            self.ACCESS_TOKEN,
            self.BASE_URL,
            self.AUTHORIZATION_HEADER,
        )
