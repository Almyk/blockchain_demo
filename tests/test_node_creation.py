import Node
import time
import random


def eventCallback(event, server, node, data=None):
    if event == "NODE_MESSAGE":
        print("Message from", node.getName(), "to", server.getName(), "Data:", str(data))

# to solve the "name already used" when testing
port1 = random.randint(1111,9999)
port2 = random.randint(1111,9999)
port3 = random.randint(1111,9999)

node1 = Node.Node('localhost', port1, eventCallback)
node2 = Node.Node('localhost', port2, eventCallback)
node3 = Node.Node('localhost', port3, eventCallback)

node1.start()
node2.start()
node3.start()

node1.connectToNode('localhost', port2)
node2.connectToNode('localhost', port3)

node1.sendAll({"test": "testan 1"})
time.sleep(1)
node2.sendAll({"test": "testan 2"})
time.sleep(1)
node3.sendAll({"test": "testan 3"})

node1.stop()
node2.stop()
node3.stop()

node1.join()
node2.join()
node3.join()

time.sleep(5)  # give the threads time to close
print("All stopped")
exit(0)

