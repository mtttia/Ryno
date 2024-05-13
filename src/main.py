from src.kernel.response import set_protocol, set_body, set_status, set_status_message, add_header, add_middleware, set_body_is_in_bytes, get_body
from src.kernel.middleware import addStaticFolder, addMiddleware, gzip_supported, compress_content
import json

def main(request, response):
    #define here your middleware
    addStaticFolder(response, "", "static", [("Content-Language", "en-US")])
    addMiddleware(response, "request", testMiddlewareBody)
    addMiddleware(response, "request", testMiddlewareHeader)
    addMiddleware(response, "request", compressMiddleware)
    return response


def testMiddlewareBody(response, server):
    set_body(response, json.dumps(server))
    return True

def testMiddlewareHeader(response, server):
    add_header(response, "Content-Type", "application/json")
    set_status(response, 200)
    set_status_message(response, "OK")
    return True

def compressMiddleware(response, server):
    if(gzip_supported(server)):
        set_body(response, compress_content(get_body(response).encode("utf-8")))
        add_header(response, 'Content-Encoding', 'gzip')
        set_body_is_in_bytes(response, True)
    return False