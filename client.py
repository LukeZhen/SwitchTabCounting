import socket

# Server address
SERVER_IP = "140.138.243.172"   # Replace with the server's IP address
PORT = 5001  # Port number to connect to

def send_file(file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, PORT))

        # Send the file name
        file_name = file_path.split("/")[-1]
        client_socket.sendall(file_name.encode())

        # Send the file content
        with open(file_path, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
        print(f"File {file_name} sent successfully.")

if __name__ == "__main__":
    file_path = "log.txt"  # Replace with the path of the file to send
    send_file(file_path)
