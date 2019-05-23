# Node implementation for a simple P2P network
# for Software Engineering class at Sogang University
#
# Author: Tommy Hansen
# Creation date: 23/05/2019

import socket
import random
import hashlib
import threading


class Node(threading.Thread):

    def __init__(self, host, port):
        super(Node, self).__init__()

        # IP and Port used for connection
        self.host = host
        self.port = port

        # Creates a unique ID for the node
        self.id = self.createUniqueID()

        # List of Inbound nodes
        self.nodesIn = []
        # List of Outbound nodes
        self.nodesOut = []

        # Initialise the server
        self.sock = self.serverInit()

        self.should_terminate = False

    # function to create Unique ID for the node
    def createUniqueID(self):
        id = hashlib.md5()
        temp = self.host + str(self.port) + str(random.uniform(-999, 999))
        id.update(temp.encode('ascii'))
        return id.hexdigest()

    # Creates the TCP/IP socket for connections
    def serverInit(self):
        sock = socket.socket()  # create socket, by default uses AF_INET
        sock.bind(None, self.port)  # None used as host to mean all available interfaces
        sock.settimeout(15.0)  # 15 seconds
        sock.listen()
        return sock

    # The part that is run when calling Node.start(), part of the threading library
    def run(self):
        while not self.should_terminate:  # while thread should not terminate
            pass
