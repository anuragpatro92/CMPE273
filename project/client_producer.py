import zmq
import time
import sys
from itertools import cycle
from consistent_hashing import Consistenthashing
from hrw import Hrw
import consul

hashring = None
producers = {}
all_servers = {}
consumer = None
def create_clients(servers):
    global producers
    context = zmq.Context()
    for server in servers:
        print(f"Creating a server connection to {server}...")
        producer_conn = context.socket(zmq.PUSH)
        producer_conn.bind(server)
        producers[server] = producer_conn



    return producers
    

def generate_data_round_robin(servers):
    print("Starting...")
    global producers
    producers = create_clients(servers)
    pool = cycle(producers.values())
    for num in range(10):
        data = { 'key': f'key-{num}', 'value': f'value-{num}' }
        print(f"Sending data:{data}")
        next(pool).send_json(data)
        time.sleep(1)
    print("Done")


def getStats(servers):

    map = dict()
    for server in servers:
        map[server] = 0
    return map


def create_consumer(server):
    global consumer
    context = zmq.Context()
    consumer = context.socket(zmq.PULL)
    consumer.bind(server)



def generate_data_consistent_hashing(servers):
    global hashring
    global consumer
    hashring = Consistenthashing(servers.values(),1)

    map = getStats(servers.values())
    producers = create_clients(servers.values())
    create_consumer(f'tcp://127.0.0.1:4500')
    for num in range(10):
        data = { 'op' : 'PUT' ,'key': f'key-{num}', 'value': f'value-{num}' }
        print(f"Sending data:{data}")
        tempnode = hashring.get_node(str(num))
        print('node to send %s' % (tempnode))
        producers[tempnode].send_json(data)
        map[tempnode] = map[tempnode] + 1
        time.sleep(1)

    print(map)
    print("Done")


def add_Node(server_port,server_name):
    global hashring
    global producers
    global consumer

    server = 'tcp://127.0.0.1' + str(":") + str(server_port)
    print('adding node .......' + str(server))
    print(consumer)
    servers = [server]
    c = consul.Consul()
    c.agent.service.register(str(server_name), address='tcp://127.0.0.1', port=server_port)

    all_servers[str(server_name)] = server
    producers = create_clients(servers)
    print(len(producers))
    node = hashring.add_node(server)
    data = { "op":"GET_ALL"}
    producers[node].send_json(data)

    raw = consumer.recv_json()
    print(raw)
    raw = raw['Collection']

    print(raw)
    print('sending again after adding')
    for val in raw:
        print(val)
        data = {'op': 'PUT', 'key': val['key'], 'value': val['value']}
        num = val['value'].split("-")[1]
        print(hashring.nodes)
        node = hashring.get_node(num)
        print('sending'+ str(node))
        producers[node].send_json(data)
        time.sleep(1)


    print("DONE")
    print(map)

def remove_Node(server_port,server_name):
    global hashring
    global producers
    global consumer


    server = 'tcp://127.0.0.1' + str(":") + str(server_port)
    print('removing node .......' + str(server))
    data = { "op":"GET_ALL"}
    producers[server].send_json(data)
    raw = consumer.recv_json()
    raw = raw['Collection']

    hashring.remove_node(server)
    producer_conn = producers[server]
    node = producers.pop(server)
    producer_conn.close()

    print(len(producers))

    print(raw)
    for val in raw:
        print(val)
        data = {'op': 'PUT', 'key': val['key'], 'value': val['value']}
        num = val['value'].split("-")[1]
        node = hashring.get_node(num)
        print('sending to' + str(node))
        producers[node].send_json(data)
        time.sleep(1)

    all_servers.pop(str(server_name))
    c = consul.Consul()
    c.agent.service.deregister(str(server_name))

    print("DONE")



    
def generate_data_hrw_hashing(servers):
    print("Starting...")

    servers_ = list(servers.values())
    producers = create_clients(servers_)
    hrw = Hrw(servers_)
    map = getStats(servers_)

    for num in range(10):
        data = { 'op' : 'PUT' ,'key': f'key-{num}', 'value': f'value-{num}' }
        print(f"Sending data:{data}")
        tempnode = hrw.get_node(str(num))
        producers[tempnode].send_json(data)
        map[tempnode] = map[tempnode] + 1
        time.sleep(1)

    print(map)
    print("Done")
def get_All():
    global producers
    global consumer
    print(producers)
    count = 0
    for node in producers:
        data = {"op": "GET_ALL"}
        producers[node].send_json(data)
        raw = consumer.recv_json()
        raw = raw['Collection']
        print('#################')
        print('NODE -' + str(node))
        print(raw)
        count += len(raw)

    print("total keys recieved = " + str(count))

    
if __name__ == "__main__":
    # servers = []
    # num_server = 1
    # if len(sys.argv) > 1:
    #     num_server = int(sys.argv[1])
    #     print(f"num_server={num_server}")
    #
    # for each_server in range(num_server):
    #     server_port = "200{}".format(each_server)
    #     servers.append(f'tcp://127.0.0.1:{server_port}')

    c = consul.Consul()
    services = c.agent.services()

    for each_server in services.keys():
        print(each_server)
        info = services[each_server]

        server_port = info['Port']
        str_info = info['Address'] + str(":") + str(server_port)
        print(str_info)
        all_servers[each_server] = str_info


        
    #print("Servers:", servers)
    #generate_data_round_robin(servers)
    #generate_data_consistent_hashing(all_servers)


    # TestCase 1
    #add_Node(2004, '4')

    #remove_Node(2002,'2')
    #remove_Node(2003,'3')

    #TestCase 2
    #remove_Node(2000,'0')
    #add_Node(2000,'0')

    #print('get_All')
    #get_All()


    #TestCase 3
    generate_data_hrw_hashing(all_servers)
    
