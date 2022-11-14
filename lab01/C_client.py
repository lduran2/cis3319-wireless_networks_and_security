
# standard libraries
import json
import socket

# local library crypto
import run_node
from run_node import servers_config_data, nodes_config_data
from node import Node


class Client:
    '''
    A simple socket client.
    '''

    def __init__(self, addr: str, port: int, buffer_size=1024):
        '''
        Allocates space for the socket client and initializes it.
        @param addr: str = address whereto to connect (without port)
        @param port: int = port of address whereto to connect
        @param buffer_size: int = default buffer size for receiving
                messages
        '''
        # create and store the node
        self.node = Node(addr, port, Client.connect, buffer_size)

    @staticmethod
    def connect(node: Node):
        # connect the socket to the given address and port
        node.s.connect((node.addr, node.port))
        # set connection to socket
        node.conn = node.s

    def send(self, msg_bytes: bytes):
        '''
        Sends the message given by `msg_bytes` through the socket.
        @param msg_bytes: bytes = message to send
        '''
        # delegate to the node
        self.node.send(msg_bytes)

    def recv(self, buffer_size=None) -> bytes:
        '''
        Receives a message from the socket.
        @param buffer_size: int? = size of the receiving buffer
        @return the message received
        '''
        # delegate to the node
        msg_bytes = self.node.recv(buffer_size)
        # return the message
        return msg_bytes

    def close(self):
        '''
        Closes the backing socket.
        '''
        self.node.close()
# end class Client


# ID for this node
ID = "CIS3319USERID"

# corresponding section in configuration file
SECTION = 'C_client'
# split data for both V_server and AS_TGS_server
AS_TGS_SERVER, V_SERVER = (
    servers_config_data[server] for server in ('V_server', 'AS_TGS_server'))
# load node data
NODE = nodes_config_data[SECTION]


# run the client until SENTINEL is given
if __name__ == '__main__':
    run_node.main(NODE.connecting_status, Client, V_SERVER.addr, V_SERVER.port, V_SERVER.charset, NODE.prompt)
# end if __name__ == '__main__'
