

set_body = lambda response, body: response.update({"body": body})
set_body_is_in_bytes = lambda response, body_is_in_bytes: response.update({"body_is_in_bytes": body_is_in_bytes})
set_status = lambda response, status: response.update({"status": status})
set_status_message = lambda response, status_message: response.update({"status_message": status_message})
set_protocol = lambda response, protocol: response.update({"protocol": protocol})
def add_header(response, key, value):
    headers = get_headers(response)
    #if header already exists delete it form the array
    exists = False
    for i, header in enumerate(headers):
        if header[0] == key:
            headers[i] = (key, value)
            exists = True
            break    
    if not exists:
        headers.append((key, value))
        response.update({"headers": headers})
add_middleware = lambda response, middleware: response["middleware"].append(middleware)

get_body = lambda response: response["body"]
get_body_is_in_bytes = lambda response: response["body_is_in_bytes"]
get_status = lambda response: response["status"]
get_status_message = lambda response: response["status_message"]
get_protocol = lambda response: response["protocol"]
get_headers = lambda response: response["headers"]
get_middlewares = lambda response: response["middleware"]