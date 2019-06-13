import Blockchain
import time
import random

port1 = random.randint(1111,9999)
port2 = random.randint(1111,9999)
#port3 = random.randint(1111,9999)

print("port1", port1)
print("port2", port2)
#print("port3", port3)

node1 = Blockchain.BlockchainNode('localhost', port1)
node2 = Blockchain.BlockchainNode('localhost', port2)

node1.start()
node2.start()

node1.connectToNode('localhost', port2)

time.sleep(1)

# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 1")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 2")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 3")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 4")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 5")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 6")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 7")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 8")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 9")
# node1.gen_transaction(node1.node_address, node2.node_address, "falafel 10")
# node2.gen_transaction(node1.node_address, node2.node_address, "kebab 1")
# node2.gen_transaction(node1.node_address, node2.node_address, "kebab 2")
# node2.gen_transaction(node1.node_address, node2.node_address, "kebab 3")
# node2.gen_transaction(node1.node_address, node2.node_address, "kebab 4")
# node2.gen_transaction(node1.node_address, node2.node_address, "kebab 5")

node2.start_mining()

testan = True
i = 0
while testan:
    msg = 'kebab ' + str(i)
    node2.gen_transaction(node1.node_address, node2.node_address, msg)
    i += 1
    cmd = input("y for continue: ")
    if cmd != 'y':
        testan = False

node2.stop_mining()

node1.stop()
node2.stop()
# node3.stop()

node1.join()
node2.join()
# node3.join()

time.sleep(5)  # give the threads time to close
print("All stopped")