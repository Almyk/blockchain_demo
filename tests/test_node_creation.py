import Node


node1 = Node.Node('localhost', 1111)
node2 = Node.Node('localhost', 2222)
node3 = Node.Node('localhost', 3333)

node1.start()
node2.start()
node3.start()

node1.connectToNode('localhost', 2222)
node2.connectToNode('localhost', 3333)

node1.sendAll({"test": "testan 1"})
node2.sendAll({"test": "testan 2"})
node3.sendAll({"test": "testan 3"})

node1.stop()
node2.stop()
node3.stop()

node1.join()
node2.join()
node3.join()

print("All stopped")

