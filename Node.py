# Node implementation for a simple P2P network
# for Software Engineering class at Sogang University
#
# Author: Tommy Hansen
# Creation date: 23/05/2019

import socket
import random
import hashlib
import threading
import json
import time


class Node(threading.Thread):

    def __init__(self, host, port, callback):
        super(Node, self).__init__()

        # IP and Port used for connection
        self.host = host
        self.port = port

        # Used for communicating back events
        self.callback = callback

        # Creates a unique ID for the node
        self.id = self.createUniqueID()

        # List of Inbound nodes
        self.nodesIn = []
        # List of Outbound nodes
        self.nodesOut = []

        # Initialise the server
        self.sock = self.serverInit()

        self.shouldTerminate = False

        self.debug = False

    def setDebug(self, bool):
        self.debug = bool

    # function to create Unique ID for the node
    def createUniqueID(self):
        id = hashlib.md5()
        temp = self.host + str(self.port) + str(random.uniform(-999, 999))
        id.update(temp.encode('ascii'))  # use host+port+randomVal to create a unique id using RSA hash function
        return id.hexdigest()

    def dprint(self, message):
        if self.debug:
            print("Node.dprint: " + message)

    # Creates the TCP/IP socket for connections
    def serverInit(self):
        sock = socket.socket()  # create socket, by default uses AF_INET
        sock.bind((None, self.port))  # None used as host to mean all available interfaces
        sock.settimeout(15.0)  # 15 seconds
        sock.listen()
        return sock

    # NodeConnection is just a basic class to create a connection node
    # if more functionality is needed we should override this in our blockchain implementation
    # and probably inherit NodeConnection in that implementation
    def newConnection(self, conn, address, callback):
        return NodeConnection(self, conn, address, callback)

    def removeClosedConnections(self):
        for node in self.nodesOut:
            if node.shouldTerminate:
                if self.callback != None:
                    self.callback("OUTBOUND_NODE_CLOSED", self, node, {})

                node.join()
                self.nodesOut.pop(self.nodesOut.index(node))

        for node in self.nodesIn:
            if node.shouldTerminate:
                if self.callback != None:
                    self.callback("INBOUND_NODE_CLOSED", self, node, {})

                node.join()
                self.nodesIn.pop(self.nodesOut.index(node))

    # Uses sendToNode to send data to all the other nodes in the network
    def sendAll(self, data):
        # Remove closed connections before trying to send messages to nodes
        self.removeClosedConnections()
        allnodes = list(set(self.nodesIn).union(set(self.nodesOut)))  # all nodes = union of inbound + outbound nodes

        for node in allnodes:
            self.sendToNode(node, data)

    def sendToNode(self, node, data):
        try:
            node.send(data)

        except Exception as e:
            self.dprint("Node.sendToNode: Error while sending data to node (%s) - (%s)" %(node.id, e))

    def connectToNode(self, host, port):
        if host == self.host and port == self.port:
            self.dprint("Node.connectToNode: Can't connect to yourself")
            return

        for node in self.nodesOut:
            if host == node.host and port == node.port:
                self.dprint("Node.connectToNode: Already connect to this node.")
                return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            clientThread = self.newConnection(sock, (host, port), self.callback)
            clientThread.start()
            self.nodesOut.append(clientThread)
            self.eventConnectToNode(clientThread)

            if self.callback != None:
                self.callback("CONNECTED_TO_NODE", self, clientThread, {})

        except Exception as e:
            self.dprint("Node.connectToNode: Error while connecting to node (%s, %s) - (%s)" %(host, port, e))

    def disconnectFromNode(self, node):
        if node in self.nodesOut:
            node.send({"type": "message", "message": "Disconnect"})
            node.stop()
            node.join()
            self.nodesOut.pop(self.nodesOut.index(node))

    def stop(self):
        self.shouldTerminate = True

    # The part that is run when calling Node.start(), part of the threading library
    def run(self):
        while not self.shouldTerminate:  # while thread should not terminate
            try:
                conn, address = self.sock.accept()

                clientThread = self.newConnection(conn, address, self.callback)
                clientThread.start()
                self.nodesIn.append(clientThread)

                if self.callback != None:
                    self.callback("NODE_CONNECTED", self, clientThread, {})
            except:
                # TODO: error handling
                pass


class NodeConnection(threading.Thread):
    def __init__(self, server, sock, address, callback):
        super(NodeConnection, self).__init__()

        self.address = address
        self.host = address[0]
        self.port = address[1]
        self.server = server
        self.sock = sock
        self.callback = callback
        self.shouldTerminate = False

        self.buffer = ""  # Used for messages between nodes

        self.id = self.createUniqueID()  # create ID

    # function to create Unique ID for the node
    def createUniqueID(self):
        id = hashlib.md5()
        temp = self.host + str(self.port) + str(random.uniform(-999, 999))
        id.update(temp.encode('ascii'))  # use host+port+randomVal to create a unique id using RSA hash function
        return id.hexdigest()

    def send(self, data):
        try:
            message = json.dumps(data, seperators=(',', ':')) + "-SEP"
            self.sock.sendall(message.encode('utf-8'))
        except:
            self.server.dprint("NodeConnection.send: Unexpected Error while sending message:")

    def stop(self):
        self.shouldTerminate = True

    # Main loop, run() is required by threading.Thread
    def run(self):
        self.sock.settimeout(15.0)

        while not self.shouldTerminate:
            message = ""

            try:
                # https://docs.python.org/3/library/socket.html
                # Note For best match with hardware and network realities,
                # the value of bufsize should be a relatively small power of 2, for example, 4096.
                message = self.sock.recv(4096)  # return value is a bytes object
                message = message.encode("utf-8")

            except:
                # terminate Node if there is an issue with the connection
                self.shouldTerminate = True

            if message != "":
                try:
                    self.buffer += str(message.decode("utf-8"))
                except:
                    # TODO: print error message
                    pass

                # Get messages one by one using seperator -SEP
                idx = self.buffer.find("-SEP")
                while(idx > 0):
                    data = self.buffer[0:idx]
                    self.buffer = self.buffer[idx+4:]

                    try:
                        data = json.loads(data)

                    except Exception as e:
                        print("NodeConnection.run: message could not be parsed. (%s) (%s) " % (data, e))

                    self.server.eventNodeMessage(self, data)

                    if self.callback != None:
                        self.callback("MESSAGE", self.server, self, data)

                    idx = self.buffer.find("-SEP")
            time.sleep(0.1)

        self.sock.settimeout(None)
        self.sock.close()
        self.server.dprint("NodeConnection: Stopped")