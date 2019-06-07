import Node
import json  # p2p네트워크로 이동되는 모든 데이터는 json이라 가정
import time  # Block에 기록되는 time_stamp는 time.time()으로부터 구해짐
import hashlib  # hashlib.sha256()


class BlockchainNode(Node.Node):

    class Transaction:
        # Transaction의 생성자
        def __init__(self, sender: str, recipient: str, data: str, 
                     digital_signature, public_key):
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
            self.data = data
            self.digital_signature = digital_signature
            self.public_key = public_key


    class Blockchain:

        class Block:
            # Block의 생성자
            def __init__(self, index: int, time_stamp: float, 
                         prev_block_hash, transaction_list: list, nonce: int):
                '''
                index : 
                time_stamp : 불록아 생성된 time, time.time()을 아용해서 구한다. 
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
                pass

        # Blockchain의 생성자
        def __init__(self):
            '''
            chain : 반드시 append_block()메소드로만 chain을 수정해야 한다. 임의로 수정하는 것은 not_defined된 행동이다.
            '''
            self.chain = []
            # Create the genesis block
            # 임의의 genesis block을 생성해서 추가해줘야 한다..!
            self.append_block()


        def resolve_conflicts(self):
            """
            This is our consensus algorithm, it resolves conflicts
            by replacing our chain with the longest one in the network.

            :return: True if our chain was replaced, False if not
            이거 꼭 구현해야하나 ㅠㅠㅠㅠ
            """
            pass


        def append_block():
            '''
            이 함수를 호출하기 전에,
            is_valid_block가 먼저 호출되어야 한다. (예외, genesis 블록 추가할 때는 ㄱㅊ)
            블록체인에 
            '''
            pass


        @property
        def get_last_block(self) -> Block:
            '''
            블록 체인에서 가장 최근에 만들어진 블록을 반환한다.
            '''
            return self.chain[-1]


    # BlockchainNode의 생성자
    def __init__(self, host, port, callback=None):
        super(BlockchainNode, self).__init__(host, port, callback)
        self.transaction_pool = []
        self.private_key = gen_private_key()
        self.public_key = gen_public_key(self.private_key)
        self.node_address = gen_node_address(self.public_key)

    
    @staticmethod
    def gen_private_key():
        '''
        개인키는 난수생성기를 통해 생성
        '''
        pass
    
    
    @staticmethod
    def gen_public_key(private_key):
        '''
        개인키로부터 타원곡선암호화를 사용해서 생성
        '''
        pass
    
    
    @staticmethod
    def gen_node_address(public_key):
        '''
        노드 주소는 공개키로부터 해시함수를 사용해서 생성한다.
        '''
        pass
    
    
    def eventNodeMessage(self, node, data):
        # TODO: handle different kinds of communications between nodes here
        '''
        p2p네트워크로부터 온 json데이터를 data['Type']에 따라서 이벤트 헨들링 하는 method
        '''

        type = data['Type']

        if type == 'transaction':
            pass
        if type == 'new_block':
            pass
        pass

        
    # 아래의 method들은 네트워크의 도움이 필요하다.
    def proof_of_work(func) -> int:
        '''
        작업증명 과정
        node에서 임의로 함수를 전달해서 채굴작업 알고리즘을 바꿀 수 있다.
        mine함수에서 호출되며, nonce값을 반환한다.
        '''
        pass


    # 아래의 함수들은 P2P네트워크의 도움이 필요한 함수들 == Node가 수행하는 함수겠지

    def mine(self, func):
        '''
        transaction pool에 Transaction이 10개 이상 쌓이면,
        pool에서 Transaction 10개를 가지고 Block생성한 다음, Nonce를 구하면, 네트워크로 전송
        만일 다른 노드에서 먼저 Nonce를 전송했다면, 내가 하고있던 mine은 interrupted되고, 
        nonce를 먼저 구한 노드로부터 새로운 Block을 제공받음
        '''
        nonce = proof_of_work(func)


    def gen_transaction(self, sender: str, receiver: str, data: str):
        '''    
        새로운 거래를 생성하는 함수
        sender에서 receiver에게 물품(items)을 전달하는 과정을 Transaction이라고 정의한다.
        1. 사용자는 거래에 들어갈 품목들을 선택한다.(items)
        2. 사용자는 개인키로 전자서명을 생성한다.
        3. Transaction에 공개키를 포함시킨다.
        4. 생성된 Transaction을 P2P네트워크에 전파한다.
        '''
        pass


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

        검증에 통과하면 자신의 transaction pool에 저장하고,
        검증에 실패하면 받은 transaction을 무시한다. (아무 행동도 하지 않는다.)
        '''
        pass


    def is_valid_block(self, block: Block) -> bool:
        '''
        블록 내부에 존재하는 nonce와 이전의 블록을 통해서 정답이 맞는지 검증한다.
        정답인 경우 return True
        아닌 경우 return False

        검증에 통과하면 자신의 블록체인에 추가하고,
        검증에 실패하면 받은 block을 무시한다. (아무 행동도 하지 않는다.)
        '''
        pass
