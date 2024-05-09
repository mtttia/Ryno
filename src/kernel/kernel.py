import socket
from src.kernel.handle_request import handle_request
from src.kernel.conf import configuration
from threading import Thread


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the host and port
        server_socket.bind((configuration["HOST"], configuration["PORT"]))

        # Listen for incoming connections
        server_socket.listen()

        host = configuration["HOST"]
        port = configuration["PORT"]
        print(f"Server is running on http://{host}:{port}")

        while True:
            # Accept incoming connections
            client_socket, address = server_socket.accept()
            print(f"Connection from {address} has been established.")

            # Handle the client's request
            Thread(target=handle_request, args=(client_socket,)).start()
            
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError:
        port = configuration["PORT"]
        print(f"Address {port} already in use, try change port in src/kernel/conf.py")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()