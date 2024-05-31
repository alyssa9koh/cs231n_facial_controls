import pyautogui

from bootup import *


# Get the size of the primary monitor
screen_width, screen_height = pyautogui.size()
# Calculate the center of the screen
center_x = screen_width // 2
center_y = screen_height // 2


def main():
    start()
    print('meow')


if __name__ == "__main__":
    main()

