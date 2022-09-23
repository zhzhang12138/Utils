# -*- coding:utf-8 -*-
# @FileName  :Client.py
# @Time      :2022/9/23 14:17
# @Author    :John Doe

# _*_coding:utf-8_*_
__author__ = 'Linhaifeng'

import socket

ip_port = ('127.0.0.1', 9000)
BUFSIZE = 1024
udp_server_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def run():
    while True:
        msg = input('>>: ').strip()
        if not msg:
            continue

        udp_server_client.sendto(msg.encode('utf-8'), ip_port)

        back_msg, addr = udp_server_client.recvfrom(BUFSIZE)
        print(back_msg.decode('utf-8'), addr)


if __name__ == '__main__':
    run()
