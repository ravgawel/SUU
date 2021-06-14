from time import time
from time import sleep
from numba import njit
import multiprocessing as mp
from multiprocessing import Pool
import argparse
import math
from multiprocessing.pool import INIT
import sched
import socket
import math
from _thread import *

parser = argparse.ArgumentParser(
    description='Simple Tcp/Udp client to send data to corresponding server')

parser.add_argument(
    '--address', help='Server address. Default is 127.0.0.1', default="127.0.0.1")

parser.add_argument(
    '--udp_port', help='Server udp port. Default is 2405', default=2405)

parser.add_argument(
    '--tcp_port', help='Server tcp port. Default is 2405', default=2405)

parser.add_argument('--peak_tcp_change', help='+- packages per seconds for sinusoid',
                    default=1)

parser.add_argument('--peak_udp_change', help='+- packages per seconds for sinusoid',
                    default=1)

parser.add_argument('--sinus_period', help='How many seconds should the period be. Default is 60',
                    default=60)

parser.add_argument('--tcp_workers', help='How many tcp workers should send packages. Default is 1',
                    default=1)

parser.add_argument('--udp_workers', help='How many udp workers should send packages. Default is 0',
                    default=0)

parser.add_argument('--pps', help='How many packages per seconds per worker. Default is 100',
                    default=100)
args = parser.parse_args()

server_ip = args.address

udp_server_port = args.udp_port
tcp_server_port = args.tcp_port

tcp_sin_modifier = int(args.peak_tcp_change)
udp_sin_modifier = int(args.peak_udp_change)

tcp_workers = int(args.tcp_workers)
udp_workers = int(args.tcp_workers)
pps = int(args.pps)
sinus_modifier = 2*math.pi/int(args.sinus_period)

BUFFER = 4096
testdata = b'x' * BUFFER * 4


def start_udp_client():
    i = 0
    while True:
        next_time = time()+1/(pps+math.sin(time()*sinus_modifier)*udp_sin_modifier)
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        if i % 100 == 0:
            print("UDP %d %f" % (i, time()))
        sock.sendto(testdata, (server_ip, tcp_server_port))
        i += 1
        sock.close()
        while time() < next_time:
            pass


def start_tcp_client():
    i = 0
    while True:
        try:
            next_time = time()+1/(pps+math.sin(time()*sinus_modifier)*tcp_sin_modifier)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if i % 100 == 0:
                print("TCP %d" % i)
            sock.connect((server_ip, tcp_server_port))
            sock.send(testdata)
            i += 1
            sock.close()
            while time() < next_time:
                pass
        except ConnectionResetError:
            pass


if __name__ == '__main__':
    for i in range(tcp_workers):
        p = mp.Process(target=start_tcp_client)
        p.start()
    for i in range(udp_workers):
        p = mp.Process(target=start_udp_client)
        p.start()

    while True:
        pass
