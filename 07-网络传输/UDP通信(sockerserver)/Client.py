# -*- coding:utf-8 -*-
# @FileName  :Client.py
# @Time      :2022/9/23 14:15
# @Author    :John Doe

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def run():
    while True:
        msg = input('>>>: ').strip()
        client.sendto(msg.encode('gbk'), ('127.0.0.1', 8080))
        res = client.recvfrom(1024)
        print(res)


client.close()

if __name__ == '__main__':
    run()
