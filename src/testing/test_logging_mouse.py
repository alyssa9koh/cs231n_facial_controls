from pynput import keyboard, mouse
import time

from .test_utils import save_to_csv


# Defines what functions should be exported
__all__ = ['test_logging_mouse_main']


LOG_DIRECTORY = './ignore_dump/'


def track_mouse_mvmt():
    # Capture the start time
    start_time = time.time()

    # Handlers here

    # File to save the input data
    filename = f'{LOG_DIRECTORY}input_log.csv'

    # Initialize a list to store the input events
    input_events = []

    # Save the recorded events to the CSV file
    save_to_csv(input_events, filename)

    print(f"Input events saved to {filename}")


def test_logging_mouse_main():
    print('maus')
    