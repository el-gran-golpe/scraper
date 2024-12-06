from __future__ import annotations

from requests import get, Response
from requests.exceptions import ConnectionError
from requests.exceptions import ChunkedEncodingError
from requests.status_codes import codes
from lxml import html

from loguru import logger

from time import sleep
from random import uniform

from fake_useragent import UserAgent
from scrapers.constants.base import MIN_SLEEP_TIME_BETWEEN_REQUESTS_SECONDS, MAX_SLEEP_TIME_BETWEEN_REQUESTS_SECONDS

from scrapers.constants.base import ACCEPT_LANGUAGE


class BaseScraper():
    """
    Class that extract all the information
    """
    def __init__(self, sleep_time_min_seconds: float = MIN_SLEEP_TIME_BETWEEN_REQUESTS_SECONDS,
                 sleep_time_max_seconds: float = MAX_SLEEP_TIME_BETWEEN_REQUESTS_SECONDS):
        # Assigns a random user agent to fake the browser
        user_agent = UserAgent()
        self.header = {'User-Agent': user_agent.random, 'Accept-Language': ACCEPT_LANGUAGE}
        self.information = {}
        self.urls = []

        self.sleep_time_min_seconds = sleep_time_min_seconds
        self.sleep_time_max_seconds = sleep_time_max_seconds

        self.pages_inspected = 0

    def get(self, url: str, connection_max_tries: int = 5, return_url: bool = False, verbose: bool = True) -> (html.HtmlElement | None | tuple[html.HtmlElement, str]):
        """
        Get the content of a web page, taking into account the user agent and the sleep time
        :param url: str. Url of the web page to get
        :param connection_max_tries: int. Maximum number of tries to connect to the web page
        :param return_url: bool. If True, it will return the url of the web page
        :param verbose: bool. If True, it will print the url of the web page

        :return: str. Content of the web page
        """
        assert type(url) == str, f"Url must be a string, not {type(url)}"
        # Check that url have a valid format
        assert url.startswith("http") and " " not in url, f"Url {url} is not valid"
        self.pages_inspected += 1
        if self.pages_inspected % 100 == 0:
            logger.info(f"Pages inspected: {self.pages_inspected}, changing user agent")
            self.header['User-Agent'] = UserAgent().random
        # Wait a random time for neither overwhelm the page nor be easily detected.
        sleep(uniform(a=self.sleep_time_min_seconds, b=self.sleep_time_max_seconds))
        # Make the request and get the HTML of the page
        response = self.get_with_retries(url=url, connection_max_tries=connection_max_tries)
        # If response gets code 200 (ok)
        if response.status_code == codes['ok']:
            if verbose:
                logger.info(f"Page inspected: {url}")
            body = html.fromstring(response.content)
            return (body, response.url) if return_url else body
        # If response gave an error code go to the next url
        else:
            raise ConnectionError(response.url + " gave code " + str(response.status_code))

    def get_with_retries(self, url: str, connection_max_tries: int = 5, sleep_time_between_tries: float = 5) -> Response:
        for connection_attempt in range(connection_max_tries):
            try:
                response = get(url=url, headers=self.header, timeout=10)
                break
            except (ConnectionError, ChunkedEncodingError):
                logger.error(f"Error connecting to {url}, try ({connection_attempt + 1}/{connection_max_tries})")
                sleep(sleep_time_between_tries)
        else:
            raise ConnectionError(f"Error connecting to {url}")
        return response
