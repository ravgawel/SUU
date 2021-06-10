import argparse
import sched
import socket
import threading
import time
from _thread import *

parser = argparse.ArgumentParser(description='Simple Tcp/Udp client to send data to corresponding server')

parser.add_argument('--address', help='Server address. Default is 0.0.0.0', default="127.0.0.1")

parser.add_argument('--udp_port', help='Server udp port. Default is 2405', default=2405)

parser.add_argument('--tcp_port', help='Server tcp port. Default is 2405', default=2405)

parser.add_argument('--peak_tcp', help='How many tcp packets are meant to be sent per second. Default is 5',
                    default=5)

parser.add_argument('--peak_udp', help='How many udp packets are meant to be sent per second. Default is 50',
                    default=50)

args = parser.parse_args()

server_ip = args.address
udp_server_port = args.udp_port
tcp_server_port = args.tcp_port

tcp_peak_per_sec = args.peak_tcp
udp_peak_per_sec = args.peak_udp


def send_udp(udp_socket, udp_scheduler, start_time):
    udp_scheduler.enter(1, 1, send_udp,
                        kwargs={'udp_socket': udp_socket, 'udp_scheduler': udp_scheduler, 'start_time': start_time})

    print(time.time())
    for i in range(udp_peak_per_sec):
        udp_socket.sendto(str.encode(f'udp {start_time}'), (server_ip, udp_server_port))

        # msg_from_server = udp_socket.recvfrom(128)
    print(time.time())
    udp_scheduler.run()


def start_udp_packets(start_time):
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_scheduler = sched.scheduler(time.time, time.sleep)
    send_udp(udp_client_socket, udp_scheduler, start_time)


def tcp_client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(message.encode())
    result = sock.recv(1024)
    print(f'message {message} \t result {result}')
    sock.close()


def start_tcp_client():
    while True:
        thread_list = []
        for i in range(tcp_peak_per_sec):
            msg = "Thread #{}, clnt time {}".format(i, time.time())
            client_thread = threading.Thread(
                target=tcp_client, args=(server_ip, tcp_server_port, msg))
            thread_list.append(client_thread)
            client_thread.start()

        [x.join() for x in thread_list]
        print(f'iteration finished {time.time()}')


if __name__ == '__main__':
    start_new_thread(start_udp_packets, (time.time(),))
    start_new_thread(start_tcp_client, ())
    while True:
        pass
