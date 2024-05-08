from src.kernel.response import set_body, set_status, set_status_message, add_header

def throw404(response):
    set_body(response, "404 Not Found")
    set_status(response, 404)
    set_status_message(response, "Not Found")
    add_header(response, "Content-Type", "text/plain")

def throw500(response):
    set_body(response, "500 Internal Server Error")
    set_status(response, 500)
    set_status_message(response, "Internal Server Error")
    add_header(response, "Content-Type", "text/plain")
    
    