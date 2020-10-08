import zmq
import math
import time
import sys
import random



# ZeroMQ Context

time.sleep(10)
message = 0


while True:

    try :
        context =zmq.Context()

        sock = context.socket(zmq.PULL)
        sock.connect("tcp://127.0.0.1:3001")

        message = sock.recv()
        message = message.decode()
        sock.close()

        time.sleep(0.3)

        if message:
            reply = "root of {} = {}".format(message, math.sqrt(int(message)))

            print("worker")
            print(reply)
            context2 = zmq.Context()
            dashboard = context2.socket(zmq.PUSH)
            dashboard.connect("tcp://127.0.0.1:3000")
            dashboard.send(reply.encode())
            dashboard.close()
    except :
        print('connecting')
        time.sleep(0.05)



