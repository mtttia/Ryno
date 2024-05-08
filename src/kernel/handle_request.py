import socket
from src.kernel.conf import configuration
import src.main as main
from src.kernel.response import get_body, get_headers, get_protocol, get_status, get_status_message, add_header, get_middlewares, get_body_is_in_bytes
from src.kernel.errors import throw404, throw500

def handle_request(client_socket):
    # Receive the request from the client
    request = client_socket.recv(configuration["max_request_buffer_size"]).decode('utf-8')

    # Parse the request to get the requested file path
    if(request == ''):  # If the request is empty, return
        return
    request_rows = request.split('\r\n')
    method = request_rows[0].split(' ')[0]
    requested_file = request_rows[0].split(' ')[1]
    requested_file = requested_file[1:]  # Remove the leading '/'

    # Construct the full path to the requested file

    get_params = {}

    if "?" in requested_file:
        requested_file = requested_file.split("?")[0]
        if len(requested_file.split("?")) > 1:
            get_params = requested_file.split("?")[1]
            get_params = get_params.split("&")
            get_params = {param.split("=")[0]: param.split("=")[1] for param in get_params}

    headers={}
    body=""
    for row in request_rows[1:]:
        if row == '':
            break
        header = row.split(": ")
        headers[header[0]] = header[1]

        

    response = {
        "body": "",
        "body_is_in_bytes": False,
        "status": 200,
        "status_message": "OK",
        "protocol": "HTTP/1.1",
        "headers": [],
        "middleware": []   
    }

    request = {
        "path": requested_file.split("/")[-1],
        "folder": "/".join(requested_file.split("/")[:-1]),
        "method": method,
        "get": get_params,
        "headers": headers,
    }

    atLeastOneMiddleware = False
    try :
        response = main.main(request, response)
    
        #run all middleware giving them response and next object and function
        middlewares = get_middlewares(response)
        #middlewares in pos 0 there is the path of the middleware and in position 1 there is the function witch need response and next
        #response is the response object that each middleware can update
        #next is the function that the middleware can call to pass the response to the next middleware
        #they should be executed only if the path match the middleware path and one middleware fo go forward must wait for the next function to be called
        
        for middleware in middlewares:
            go_forward = False
            if isInPath(middleware[0], request["folder"]):
                atLeastOneMiddleware = True
                go_forward = middleware[1](response, request)
                if not go_forward:
                    break
    except Exception as e:
        throw500(response)
    finally: 

        if not atLeastOneMiddleware:
            throw404(response)

        add_header(response, 'Content-Length', len(get_body(response)))

        response_text = f"{get_protocol(response)} {get_status(response)} {get_status_message(response)}\r\n"

        #add all header
        for header in get_headers(response):
            response_text += f"{header[0]}: {header[1]}\r\n"

        
        response_text += f"\r\n"
        if(get_body_is_in_bytes(response)):
            response_text = response_text.encode("utf-8") + get_body(response)
        else:
            response_text = response_text.encode("utf-8") + get_body(response).encode("utf-8")

        # Send the response back to the client
        client_socket.sendall(response_text)

        # Close the client socket
        client_socket.close()

def isInPath(path, path_requested):
    return path == path_requested