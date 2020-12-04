import consul
import time


def testConsul():
    c = consul.Consul()

# poll a key for updates
    index = None
    while True:
        index, data = c.kv.get('test/data/s',index=index)
    #index1, data1 = c.kv.get('test/data/y',index=index)


        print(data)
        print(index)
    #print(data1)
    #print(index1)

# in another process

def test_service_dereg_issue_156():
    # https://github.com/cablehead/python-consul/issues/156
    val = 5
    service_name = str(val)
    c = consul.Consul()
    c.agent.service.register(service_name,address='tcp://127.0.0.1',port=9000)

    #time.sleep(80 / 1000.0)

    print(c.agent.services())
    index = None
    # while True:
    #     index, data = c.agent.service('tcp://127.0.0.1:9000',index=index)

    # Clean up tasks
    c.agent.service.deregister("0")
    c.agent.service.deregister("1")
    c.agent.service.deregister("2")
    c.agent.service.deregister("3")
    c.agent.service.deregister("4")
    c.agent.service.deregister("10")
    c.agent.service.deregister("15")
    c.agent.service.deregister("7")
    if(c.agent.service.deregister("5")) :
        print('anurag')
    val = c.agent.services()
    return val

    #time.sleep(40 / 1000.0)

def sample(val):

    i = 0
    for v in val :
        print(val[v])
        print(i+1)
        i = i+1

val = test_service_dereg_issue_156()
#sample(val)

#testConsul()