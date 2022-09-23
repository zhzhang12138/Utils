# -*- coding:utf-8 -*-
# @FileName  :Client.py
# @Time      :2022/9/23 14:02
# @Author    :John Doe
# import socket
from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8888))


def run():
    while True:
        msg = input('请输入命令：').strip()
        if not msg:
            continue
        client.send(msg.encode('utf-8'))

        cmd_res = client.recv(1024)

        print(cmd_res.decode('utf-8'))


if __name__ == '__main__':
    run()
