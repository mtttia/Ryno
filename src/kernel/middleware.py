import os
from src.kernel.response import set_body, add_header, add_middleware, set_body_is_in_bytes
from src.kernel.errors import throw404
import gzip
from io import BytesIO

def addMiddleware(response, route, middleware):
    add_middleware(response, (route, middleware))

def addStaticFolder(response, route, folder):
    addMiddleware(response, route, lambda response, server:  server_static(response, server, folder, route))

def server_static(response, server, folder, route):
    if server["method"] != "GET":
        throw404(response)
        return False
    path_requested = server["path"]
    if path_requested == "":
        path_requested = "index.html"
    if(route != ""):
        folder_requested = server["folder"].split(route)[1]
    else: 
        folder_requested = server["folder"]
    file_path = os.path.join(folder, folder_requested, path_requested)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
        if(gzip_supported(server)):
            content = compress_content(content)
            add_header(response, 'Content-Encoding', 'gzip')
        set_body(response, content)
        set_body_is_in_bytes(response, True)
        add_header(response, 'Content-Type', get_file_type(file_path))
    else:
        throw404(response)
        return False
    
def should_decode_utf8(file_path):
    return file_path.split('.')[-1] in ['html', 'css', 'js']
    
def get_file_type(filename):
    ext = filename.split('.')[-1]
    if ext == 'html':
        return 'text/html'
    elif ext == 'css':
        return 'text/css'
    elif ext == 'js':
        return 'text/javascript'
    elif ext == 'png':
        return 'image/png'
    elif ext == 'jpg' or ext == 'jpeg':
        return 'image/jpeg'
    elif ext == 'gif':
        return 'image/gif'
    elif ext == 'ico':
        return 'image/x-icon'
    else:
        return 'text/plain'
    
def gzip_supported(server):
    return 'gzip' in server["headers"]["Accept-Encoding"]
    
def compress_content(content):
    # Compress content using gzip
    with BytesIO() as buf:
        with gzip.GzipFile(fileobj=buf, mode='w') as f:
            f.write(content)
        compressed_data = buf.getvalue()
    return compressed_data