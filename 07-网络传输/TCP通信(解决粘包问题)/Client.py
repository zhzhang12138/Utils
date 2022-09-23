# import socket
from socket import *
import struct
import json

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8081))


def run():
    while True:
        msg = input('请输入命令：').strip()
        if not msg:
            continue
        client.send(msg.encode('utf-8'))

        # 收数据
        # 1、先收4个字节，从中提取接下来要收的头的长度
        x = client.recv(4)
        hander_len = struct.unpack('i', x)[0]

        # 2、接收头并解析
        json_str_bytes = client.recv(hander_len)
        json_str = json_str_bytes.decode('gbk')
        hander_dic = json.loads(json_str)
        total_size = hander_dic['total_size']

        # 3、接收真实的数据
        recv_size = 0
        while recv_size < total_size:
            recv_data = client.recv(1024)  # 本次接收，最大接收1024Bytes
            recv_size += len(recv_data)
            print(recv_data.decode('utf-8'), end='')  # 强调：windows用gbk
        else:
            print()


# 粘包问题出现的原因：
# 1、tcp是流式协议，数据像水流一样黏在一起，没有任何边界区分
# 2、收数据没有收干净，有残留，就会更下一次结果混淆在一起
# 解决的核心法门就是：每次都收干净，不要有任何残留

if __name__ == '__main__':
    run()
