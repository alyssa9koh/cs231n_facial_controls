import pyautogui

# Wait for 5 seconds before starting to type to give you time to focus on the input field
pyautogui.sleep(5)

# Type out the string "Hello, world!"
pyautogui.typewrite("Hello, world!")

pyautogui.sleep(5)

# Move the mouse to the position (100, 100) over 2 seconds
pyautogui.moveTo(100, 100, duration=2)

# Move the mouse 50 pixels to the right and 50 pixels down over 1 second
pyautogui.move(150, 150, duration=1)
