from __future__ import absolute_import

import logging

from ._response import response_seek_wrapper
from ._urllib2_fork import BaseHandler


class HTTPResponseDebugProcessor(BaseHandler):
    handler_order = 900  # before redirections, after everything else

    def http_response(self, request, response):
        pass

    https_response = http_response


class HTTPRedirectDebugProcessor(BaseHandler):

    def http_request(self, request):
        pass

    https_request = http_request
