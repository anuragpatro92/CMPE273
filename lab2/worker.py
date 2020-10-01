import zmq
import math
import time

# ZeroMQ Context



while True:

    try :
        context =zmq.Context()

        sock = context.socket(zmq.PULL)
        sock.connect("tcp://127.0.0.1:3001")

        message = sock.recv()
        message = message.decode()
        sock.close()

        time.sleep(1)

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
        time.sleep(2)



# Define the socket using the "Context"




# Run a simple "Echo" Server
