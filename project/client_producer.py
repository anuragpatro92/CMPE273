import zmq
import time
import sys
from itertools import cycle
from consistent_hashing import Consistenthashing
from hrw import Hrw

def create_clients(servers):
    producers = {}
    context = zmq.Context()
    for server in servers:
        print(f"Creating a server connection to {server}...")
        producer_conn = context.socket(zmq.PUSH)
        producer_conn.bind(server)
        producers[server] = producer_conn
    return producers
    

def generate_data_round_robin(servers):
    print("Starting...")
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



def generate_data_consistent_hashing(servers):
    hashring = Consistenthashing(servers,20)
    map = getStats(servers)
    producers = create_clients(servers)
    for num in range(1000000):
        data = { 'key': f'key-{num}', 'value': f'value-{num}' }
        print(f"Sending data:{data}")
        tempnode = hashring.get_node(str(num))
        print('node to send %s' % (tempnode))
        producers[tempnode].send_json(data)
        map[tempnode] = map[tempnode] + 1

    print("DONE")
    print(map)





    
def generate_data_hrw_hashing(servers):
    print("Starting...")
    producers = create_clients(servers)
    hrw = Hrw(servers)
    map = getStats(servers)

    for num in range(1000000):
        data = {'key': f'key-{num}', 'value': f'value-{num}'}
        print(f"Sending data:{data}")
        tempnode = hrw.get_node(num)
        producers[tempnode].send_json(data)
        map[tempnode] = map[tempnode] + 1

    print(map)
    print("Done")
    
    
if __name__ == "__main__":
    servers = []
    num_server = 1
    if len(sys.argv) > 1:
        num_server = int(sys.argv[1])
        print(f"num_server={num_server}")
        
    for each_server in range(num_server):
        server_port = "200{}".format(each_server)
        servers.append(f'tcp://127.0.0.1:{server_port}')
        
    print("Servers:", servers)
    #generate_data_round_robin(servers)
    generate_data_consistent_hashing(servers)
    generate_data_hrw_hashing(servers)
    
