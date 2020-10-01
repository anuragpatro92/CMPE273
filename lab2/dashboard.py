import zmq

# ZeroMQ Context
context2 =zmq.Context()

# Define the socket using the "Context"
sock=context2.socket(zmq.PULL)
sock.bind("tcp://127.0.0.1:3000")

# Run a simple "Echo" Server
while True:
    message=sock.recv()
    message=message.decode()
    reply_msg="received: "+ message
    # sock.send(reply_msg.encode())
    print(reply_msg)