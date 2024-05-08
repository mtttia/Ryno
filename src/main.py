from src.kernel.response import set_protocol, set_body, set_status, set_status_message, add_header, add_middleware
from src.kernel.middleware import addStaticFolder, addMiddleware

def main(request, response):
    #define here your middleware
    addMiddleware(response, "api", testMiddlewareBody)
    addMiddleware(response, "api", testMiddlewareHeader)
    addStaticFolder(response, "", "static")
    addStaticFolder(response, "css", "static/css")
    addStaticFolder(response, "js", "static/js")
    addStaticFolder(response, "fonts", "static/fonts")
    addStaticFolder(response, "images", "static/images")
    addStaticFolder(response, "images/reviews", "static/images/reviews")
    addStaticFolder(response, "images/slides", "static/images/slides")
    addStaticFolder(response, "images/team", "static/images/team")
    addStaticFolder(response, "videos", "static/videos")

    return response


def testMiddlewareBody(response, server):
    set_body(response, "{\"name\":\"Jude\"}")
    return True

def testMiddlewareHeader(response, server):
    add_header(response, "Content-Type", "application/json")
    return True