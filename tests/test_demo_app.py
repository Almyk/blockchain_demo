import Blockchain
import time
import random

port1 = 889
port2 = random.randint(1111,9999)
port3 = random.randint(1111,9999)
port4 = random.randint(1111,9999)
port5 = random.randint(1111,9999)

print("port1", port1)
print("port2", port2)
print("port3", port3)
print("port4", port4)
print("port5", port5)


node1 = Blockchain.BlockchainNode('localhost', port1)
node2 = Blockchain.BlockchainNode('localhost', port2)
node3 = Blockchain.BlockchainNode('localhost', port3)
node4 = Blockchain.BlockchainNode('localhost', port4)
node5 = Blockchain.BlockchainNode('localhost', port5)

node1.start()
node2.start()
node3.start()
node4.start()
node5.start()

node1.connectToNode('localhost', port2)
node1.connectToNode('localhost', port3)
node1.connectToNode('localhost', port4)
node1.connectToNode('localhost', port5)

node2.start_mining()
node4.start_mining()

time.sleep(2)

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
node4.stop_mining()

node1.stop()
node2.stop()
node3.stop()
node4.stop()
node5.stop()

node1.join()
node2.join()
node3.join()
node4.join()
node5.join()

time.sleep(5)  # give the threads time to close
print("All stopped")