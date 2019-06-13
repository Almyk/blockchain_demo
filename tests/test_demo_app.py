import Blockchain
import time
import random

port1 = 888
port2 = random.randint(1111,9999)
# port3 = random.randint(1111,9999)
# port4 = random.randint(1111,9999)
# port5 = random.randint(1111,9999)

print("port1", port1)
print("port2", port2)
# print("port3", port3)
# print("port4", port4)
# print("port5", port5)


node1 = Blockchain.BlockchainNode('localhost', port1)
node2 = Blockchain.BlockchainNode('localhost', port2)
# node3 = Blockchain.BlockchainNode('localhost', port3)
# node4 = Blockchain.BlockchainNode('localhost', port4)
# node5 = Blockchain.BlockchainNode('localhost', port5)

node1.start()
node2.start()
# node3.start()
# node4.start()
# node5.start()

node1.join_network('localhost', port2)
# node1.join_network('localhost', port3)
# node1.join_network('localhost', port4)
# node1.join_network('localhost', port5)

# node2.start_mining()
# node4.start_mining()

time.sleep(2)

testan = True
i = 0
cmd = ""
node_list = list()
while testan:
    if cmd == 't':
        msg = 'kebab ' + str(i)
        node2.gen_transaction(node1.node_address, node2.node_address, msg)
        i += 1
    elif cmd == 'y':
        node = Blockchain.BlockchainNode('localhost', random.randint(1111,9999))
        node_list.append(node)
        node.start()
        node.join_network('localhost', port1)
        node.start_mining()
    elif cmd == 'u':
        node = Blockchain.BlockchainNode('localhost', random.randint(1111, 9999))
        node_list.append(node)
        node.start()
        node.join_network('localhost', port1)

    cmd = input("t for transaction,u for user, y for miner: ")
    if not (cmd == 'y' or cmd == 't' or cmd == 'u'):
        testan = False

# node2.stop_mining()
# node4.stop_mining()

for node in node_list:
    node.stop_mining()
    node.stop()

node1.stop()
node2.stop()
# node3.stop()
# node4.stop()
# node5.stop()

node1.join()
node2.join()
# node3.join()
# node4.join()
# node5.join()

for node in node_list:
    node.join()

time.sleep(5)  # give the threads time to close
print("All stopped")