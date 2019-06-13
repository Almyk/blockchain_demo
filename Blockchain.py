import Node
import threading
import json  # p2p네트워크로 이동되는 모든 데이터는 json이라 가정
import time  # Block에 기록되는 time_stamp는 time.time()으로부터 구해짐
import hashlib  # hashlib.sha256()
from fastecdsa import ecdsa,keys,curve,point
# https://pypi.org/project/fastecdsa/
LEVEL = "01"


class BlockchainNode(Node.Node):

    class Transaction:
        # Transaction의 생성자
        def __init__(self, sender: str, recipient: str, item_history: str, digital_signature, public_key):
            '''
            sender : 보내는 사람의 URL
            recipient : 받는 사람의 URL
            data : 거래 과정???? 너무 추상적이잖아...! 구체적으로 정해줄 수 있는 사람...?
            digital_signature : 전자서명, 나중에 transaction검증할 때 사용함
            public_key : sender의 공개키, 나중에 transaction검증할 때 사용함

            *********나중에 digital_signature, public_key type이 정해지면 민우한테 꼭 알리기*************
            '''
            self.sender = sender
            self.recipient = recipient
            self.item_history = item_history
            self.digital_signature = digital_signature
            self.public_key = public_key

        def serialize(self):
            self.digital_signature = (str(self.digital_signature[0]),str(self.digital_signature[1]))
            self.public_key = (str(self.public_key.x),str(self.public_key.y))

        def deserialize(self):
            self.digital_signature = (int(self.digital_signature[0]),int(self.digital_signature[1]))
            self.public_key = point.Point(int(self.public_key[0]),int(self.public_key[1]))

    class Blockchain:

        class Block:
            # Block의 생성자
            def __init__(self, index: int, time_stamp: float,
                         prev_block_hash, transaction_list, nonce: int):
                '''
                index :
                time_stamp : 불록이 생성된 time, time.time()을 이용해서 구한다.
                prev_block_hash : 이전 블록의 hash값
                transaction_list : 블록이 가지고 있는 거래들. Block하나에 10개의 Transaction이 있어야 함
                nonce : 채굴 과정에서 구한 정답
                '''
                self.index = index
                self.time_stamp = time_stamp
                self.prev_block_hash = prev_block_hash
                self.transaction_list = transaction_list
                self.nonce = nonce

            def get_hash_val(self):
                '''
                sha256을 이용해서 block의 hash값을 return
                '''
                merge_string = str(self.index) + str(self.time_stamp) + str(self.prev_block_hash) + str(self.transaction_list) + str(self.nonce)

                return hashlib.sha256(merge_string.encode()).hexdigest()
            def serialize(self):
                temp = ''
                for trans in self.transaction_list:
                    temp += trans +','
                temp = temp[0:-1]
                self.transaction_list = str(temp)
            def deserialize(self):
                temp=[]
                for trans in self.transaction_list.split(','):
                    temp.append(trans)

                self.transaction_list = temp

        # Blockchain의 생성자
        def __init__(self):
            '''
            chain : 반드시 append_block()메소드로만 chain을 수정해야 한다. 임의로 수정하는 것은 not_defined된 행동이다.
            '''
            self.chain = []
            # Create the genesis block
            # 임의의 genesis block을 생성해서 추가해줘야 한다..!
            genesis_block = self.Block(0,0,0,[],0)
            self.append_block(genesis_block)

        def resolve_conflicts(self):
            """
            This is our consensus algorithm, it resolves conflicts
            by replacing our chain with the longest one in the network.

            :return: True if our chain was replaced, False if not
            이거 꼭 구현해야하나 ㅠㅠㅠㅠ
            """
            pass

        def append_block(self,block: Block):
            '''
            이 함수를 호출하기 전에,
            is_valid_block가 먼저 호출되어야 한다. (예외, genesis 블록 추가할 때는 ㄱㅊ)
            블록체인에
            '''
            self.chain.append(block)

        @property
        def get_last_block(self) -> Block:
            '''
            블록 체인에서 가장 최근에 만들어진 블록을 반환한다.
            '''
            return self.chain[-1]

    # BlockchainNode의 생성자
    def __init__(self, host, port, callback=None):
        super(BlockchainNode, self).__init__(host, port, callback)
        self.blockchain = self.Blockchain()
        self.transaction_pool = []
        self.private_key = self.gen_private_key()
        self.public_key = self.gen_public_key(self.private_key)
        self.node_address = self.gen_node_address(self.public_key)
        self.miner = Mine(self)
        self.miner_count = 0

    def gen_keys(self):
        self.private_key = self.gen_private_key()
        self.public_key = self.gen_public_key(self.private_key)
        self.node_address = self.gen_node_address(self.public_key)
        return str(self.private_key)

    def gen_private_key(self):
        '''
        개인키는 난수생성기를 통해 생성
        '''
        return keys.gen_private_key(curve.P256)

    def gen_public_key(self, private_key):
        '''
        개인키로부터 타원곡선암호화(ecdsa)를 사용해서 생성
        '''
        return keys.get_public_key(private_key,curve.P256)

    def gen_node_address(self, public_key):
        '''
        노드 주소는 공개키로부터 해시함수를 사용해서 생성한다.
        '''
        string = str(public_key.x).encode() + str(public_key.y).encode()
        return hashlib.sha256(string).hexdigest()

    def eventNodeMessage(self, node, data):
        '''
        p2p네트워크로부터 온 json데이터를 data['Type']에 따라서 이벤트 헨들링 하는 method
        '''
        type = data['Type']
        if type == 'transaction':
            digital_signature = data['digital_signature']
            public_key = data['public_key']
            sender = data['sender']
            recipient = data['recipient']
            item_history = data['item_history']
            transaction = self.Transaction(sender, recipient, item_history, digital_signature, public_key)
            transaction.deserialize()
            if self.is_valid_transaction(transaction):
                self.transaction_pool.append(transaction.item_history)
                print("A valid transaction was received:")
                print(item_history)

        elif type == 'new_block':
            new_block = self.Blockchain.Block(data['index'],data['time_stamp'],data['prev_block_hash'],data['transaction_list'],int(data['nonce']))
            new_block.deserialize()
            if self.is_valid_block(new_block) is True:
                self.blockchain.append_block(new_block)
                print("A valid block was received:")
                print(data['transaction_list'])

        elif type == 'new_miner':
            print(self.getName(), "miner_count++")
            self.miner_count += 1

        elif type == 'retired_miner':
            print(self.getName(), "miner_count--")
            self.miner_count -= 1

        elif type == 'ask_mine_count':
            host, port = data['Address']

            allnodes = self.getAllNodes()
            for node in allnodes:
                rcv_port = node.port
                rcv_host = node.host
                if host == rcv_host and port == rcv_port:
                    self.sendToNode(node, {'Type': 'miner_count', 'count': self.miner_count})
                    break

        elif type == 'miner_count':
            self.miner_count = data['count']
            if self.callback != None:
                self.callback("update_miner_count", self, node, {'count': self.miner_count})

        elif type == 'ask_transaction_pool':
            host, port = data['Address']

            allnodes = self.getAllNodes()
            for node in allnodes:
                rcv_port = node.port
                rcv_host = node.host
                if host == rcv_host and port == rcv_port:
                    self.sendToNode(node, {'Type': 'transaction_pool', 'pool': self.transaction_pool})
                    break

        elif type == 'transaction_pool':
            self.transaction_pool = data['pool']
            if self.callback != None:
                self.callback("update_transaction_pool", self, node, {'pool': self.transaction_pool})


    def gen_transaction(self, sender: str, receiver: str, data: str):
        '''    
        새로운 거래를 생성하는 함수
        sender에서 receiver에게 물품(items)을 전달하는 과정을 Transaction이라고 정의한다.
        1. 사용자는 거래에 들어갈 품목들을 선택한다.(items)
        2. 사용자는 개인키로 전자서명을 생성한다.
        3. Transaction에 공개키를 포함시킨다.
        4. 생성된 Transaction을 P2P네트워크에 전파한다.
        '''
        ret_str = ""
        if self.get_unique_node_count() >= 5 and self.miner_count >= 2:
            digital_signature = ecdsa.sign(sender + receiver + data, self.private_key)
            new_transaction = self.Transaction(sender,receiver,data,digital_signature,self.public_key)
            new_transaction.serialize()
            jdata = json.dumps(new_transaction.__dict__)
            jdata = json.loads(jdata)
            jdata['Type'] = 'transaction'
            new_transaction.deserialize()
            self.transaction_pool.append(new_transaction.item_history)

            self.sendAll(jdata)
            return ret_str
        else:
            ret_str = "Failed to generate transaction: "
            if self.get_unique_node_count() < 5:
                ret_str += "'Too few users in network' "
            if self.miner_count < 2:
                ret_str += "'Too few miners in network'"
            print(ret_str)
            return ret_str

    def get_blockchain_from_network(self):
        '''
        P2P네트워크로부터 최신의 블록체인을 json형태로 모두 받아옴
        '''
        pass

    def is_valid_transaction (self, transaction: Transaction) -> bool:
        '''
        gen_transaction이후 생성된 Transaction을 전파받은 노드들은 
        Transaction에 포함된 공개키와 전자서명으로 검증을 수행한다.
        통과하면 return True
        실패하면 return False

        eventNodeMessage에서 is_valid_transaction 함수를 호출했을 때,
        검증에 통과하면 자신의 transaction pool에 저장하고,
        검증에 실패하면 받은 transaction을 무시한다. (아무 행동도 하지 않는다.)
        '''
        string = transaction.sender+transaction.recipient+transaction.item_history
        valid = ecdsa.verify(transaction.digital_signature, string,transaction.public_key)

        return valid

    def is_valid_block(self, block: Blockchain.Block) -> bool:
        '''
        블록 내부에 존재하는 nonce와 이전의 블록을 통해서 정답이 맞는지 검증한다.
        정답인 경우 return True
        아닌 경우 return False

        eventNodeMessage에서 is_valid_block 함수를 호출했을 때,
        검증에 통과하면 자신의 블록체인에 추가하고,
        검증에 실패하면 받은 block을 무시한다. (아무 행동도 하지 않는다.)
        '''
        prev = self.blockchain.get_last_block
        if prev.get_hash_val() != block.prev_block_hash:
            print("prev.get_hash_val() != block.prev_block_hash")
        return (block.prev_block_hash == 0 or prev.get_hash_val() == block.prev_block_hash) and (block.get_hash_val() < LEVEL)

    def start_mining(self):
        if not self.miner.is_mining:
            self.miner.start()
            print("%s started mining" % self.node_address)
            self.miner_count += 1
            self.sendAll({'Type': 'new_miner'})

    def stop_mining(self):
        if self.miner.is_mining:
            self.miner.stop_mining()
            # self.miner.join()
            print("%s stopped mining" % self.node_address)
            self.miner_count -= 1
            self.sendAll({'Type': 'retired_miner'})

    def get_unique_node_count(self):
        self.removeClosedConnections()
        allnodes = self.getAllNodes()

        unique_nodes = dict()
        uniq_count = 1
        for node in allnodes:
            port = node.peerPort
            host = node.peerHost
            if port not in unique_nodes.keys():
                unique_nodes[port] = [host]
                uniq_count += 1
            elif host not in unique_nodes[port]:
                hosts = unique_nodes[port]
                hosts.append(host)
                unique_nodes[port] = hosts
                uniq_count += 1

        return uniq_count

    def ask_for_mine_count(self):
        for node in self.nodesOut:
            if not node.shouldTerminate:
                self.sendToNode(node, {'Type': 'ask_mine_count', 'Address': (self.host, self.port)})
                break

    def ask_for_transaction_pool(self):
        for node in self.nodesOut:
            if not node.shouldTerminate:
                self.sendToNode(node, {'Type': 'ask_transaction_pool', 'Address': (self.host, self.port)})
                break

    def join_network(self, host, port):
        self.connectToNode(host, port)
        time.sleep(0.1)
        self.ask_for_mine_count()
        self.ask_for_transaction_pool()
        time.sleep(0.1)

class Mine(threading.Thread):
    def __init__(self, blockchainNode):
        super(Mine, self).__init__()
        self.should_terminate = False
        self.blockchainNode = blockchainNode
        self.is_mining = False

    def run(self):
        '''
        transaction pool에 Transaction이 10개 이상 쌓이면,
        pool에서 Transaction 10개를 가지고 Block생성한 다음, Nonce를 구하면, 네트워크로 전송
        만일 다른 노드에서 먼저 Nonce를 전송했다면, 내가 하고있던 mine은 interrupted되고,
        nonce를 먼저 구한 노드로부터 새로운 Block을 제공받음
        '''
        self.is_mining = True
        while (self.should_terminate == False):
            while len(self.blockchainNode.transaction_pool) < 10:
                time.sleep(2)
                if self.should_terminate:
                    return
            prev = self.blockchainNode.blockchain.get_last_block
            new_transaction = self.blockchainNode.transaction_pool[0:10]
            self.blockchainNode.transaction_pool = self.blockchainNode.transaction_pool[10:]
            block = self.blockchainNode.Blockchain.Block(prev.index + 1, time.time(), prev.get_hash_val(), new_transaction, 0)
            if self.blockchainNode.get_unique_node_count() >= 5 and self.blockchainNode.miner_count >= 2 and self.proof_of_work(block):
                # if hash puzzle is solved send block
                print("new block created")
                self.blockchainNode.blockchain.append_block(block)
                block.serialize()
                data = json.dumps(block.__dict__)
                data = json.loads(data)
                data['Type'] = 'new_block'
                self.blockchainNode.sendAll(data)
                block.deserialize()

        self.is_mining = False

    def proof_of_work(self,block) -> bool:
        '''
        작업증명 과정
        node에서 임의로 함수를 전달해서 채굴작업 알고리즘을 바꿀 수 있다.
        mine함수에서 호출되며, 결과를 구하면 true값을 .
        '''
        block.nonce = 0
        while block.get_hash_val() > LEVEL:
            block.nonce+=1
            # 새로운 블럭이 추가됨
            if self.should_terminate:
                return False
            if self.blockchainNode.blockchain.get_last_block.get_hash_val() != block.prev_block_hash:
                return False
        print("block hash:")
        print(block.get_hash_val())
        return True

    def stop_mining(self):
        self.should_terminate = True
