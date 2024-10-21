import socket

# Configure the local server and the target server
LOCAL_HOST = '0.0.0.0'
LOCAL_PORT = 65432

TARGET_HOST = '192.168.188.239'  # VM's IP address (target address)
TARGET_PORT = 65432  # Replace with the target server's port

def handle_client(client_socket):
    # Create a connection to the target server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
        remote_socket.connect((TARGET_HOST, TARGET_PORT))

        # Receive data from the client and forward it to the target server
        while True:
            client_data = client_socket.recv(4096)
            if not client_data:
                break  # End the loop if there's no more data from the client

            remote_socket.sendall(client_data)

            # Receive the response from the target server and send it back to the client
            server_data = remote_socket.recv(4096)
            if not server_data:
                break  # End the loop if there's no more data from the server

            client_socket.sendall(server_data)

    client_socket.close()

def start_proxy():
    # Create a TCP socket to listen for incoming connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((LOCAL_HOST, LOCAL_PORT))
        server_socket.listen(1)  # Maximum of 1 pending connection
        print(f"[*] Listening on {LOCAL_HOST}:{LOCAL_PORT}")

        # Accept only one client connection
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Handle the client's request
        handle_client(client_socket)

if __name__ == '__main__':
    start_proxy()