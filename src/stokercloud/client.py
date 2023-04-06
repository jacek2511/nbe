import json
from http.client import HTTPResponse
from urllib import request
from urllib.parse import urljoin
import logging
import time
from stokercloud.controller_data import ControllerData

logger = logging.getLogger(__name__)


class TokenInvalid(Exception):
    pass


class Client:
    BASE_URL = "http://www.stokercloud.dk/"

    def __init__(self, name: str, password: str = None, cache_time_seconds: int = 10):
        self.name = name
        self.password = password
        self.token = None
        self.state = None
        self.last_fetch = None
        self.cache_time_seconds = cache_time_seconds

    def refresh_token(self):
        with request.urlopen(
                urljoin(
                    self.BASE_URL,
                    'v2/dataout2/login.php?user=%s' % self.name
                )
        ) as response:
            data = json.loads(response.read())
            self.token = data['token']  # actual token
            self.state = data['credentials']  # readonly

    def make_request(self, url, *args, **kwargs):
        try:
            if self.token is None:
                raise TokenInvalid()
            absolute_url = urljoin(
                self.BASE_URL,
                "%stoken=%s" % (url, self.token)
            )
            logger.debug(absolute_url)
            with request.urlopen(absolute_url) as data:
                return json.load(data)
        except TokenInvalid:
            self.refresh_token()
            return self.make_request(url, *args, **kwargs)

    def update_controller_data(self):
        self.cached_data = self.make_request("v16bckbeta/dataout2/controllerdata2.php?screen=b1%2C17%2Cb2%2C5%2Cb3%2C4%2Cb4%2C6%2Cb5%2C12%2Cb6%2C14%2Cb7%2C15%2Cb8%2C16%2Cb9%2C9%2Cb10%2C7%2Cd1%2C3%2Cd2%2C4%2Cd3%2C4%2Cd4%2C0%2Cd5%2C0%2Cd6%2C0%2Cd7%2C0%2Cd8%2C0%2Cd9%2C0%2Cd10%2C0%2Ch1%2C2%2Ch2%2C3%2Ch3%2C5%2Ch4%2C13%2Ch5%2C4%2Ch6%2C1%2Ch7%2C9%2Ch8%2C10%2Ch9%2C7%2Ch10%2C8%2Cw1%2C2%2Cw2%2C3%2Cw3%2C9%2Cw4%2C4%2Cw5%2C5&")
        self.last_fetch = time.time()

    def controller_data(self):
        if not self.last_fetch or (time.time() - self.last_fetch) > self.cache_time_seconds:
            self.update_controller_data()
        return ControllerData(self.cached_data)

