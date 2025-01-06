import time
import os
from pynput.keyboard import Key, Listener
import pygetwindow as gw  # Library to check active windows

# Configuration
TARGET_WINDOW_TITLE = "Exam Browser"  # Replace with part of your browser/tab title
LOG_FILE = "log.txt"

# Initialize counter
switch_count = 0
last_active_window = ""

# Function to log events
def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event}\n")
    print(event)

# Function to monitor active window
def monitor_window():
    global switch_count, last_active_window

    while True:
        try:
            # Get the current active window title
            active_window = gw.getActiveWindowTitle()

            # Check if the user has switched away from the target window
            if active_window and TARGET_WINDOW_TITLE not in active_window:
                if last_active_window != active_window:  # Prevent duplicate logging
                    switch_count += 1
                    log_event(f"Switched away! Total switches: {switch_count}")
                last_active_window = active_window
            else:
                last_active_window = TARGET_WINDOW_TITLE

            time.sleep(1)  # Adjust interval as needed
        except Exception as e:
            log_event(f"Error: {e}")
            break

# Function to handle key presses (if needed for additional monitoring)
def anonymous(key):
    key = str(key).replace("'", "")
    if key == "Key.f12":  # Exit the program on F12 key
        log_event("Examination ended. Exiting...")
        raise SystemExit(0)

# Start monitoring
if __name__ == "__main__":
    # Start monitoring the window switches in a separate thread
    from threading import Thread

    window_thread = Thread(target=monitor_window, daemon=True)
    window_thread.start()

    # Start key listener (optional)
    with Listener(on_press=anonymous) as listener:
        listener.join()
