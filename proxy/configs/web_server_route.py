# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.
    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.
"""
import logging
import requests

from typing import List, Tuple
from ..common.utils import build_http_response
from ..http.parser import HttpParser
from ..http.codes import httpStatusCodes
from ..http.websocket import WebsocketFrame
from ..http.server import HttpWebServerBasePlugin, httpProtocolTypes
from pprint import pprint as pp
import json
import time


logger = logging.getLogger(__name__)
WEBSERVER_IP = "10.0.5.4" # IP of the webserver that is to be protected
PATH_TO_BLOCK_LIST = "/home/albert752/block_list.txt" # Path to the blacklist
CACHE = {"time": 0, "data": None} # Cache variable for the website
MAX_CACHE_TIME = 10 # Maximum number of seconds without refreshing the cache


class WebServerPlugin(HttpWebServerBasePlugin):
    """
    Proxy inbuilt web server that forwards the request to the
    original webserver and then returns a cached response. It
    is also responsible of the temporal IP filtering.
    """

    def routes(self) -> List[Tuple[int, str]]:
        """
        Definition of the available routes and protocols, in this case all.
        NOTE: Only HTTP protocol will work
        :return: list of tuples with the protocols and the routes.
        """
        return [
            (httpProtocolTypes.HTTP, r'/$'),
            (httpProtocolTypes.HTTPS, r'/$'),
            (httpProtocolTypes.WEBSOCKET, r'/$'),
        ]

    def handle_request(self, request: HttpParser) -> None:
        """
        Request handler
        :param request: HttpParser object
        :return: cached webpage from the original webserver
        """
        # Opens the blacklist and parses all the instances
        with open(PATH_TO_BLOCK_LIST, 'r') as fp:
            ips = json.load(fp)
            fp.close()

        # Only responds if the IP is not present or, in case that it is present, if the blocking period
        # has expired.
        if self.client.addr[0] not in list(ips.keys()) or time.time() > ips[self.client.addr[0]]:

            # Check if the cache is old
            if CACHE['time'] + MAX_CACHE_TIME < time.time():
                # If the cache is old, request again the webpage
                response = requests.get("http://" + WEBSERVER_IP).content
                CACHE['time'] = time.time()
                CACHE['data'] = response
                print("******************** serving from webserver **********************")
            else:
                # If not, announce that it is using the cache only for demonstration purposes
                print("******************** serving from cache **********************")
            if request.path == b'/':
                # Finally fill the response with the webpage data
                self.client.queue(memoryview(build_http_response(
                    httpStatusCodes.OK, body=CACHE['data'])))


    def on_websocket_open(self) -> None:
        logger.info('Websocket open')

    def on_websocket_message(self, frame: WebsocketFrame) -> None:
        logger.info(frame.data)

    def on_websocket_close(self) -> None:
        logger.info('Websocket close')