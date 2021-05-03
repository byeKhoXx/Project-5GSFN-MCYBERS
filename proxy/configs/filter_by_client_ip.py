# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.
"""
from typing import Optional

from ..http.exception import HttpRequestRejected
from ..http.parser import HttpParser
from ..http.codes import httpStatusCodes
from ..http.proxy import HttpProxyBasePlugin

PATH_TO_BLOCK_LIST = "/home/albert752/block_list.txt"

class FilterByClientIpPlugin(HttpProxyBasePlugin):
    """Drop traffic by inspecting incoming client IP address."""

    def before_upstream_connection(
            self, request: HttpParser) -> Optional[HttpParser]:
        with open(PATH_TO_BLOCK_LIST, 'r') as fp:
            ips = fp.read().splitlines()
            fp.close()
        if self.client.addr[0] in ips:
            raise HttpRequestRejected(
                status_code=httpStatusCodes.I_AM_A_TEAPOT, reason=b'I\'m a tea pot',
                headers={
                    b'Connection': b'close',
                }
            )
        return request

    def handle_client_request(
            self, request: HttpParser) -> Optional[HttpParser]:
        return request

    def handle_upstream_chunk(self, chunk: memoryview) -> memoryview:
        return chunk

    def on_upstream_connection_close(self) -> None:
        pass
