import logging
from pynput import keyboard, mouse
import threading
import time

from .test_utils import save_to_csv


# Defines what functions should be exported
__all__ = ['test_logging_main']


LOG_DIRECTORY = './src/ignore_dump/'
KEYMOUSE_CSV_NAME = 'keymouse_log' # No need to put '.csv' at the end
MOUSE_MVMT_CSV_NAME = 'mouse_mvmt_log'


def sample_mouse_position(input_events, start_time, sample_interval):
    while True:
        x, y = mouse.Controller().position
        event = ('Mouse', f'Moved to ({x}, {y})', time.time() - start_time)
        input_events.append(event)
        logging.info(f'Mouse move event: {event}')
        time.sleep(sample_interval)

def listen_keymouse_inputs(sample_interval=0.1):
    # Capture the start time
    start_time = time.time()

    # Keyboard event handler
    def on_key_press(key):
        try:
            event = ('Keyboard', f'Key {key.char} pressed', time.time() - start_time)
        except AttributeError:
            event = ('Keyboard', f'Special key {key} pressed', time.time() - start_time)
        keymouse_events.append(event)

    def on_key_release(key):
        event = ('Keyboard', f'Key {key} released', time.time() - start_time)
        keymouse_events.append(event)
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    # Mouse event handler
    def on_click(x, y, button, pressed):
        if pressed:
            event = ('Mouse', f'Button {button} pressed', time.time() - start_time)
            # event = ('Mouse', f'Button {button} pressed at ({x}, {y})', time.time() - start_time)
        else:
            event = ('Mouse', f'Button {button} released', time.time() - start_time)
            # event = ('Mouse', f'Button {button} released at ({x}, {y})', time.time() - start_time)
        keymouse_events.append(event)

    def on_scroll(x, y, dx, dy):
        event = ('Mouse', f'Scrolled at ({x}, {y}) with delta ({dx}, {dy})', time.time() - start_time)
        keymouse_events.append(event)


    # Files to save the input data
    keymouse_filename = f'{LOG_DIRECTORY}{KEYMOUSE_CSV_NAME}.csv'
    mouse_mvmt_filename = f'{LOG_DIRECTORY}{MOUSE_MVMT_CSV_NAME}.csv'

    # Initialize lists to store the input events
    keymouse_events = []
    mouse_mvmt_events = []

    # Collect events from both keyboard and mouse
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    # Start a thread to sample mouse position periodically
    mouse_sampling_thread = threading.Thread(target=sample_mouse_position, args=(mouse_mvmt_events, start_time, sample_interval))
    mouse_sampling_thread.daemon = True
    mouse_sampling_thread.start()

    # Keep the listeners running until keyboard_listener is stopped
    keyboard_listener.join()
    mouse_listener.stop()

    # Save the recorded events to the CSV files
    save_to_csv(keymouse_events, keymouse_filename)
    save_to_csv(mouse_mvmt_events, mouse_mvmt_filename)

    print(f"Keymouse input events saved to {keymouse_filename}")
    print(f"Mouse movement events saved to {mouse_mvmt_filename}")


def test_logging_main():
    print('Now listening to button inputs from keyboard and mouse, as well as mouse scrolling.')
    print('To exit logging and save what was recorded, press ESC.')
    listen_keymouse_inputs()
