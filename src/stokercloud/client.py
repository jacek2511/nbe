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
                "%s?token=%s" % (url, self.token)
            )
            logger.debug(absolute_url)
            with request.urlopen(absolute_url) as data:
                return json.load(data)
        except TokenInvalid:
            self.refresh_token()
            return self.make_request(url, *args, **kwargs)

    def update_controller_data(self):
        self.cached_data = self.make_request("v2/dataout2/controllerdata2.php")
        self.last_fetch = time.time()

    def controller_data(self):
        if not self.last_fetch or (time.time() - self.last_fetch) > self.cache_time_seconds:
            self.update_controller_data()
        return ControllerData(self.cached_data)
