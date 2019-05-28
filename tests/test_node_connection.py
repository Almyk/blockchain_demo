import Node
import time
import random


def eventCallback(event, server, node, data=None):
    if event == "NODE_MESSAGE":
        print("Message from", node.getName(), "to", server.getName(), "Data:", str(data))
    elif event == "CONNECTED_TO_NODE":
        print("Connection established to ", node.host, node.port, "from", server.host, server.port)

# to solve the "name already used" when testing
port1 = random.randint(1111,9999)
port2 = random.randint(1111,9999)
port3 = random.randint(1111,9999)
port4 = random.randint(1111,9999)

print("port1", port1)
print("port2", port2)
print("port3", port3)
print("port4", port4)

node1 = Node.Node('localhost', port1, eventCallback)
node2 = Node.Node('localhost', port2, eventCallback)
node3 = Node.Node('localhost', port3, eventCallback)
node4 = Node.Node('localhost', port4, eventCallback)

node1.start()
node2.start()
node3.start()
node4.start()

node1.connectToNode('localhost', port2)  # node1 connects to node 2
time.sleep(2)
node2.connectToNode('localhost', port4)
time.sleep(2)
node1.connectToNode('localhost', port3)  # node 1 connects to node 3 -> node 3 should connect to node 2
                                         # and since node 2 is connected to node 4 -> node 3 should connect to node 2
# time.sleep(5)
# print("Messages from node 3")
# node3.sendAll({"test1": "node 3"})     # node 3 should send message to node 1, 2 and 4
# time.sleep(3)
# print("Messages from node 4")
# node4.sendAll({"test2": "node 4"})      # should send to all other nodes in network
time.sleep(3)
print("Messages from node 2")
node2.sendAll({"test3": "node 2"})      # should send to all other nodes in network

node1.stop()
node2.stop()
node3.stop()
node4.stop()

node1.join()
node2.join()
node3.join()
node4.join()

time.sleep(2)  # give the threads time to close
print("All stopped")