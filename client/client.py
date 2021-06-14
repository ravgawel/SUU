from numba import njit
import multiprocessing as mp
from multiprocessing import Pool
import argparse
import math
from multiprocessing.pool import INIT
import sched
import socket
import threading
import time
from _thread import *

parser = argparse.ArgumentParser(
    description='Simple Tcp/Udp client to send data to corresponding server')

parser.add_argument(
    '--address', help='Server address. Default is 127.0.0.1', default="127.0.0.1")

parser.add_argument(
    '--udp_port', help='Server udp port. Default is 2405', default=2405)

parser.add_argument(
    '--tcp_port', help='Server tcp port. Default is 2405', default=2405)

parser.add_argument('--peak_tcp', help='How many tcp packets are meant to be sent per second. Default is 5',
                    default=5)

parser.add_argument('--peak_udp', help='How many udp packets are meant to be sent per second. Default is 50',
                    default=50)

parser.add_argument('--sinus_period', help='How many seconds should the period be. Default is 60',
                    default=60)

args = parser.parse_args()

server_ip = args.address
udp_server_port = args.udp_port
tcp_server_port = args.tcp_port

tcp_peak_per_sec = args.peak_tcp
udp_peak_per_sec = args.peak_udp

sinus_period = int(args.sinus_period)

BUFFER = 4096
testdata = b'x' * BUFFER * 4


def start_tcp_client():
    i = 0
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if i % 100 == 0:
                print(i)
            sock.connect((server_ip, tcp_server_port))
            for _ in range(1, 100000):
                i += 1
                sock.send(testdata)
            sock.close()

        except ConnectionResetError:
            pass


if __name__ == '__main__':
    for i in range(3):
        p = mp.Process(target=start_tcp_client)
        p.start()
    while True:
        pass
