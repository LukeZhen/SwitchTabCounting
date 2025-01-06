import time
import socket
import pygetwindow as gw

# Configuration
SERVER_IP = "192.168.239.135"  # Replace with the server's IP address
SERVER_PORT = 9999
TARGET_WINDOW_TITLE = "Exam Browser"  # Replace with part of your browser/tab title

switch_count = 0
last_active_window = ""

def log_and_send_event(event, client_socket):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    message = f"{timestamp} - {event}"
    print(message)  # Optional: log to console
    client_socket.sendall(message.encode('utf-8'))  # Send to server

def monitor_window(client_socket):
    global switch_count, last_active_window

    while True:
        try:
            # Get the current active window title
            active_window = gw.getActiveWindowTitle()

            # Check if the user has switched away from the target window
            if active_window and TARGET_WINDOW_TITLE not in active_window:
                if last_active_window != active_window:  # Prevent duplicate logging
                    switch_count += 1
                    log_and_send_event(f"Switched away! Total switches: {switch_count}", client_socket)
                last_active_window = active_window
            else:
                last_active_window = TARGET_WINDOW_TITLE

            time.sleep(1)  # Adjust interval as needed
        except Exception as e:
            log_and_send_event(f"Error: {e}", client_socket)
            break

if __name__ == "__main__":
    try:
        # Connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

            # Start monitoring the window
            monitor_window(client_socket)
    except Exception as e:
        print(f"Connection error: {e}")
