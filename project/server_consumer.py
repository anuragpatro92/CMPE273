import zmq
import sys
import consul
from  multiprocessing import Process
import json

servers = dict()
index = 0
import time
data = dict()
def server(port):
    global data
    context = zmq.Context()
    print(f"Started a server at:{port}...")
    consumer = context.socket(zmq.PULL)
    consumer.connect(f"tcp://127.0.0.1:{port}")
    producer = context.socket(zmq.PUSH)
    producer.connect(f"tcp://127.0.0.1:4500")
    
    while True:
        raw = consumer.recv_json()

        if(raw['op'] == 'GET_ALL'):

            print(data)
            json_list = []
            for key in data.keys():
                json_val = {'key' : key , 'value' : data[key]}
                json_list.append(json_val)

            json_string = {'Collection':json_list}

            print(json_string)
            producer.send_json(json_string)
            data.clear()


        elif (raw['op'] == 'PUT'):
            key, value = raw['key'], raw['value']
            print(f"Server_port={port}:key={key},value={value}")
            data[key] = value
        elif(raw['op']== 'GET'):
            print(data)
            json_string = {'key': key, 'value': data[key]}
            producer.send_json(json_string)
            print(json_string)

        
        
if __name__ == "__main__":
    num_server = 1

    c = consul.Consul()

    if len(sys.argv) > 1:
        num_server = int(sys.argv[1])
        print(f"num_server={num_server}")

    for each_server in range(num_server):
        server_port = "200{}".format(each_server)
        print(f"Starting a server at:{server_port}...")
        print(type(server_port))
        process = Process(target=server, args=(server_port,))
        str_index = str(index)
        servers[str(index)] = process
        process.start()
        c.agent.service.register(str_index, address='tcp://127.0.0.1', port=int(server_port))
        index = index+1

    while True:
        services = c.agent.services()

        #remove a server
        if(len(servers)) > len(services):
            print('inside f')

            for key in servers.keys():
                if key not in services:
                    process = servers[key]
                    process.terminate()
                    print('removing a  server......' + str(key))
                    #process.close()
                    servers.pop(key)
                    break


        #add a server
        elif len(servers) < len(services):
            print('inside s')
            for key in services.keys():

                if key not in servers:
                    info = services[key]
                    server_port = info['Port']
                    print('adding a new server......' + str(server_port))
                    print(server_port)
                    process = Process(target=server, args=(str(server_port),))

                    servers[str(key)] = process
                    process.start()
                    break


        time.sleep(1)

    