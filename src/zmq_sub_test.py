'''
This file is intended to test if OpenFace is interacting correctly with ZeroMQ.

This file creates a ZeroMQ subscriber that listens to publishers at the localhost
at port 5570. When it receives a message, it prints it to the terminal.

To run this file: open a terminal, navigate to the directory this file is in, and
run `python zmq_sub_test.py`.

For information on setting up OpenFace with ZeroMQ, see the `setup` folder in this repo.
'''

import zmq

def main():
    # Prepare our context and subscriber socket
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # Connect to the publisher server
    socket.connect("tcp://127.0.0.1:5570")

    # Subscribe to the topic "openface"
    socket.setsockopt_string(zmq.SUBSCRIBE, 'openface')

    print("Subscriber connected and waiting for messages...")

    while True:
        try:
            # Receive the message with a timeout of 100 milliseconds
            message = socket.recv_string(flags=zmq.NOBLOCK)
            if message:
                print(f"Received message: {message}")
        except zmq.Again:
            pass  # No message received within timeout
        except KeyboardInterrupt:
            print("Subscriber interrupted")
            break

if __name__ == "__main__":
    main()
