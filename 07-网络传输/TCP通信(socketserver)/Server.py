# -*- coding:utf-8 -*-
# @FileName  :Server.py
# @Time      :2022/9/23 14:02
# @Author    :John Doe
import socketserver

"""
socket并不能多并发，只能支持一个用户，socketserver 简化了编写网络服务程序的任务，
socketserver是socket的再封装。socketserver在python2中为SocketServer,在python3取消了首字母大
写，改名为socketserver。
socketserver中包含了两种类，一种为服务类（server class），一种为请求处
理类（request handle class）。前者提供了许多方法：像绑定，监听，运行……（也就是建立连接的过
程） 后者则专注于如何处理用户所发送的数据（也就是事务逻辑）。一般情况下，所有的服务，都是先
建立连接，也就是建立一个服务类的实例，然后开始处理用户请求，也就是建立一个请求处理类的实例。
"""


class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # 如果是tcp协议，self.requese=>conn
        print(self.client_address)

        while True:
            try:
                cmd = self.request.recv(1024)
                if not cmd:
                    break
                self.request.send(cmd.upper())
            except Exception:
                break
        self.request.close()


if __name__ == '__main__':
    # 服务端应该做的两件事
    # 第一件事：循环的从半连接池中取出连接请求与其建立双向链接，拿到链接对象
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 8888), MyRequestHandler)
    s.serve_forever()
    # 等同于：
    # while True:
    #     conn,client_addr = server.accept()
    #     启动一个线程(conn,client_addr)

    # 第二件事：拿到链接对象，与其进行通信循环--->handle
