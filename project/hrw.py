from hashlib import md5

MOD = 100000000
class Hrw:

    def __init__(self, server_list):
        self.servers = server_list

    def hash(self,val,server):

        info = str(server) + str(val)
        hashed_value = md5(info.encode())
        digit = int(hashed_value.hexdigest(), 16) % MOD
        return digit

    def get_node(self,val):
        server_index = 0
        max = 0
        for i in range(0,len(self.servers)):
            digit = self.hash(val,self.servers[i])
            if digit > max :
                max = digit
                server_index = i

        return self.servers[server_index]


