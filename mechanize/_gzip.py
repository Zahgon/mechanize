from __future__ import absolute_import

import struct
import zlib
from io import DEFAULT_BUFFER_SIZE

from ._urllib2_fork import BaseHandler
from .polyglot import is_py2


CRC_MASK = 0xffffffff
if is_py2:
    CRC_MASK = long(CRC_MASK)


def gzip_prefix():
    # See http://www.gzip.org/zlib/rfc-gzip.html
    pass


def compress_readable_output(src_file, compress_level=6):
    pass


def read_amt(f, amt):
    pass


class UnzipWrapper:
    def __init__(self, fp):
        self.__decoder = zlib.decompressobj(-zlib.MAX_WBITS)
        self.__data = b''
        self.__crc = zlib.crc32(self.__data) & CRC_MASK
        self.__fp = fp
        self.__size = 0
        self.__is_fully_read = False

    def read(self, sz=-1):
        pass

    def readline(self, sz=-1):
        # Dont care about making this efficient
        pass

    def close(self):
        pass

    def fileno(self):
        pass

    def __iter__(self):
        ans = self.readline()
        if ans:
            yield ans

    def next(self):
        pass


def create_gzip_decompressor(zipped_file):
    pass


class HTTPGzipProcessor(BaseHandler):
    handler_order = 200  # response processing before HTTPEquivProcessor

    def __init__(self, request_gzip=False):
        self.request_gzip = request_gzip

    def __copy__(self):
        return self.__class__(self.request_gzip)

    def http_request(self, request):
        pass

    def http_response(self, request, response):
        # post-process response
        pass

    https_response = http_response
    https_request = http_request
