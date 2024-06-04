import pyautogui

from bootup import *
from testing import *

def main():
    print('-----')
    print('Project: CS231N Facial Controls starting...')
    print('')

    print('Choose what program you want to run by entering a number and then pressing \'ENTER\':')
    print('0: bootup; 1: test_logging_keyboard; 2: test_accuracy_calc_keyboard')
    main_choice = input('')

    if main_choice == '0':
        bootup_main()
    elif main_choice == '1':
        test_logging_keyboard_main()
    elif main_choice == '2':
        test_accuracy_calc_keyboard_main()
    else:
        print('No valid program selected. Exiting.')

if __name__ == "__main__":
    main()

