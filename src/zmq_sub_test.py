'''
This file is intended to test if OpenFace is interacting correctly with ZeroMQ.

This file creates a ZeroMQ subscriber that listens to publishers at the localhost
at port 5570. When it receives a message, it prints it to the terminal.

To run this file: open a terminal, navigate to the directory this file is in, and
run `python zmq_sub_test.py`.
'''

import zmq

def main():
    # Create a ZeroMQ context
    context = zmq.Context()

    # Create a subscriber socket
    subscriber = context.socket(zmq.SUB)

    # Set the topic filter. In this case, we're subscribing to all topics.
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    # Connect to the publisher endpoint
    subscriber.connect("tcp://127.0.0.1:5570")  # Update the IP and port if necessary

    try:
        while True:
            # Receive the message
            message = subscriber.recv_string()

            # Print the received message
            print("Received message:", message)

    except KeyboardInterrupt:
        print("Exiting...")

    # Close the socket and context when done
    subscriber.close()
    context.term()

if __name__ == "__main__":
    main()
