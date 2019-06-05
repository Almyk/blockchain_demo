import Node

class BlockchainNode(Node.Node):

    def __init__(self, host, port, callback=None):
        super(BlockchainNode, self).__init__(host, port, callback)

        self.rsa_key = None

    def eventNodeMessage(self, node, data):
        # TODO: handle different kinds of communications between nodes here

        type = data['Type']

        if type == 'transaction':
            pass
        if type == 'new_block':
            pass
        pass