import zmq
import sys
import time
# ZeroMQ Context


context=zmq.Context()

# Define the socket using the "Context"
sock=context.socket(zmq.PUSH)
sock.bind("tcp://127.0.0.1:3001")

# Send a "message" using the socket
for i in range(10001):

    time.sleep(0.5)
    print("{}".format(i).encode())
    sock.send("{}".format(i).encode())

# print(sock.recv().decode())

