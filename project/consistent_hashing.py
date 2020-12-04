from hashlib import md5
from bisect import bisect

MOD = 1000000
class Consistenthashing(object):

    def __init__(self, server_list, num_replicas=1):

        nodes,hashednodes,map = self.generate_nodes(server_list, num_replicas)
        hashednodes.sort()

        self.num_replicas = num_replicas
        self.nodes = nodes
        self.hnodes = hashednodes
        self.nodes_map = map
        print(self.nodes_map)




    def hash(self,val):
        hashed_value = md5(val.encode())
        digit = int(hashed_value.hexdigest(), 16) % MOD
        return digit


    def generate_nodes(self,server_list, num_replicas):
        nodes = []
        hashedNodes = []
        nodes_map = dict()

        for i in range(num_replicas):
            for server in server_list:
                node = "{0}-{1}".format(server, i)
                nodes.append(node)
                hashedValue = self.hash(node)
                hashedNodes.append(hashedValue)
                nodes_map[hashedValue] = server


        return nodes,hashedNodes,nodes_map

    def get_node(self, val):
        pos = bisect(self.hnodes, self.hash(val))
        if pos == len(self.hnodes):
            return self.nodes_map[self.hnodes[0]]
        else:
            return self.nodes_map[self.hnodes[pos]]


    def add_node(self,server):

        node = "{0}-{1}".format(server,0)
        self.nodes.append(node)
        hashedValue = self.hash(node)
        pos = bisect(self.hnodes, hashedValue)


        if pos == len(self.hnodes):
            prev_node =  self.nodes_map[self.hnodes[0]]
        else:
            prev_node =  self.nodes_map[self.hnodes[pos]]

        self.hnodes.insert(pos, hashedValue)
        self.nodes_map[hashedValue] = server

        return prev_node

    def remove_node(self,server):

        node = "{0}-{1}".format(server, 0)
        pos = self.hnodes.index(self.hash(node)) + 1

        if pos == len(self.hnodes):
            prev_node =  self.nodes_map[self.hnodes[0]]
        else:
            prev_node =  self.nodes_map[self.hnodes[pos]]

        self.nodes.remove(node);
        self.hnodes.remove(self.hash(node))
        self.nodes_map.pop(self.hash(node))



