import argparse
import asyncore
import socket
from _thread import *

parser = argparse.ArgumentParser(description='Simple Tcp/Udp server to get data on specific ports and address')

parser.add_argument('--address', help='Ip Address to listen to. Default is 0.0.0.0', default='0.0.0.0')

parser.add_argument('--udp_port', help='Port to listen to for udp data. Default is 2405', default=2405)

parser.add_argument('--tcp_port', help='Port to listen to for tcp data. Default is 2405', default=2405)

args = parser.parse_args()


def udp_server(ip, port):
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind((ip, port))
    print('UDP server ' + ip + ':' + str(port) + ' up and listening')

    while True:
        message, address = udp_server_socket.recvfrom(1024)

        print('UDP(' + str(address[0]) + ':' + str(address[1]) + '): ' + message.decode())
        udp_server_socket.sendto(message, address)


class TcpServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        socket, address = self.accept()
        TcpEchoHandler(socket)


class TcpEchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        msg = self.recv(512)
        print(msg.decode())
        self.close()


if __name__ == '__main__':
    ip_address = args.address
    udp_port = args.udp_port
    tcp_port = args.tcp_port

    start_new_thread(udp_server, (ip_address, udp_port))
    server = TcpServer(ip_address, tcp_port)
    asyncore.loop()
