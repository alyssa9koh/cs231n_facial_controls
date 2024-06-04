import csv
import os
from pynput import keyboard, mouse
import time


# Defines what functions should be exported
__all__ = ['test_logging_keyboard_main']


LOG_DIRECTORY = './ignore_dump/'


# Function to save input events to a CSV file
def save_to_csv(events, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Event Type', 'Event', 'Timestamp'])
        writer.writerows(events)


def listen_keymouse_inputs():
    # Capture the start time
    start_time = time.time()

    # Keyboard event handler
    def on_key_press(key):
        try:
            event = ('Keyboard', f'Key {key.char} pressed', time.time() - start_time)
        except AttributeError:
            event = ('Keyboard', f'Special key {key} pressed', time.time() - start_time)
        input_events.append(event)

    def on_key_release(key):
        event = ('Keyboard', f'Key {key} released', time.time() - start_time)
        input_events.append(event)
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    # Mouse event handler
    def on_click(x, y, button, pressed):
        if pressed:
            event = ('Mouse', f'Button {button} pressed at ({x}, {y})', time.time() - start_time)
        else:
            event = ('Mouse', f'Button {button} released at ({x}, {y})', time.time() - start_time)
        input_events.append(event)

    def on_scroll(x, y, dx, dy):
        event = ('Mouse', f'Scrolled at ({x}, {y}) with delta ({dx}, {dy})', time.time() - start_time)
        input_events.append(event)


    # File to save the input data
    filename = f'{LOG_DIRECTORY}input_log.csv'

    # Initialize a list to store the input events
    input_events = []

    # Collect events from both keyboard and mouse
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    # Keep the listeners running until keyboard_listener is stopped
    keyboard_listener.join()
    mouse_listener.stop()

    # Save the recorded events to the CSV file
    save_to_csv(input_events, filename)

    print(f"Input events saved to {filename}")


def test_logging_keyboard_main():
    print('Now listening to button inputs from keyboard and mouse, as well as mouse scrolling.')
    print('To exit logging and save what was recorded, press ESC.')
    listen_keymouse_inputs()
