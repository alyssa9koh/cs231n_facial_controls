import pydirectinput
import zmq
import time
import json
# from timeit import default_timer as timer
pydirectinput.PAUSE = 0

# Defines what functions should be exported
__all__ = ['bootup_main', 'pydirectinput_helper_x']


def screen_calibration():    
    print('Calibrating to your screen...')
    # Get the size of the primary monitor
    screen_width, screen_height = pydirectinput.size()
    # Calculate the center of the screen
    center_x = screen_width // 2
    center_y = screen_height // 2
    print('...')
    print('Moving the cursor to the middle of the screen.')
    pydirectinput.moveTo(center_x, center_y, duration=1)
    print('Your screen is now calibrated!')                                                                                    
    print('Feel free to move the mouse however you please.')
    print('The program has recorded the coordinates for the center of your screen already.')
    print('')
    return screen_width, screen_height, center_x, center_y


def zmq_sub_test():
    # Prepare our context and subscriber socket
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # Connect to the publisher server
    socket.connect("tcp://127.0.0.1:5570")

    # Subscribe to the topic "openface"
    socket.setsockopt_string(zmq.SUBSCRIBE, 'openface')

    print("Subscriber connected and waiting for messages...")
    time.sleep(1)
    while True:
        try:
            # Receive the message with a timeout of 100 milliseconds
            message = socket.recv_string(flags=zmq.NOBLOCK)
            if message:
                print(f"Received message!")
                return socket
        except zmq.Again as e:
            # If the operation would block, handle it here
            print("No message sent or received, retrying in 5...")
            time.sleep(5)


def zmq_calibration():
    print('Now let\'s calibrate this project with OpenFace.')
    choice_ready = input('When you\'re ready, please press ENTER...')
    print('')
    print('Please navigate to your local executable of OpenFaceOffline built with ZeroMQ publisher support.')
    print('If you do not have this ready or do not know what this means,')
    print('please refer to the README guide found here: https://github.com/alyssa9koh/cs231n_facial_controls/tree/main/setup')
    print('')
    print('Once you\'ve found the executable, please run it.')
    choice_ready_openface = input('Once it\'s running, please come back to this terminal and press ENTER...')
    print('')

    print('Setting up a simple ZeroMQ subscriber and listening for a publisher...')
    socket = zmq_sub_test()
    print('')
    print('Make sure to keep OpenFaceOffline running.')
    print('If you close it and still want to keep playing, be sure to run this project again.')
    print('')
    return socket

# Function to move the mouse cursor
def pydirectinput_helper_x(pose_Rz, screen_width, center_x):
    # Calculate the new x-coordinate within the screen bounds
    new_x = center_x - int(pose_Rz * (screen_width / 2))
    # Move the mouse cursor to the new x-coordinate
    # start = timer()
    pydirectinput.moveTo(new_x, pydirectinput.position()[1])
    # end = timer()
    # print("it took socket recv string: {}".format(end-start))

# pose_Rz correlates to tilt
def mouse_mvmt_calibration(socket, screen_width, screen_height, center_x, center_y):
    print('Let\'s now test that the mouse moves as intended.')
    smiling = False
    mouth_open = False
    nose_wrinkle = False
    eyebrow_raise = False
    while True:
        try:
            # Receive the message with a timeout of 100 milliseconds
            message = socket.recv_string(flags=zmq.NOBLOCK)

            # Check that the message is valid
            if not message:
                print('Received message, but message is NULL. Ending program.')
                return
            if message == 'openface':
                continue
            data = json.loads(message)
            if isinstance(data, int) or (not isinstance(data, int) and 'pose' not in data):
                # There are other valid messages that won't have pose. So just continue
                continue
            
            if data['au_c']['AU09']: # nose_wrinkle
                if not nose_wrinkle:
                    pydirectinput.keyDown('ctrlleft')
                    nose_wrinkle = True
            else:
                if nose_wrinkle:
                    pydirectinput.keyUp('ctrlleft')
                    nose_wrinkle = False
              
            if data['au_c']['AU25']:
                if not mouth_open:
                    pydirectinput.mouseDown(button='left') 
                    mouth_open = True
            else:
                if mouth_open:
                    pydirectinput.mouseUp(button='left') 
                    mouth_open = False    
            
            if data['au_c']['AU01'] and data['au_c']['AU02'] and data['au_c']['AU05']: # eyebrow_raise
                if not eyebrow_raise:
                    pydirectinput.keyDown('ctrlright')
                    eyebrow_raise = True
            else:
                if eyebrow_raise:
                    pydirectinput.keyUp('ctrlright')
                    eyebrow_raise = False
            
            if data['au_c']['AU10'] and data['au_c']['AU12'] and data['au_c']['AU14'] : # smile :) 
                # Action Units: upper lip raise, lip corner puller, dimpler
                if not smiling:                                              
                    pydirectinput.mouseDown(button='right') # start hold down right click => backing up
                    smiling = True                         
            else:
                if smiling: # end smile 
                    pydirectinput.mouseUp(button='right') # release right hold 
                    smiling = False        

            # Parse out pose_Rz, then limit it to the interval [-1,1]
            pose_Rz = data['pose']['pose_Rz']
            if pose_Rz > 1: pose_Rz = 1
            if pose_Rz < -1: pose_Rz = -1

            pydirectinput_helper_x(pose_Rz, screen_width, center_x)
        except zmq.Again as e:
            pass


def bootup_main():
    screen_width, screen_height, center_x, center_y = screen_calibration()

    socket = zmq_calibration()

    mouse_mvmt_calibration(socket, screen_width, screen_height, center_x, center_y)

