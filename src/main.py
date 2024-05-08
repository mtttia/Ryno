from src.kernel.response import set_protocol, set_body, set_status, set_status_message, add_header, add_middleware
from src.kernel.middleware import addStaticFolder, addMiddleware
import json

def main(request, response):
    #define here your middleware
    addStaticFolder(response, "", "static")
    addMiddleware(response, "request", testMiddlewareBody)
    addMiddleware(response, "request", testMiddlewareHeader)

    return response


def testMiddlewareBody(response, server):
    set_body(response, json.dumps(server))
    return True

def testMiddlewareHeader(response, server):
    add_header(response, "Content-Type", "application/json")
    set_status(response, 200)
    set_status_message(response, "OK")
    return True