# -*- coding:utf-8 -*-
# @FileName  :Server.py
# @Time      :2022/9/23 14:07
# @Author    :John Doe
import socketserver


class MyRequestHandle(socketserver.BaseRequestHandler):
    def handle(self):
        client_data = self.request[0]
        server = self.request[1]
        print('客户端发过来的数据%s' % client_data)
        client_address = self.client_address
        server.sendto(client_data.upper(), client_address)


if __name__ == '__main__':
    s = socketserver.ThreadingUDPServer(('127.0.0.1', 8080), MyRequestHandle)
    s.serve_forever()
    # 相当于：只负责循环的收
    # while True:
    #     data,client_addr = server.recvfrom(1024)
    #     启动一个线程处理后续的事情（data,client_addr）
