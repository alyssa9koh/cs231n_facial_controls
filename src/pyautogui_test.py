import pyautogui

# Get the size of the primary monitor
screen_width, screen_height = pyautogui.size()

# Calculate the center of the screen
center_x = screen_width // 2
center_y = screen_height // 2

print(f"The center of the screen is at: ({center_x}, {center_y})")

# Wait for 5 seconds before starting to type to give you time to focus on the input field
pyautogui.sleep(5)

# Type out the string "Hello, world!"
pyautogui.typewrite("Hello, world!")

pyautogui.sleep(5)

# Move the mouse to the position (100, 100) over 2 seconds
pyautogui.moveTo(100, 100, duration=2)

# Move the mouse 50 pixels to the right and 50 pixels down over 1 second
pyautogui.move(150, 150, duration=1)

# Move cursor to center of screen
pyautogui.moveTo(center_x, center_y, duration=3)
