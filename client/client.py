import socket

server_ip = "127.0.0.1"
udp_server_port = 20001
tcp_server_port = 12345


def send_udp_msg(message):
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_client_socket.sendto(str.encode(message), (server_ip, udp_server_port))

    msg_from_server = udp_client_socket.recvfrom(1024)
    print("Received from the UDP server: " + msg_from_server[0].decode())


def send_tcp_msg(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, tcp_server_port))
    s.send(message.encode())

    msg_from_server = s.recv(1024)
    print('Received from the TCP server:', msg_from_server.decode())
    s.close()


if __name__ == '__main__':
    send_udp_msg("UDP message")
    send_tcp_msg("TCP message")
