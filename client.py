import socket

# Configuration
SERVER_IP = "192.168.239.135"  # Listen on all interfaces
SERVER_PORT = 9999

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(5)
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Decode and print the message
                    print(f"Received: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_server()
