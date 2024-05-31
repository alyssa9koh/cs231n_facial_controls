import pyautogui

# Defines what functions should be exported
__all__ = ['start']

def screen_calibration():
    print('Calibrating to your screen...')
    # Get the size of the primary monitor
    screen_width, screen_height = pyautogui.size()
    # Calculate the center of the screen
    center_x = screen_width // 2
    center_y = screen_height // 2
    print('...')
    print('Moving the cursor to the middle of the screen.')
    pyautogui.moveTo(center_x, center_y, duration=1)
    print('Your screen is now calibrated!')
    return center_x, center_y

def start():
    print('-----')
    print('Project: CS231N Facial Controls starting...')
    print('')
    center_x, center_y = screen_calibration()
