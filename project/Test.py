from consistent_hashing import Ring

import hashlib

print(hashlib.algorithms_available)
print(hashlib.algorithms_guaranteed)
server_list = ['127.0.0.1', '127.0.0.2', '127.0.0.3']
ring = Ring(server_list,100)

count = {'127.0.0.1' : 0 , '127.0.0.2' : 0, '127.0.0.3' : 0}

for i in range(0,100):
    count[ring.get_node(str(i))] += 1

print(count)