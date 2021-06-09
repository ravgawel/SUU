import socket
from _thread import *


def udp_server(ip, port):
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind((ip, port))
    print('UDP server ' + ip + ':' + str(port) + ' up and listening')

    while True:
        message, address = udp_server_socket.recvfrom(1024)

        print('UDP(' + str(address[0]) + ':' + str(address[1]) + '): ' + message.decode())
        udp_server_socket.sendto(message, address)


def tcp_server(ip, port):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((ip, port))
    tcp_server_socket.listen(5)
    print('TCP server ' + ip + ':' + str(port) + ' up and listening')

    while True:
        connection, address = tcp_server_socket.accept()
        message = connection.recv(1024)

        print('TCP(' + str(address[0]) + ':' + str(address[1]) + '): ' + message.decode())
        connection.send(message)
        connection.close()


if __name__ == '__main__':
    ip_address = "127.0.0.1"
    udp_port = 20001
    tcp_port = 12345

    start_new_thread(udp_server, (ip_address, udp_port))
    tcp_server(ip_address, tcp_port)
