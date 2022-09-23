# -*- coding:utf-8 -*-
# @FileName  :Server.py
# @Time      :2022/9/23 14:17
# @Author    :John Doe


# _*_coding:utf-8_*_
__author__ = 'Linhaifeng'

import socket

ip_port = ('127.0.0.1', 9000)
BUFSIZE = 1024
udp_server_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_server_client.bind(ip_port)


def run():
    while True:
        msg, addr = udp_server_client.recvfrom(BUFSIZE)
        print(msg, addr)

        udp_server_client.sendto(msg.upper(), addr)


if __name__ == '__main__':
    run()
