# 服务端应该满足两个特点
# 1、一致对外提供服务
# 2、并发的服务多个客户端

import subprocess
from socket import *
import struct
import json

server = socket(AF_INET, SOCK_STREAM)  # #创建服务器套接字
server.bind(('127.0.0.1', 8081))  # #把地址绑定到套接字
server.listen(5)  # #监听链接


def run():
    # 服务端应该做的两件事
    # 第一件事：循环的从半连接池中取出连接请求与其建立双向链接，拿到链接对象
    while True:  # 服务器无限循环
        conn, client_addr = server.accept()  # 接受客户端链接

        # 第二件事：拿到链接对象，与其进行通信循环
        while True:  # #通讯循环
            try:
                cmd = conn.recv(1024)
                if not cmd:
                    break
                obj = subprocess.Popen(cmd.decode('utf-8'),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE
                                       )
                stdout_res = obj.stdout.read()  # 正确结果
                stderr_res = obj.stderr.read()  # 错误结果
                totoal_size = len(stdout_res) + len(stderr_res)
                print(stdout_res)
                print(stderr_res)

                # 1、制作头
                hander_dic = {
                    'filename': "a.txt",
                    'total_size': totoal_size,
                    'md5': "123456789"
                }
                json_str = json.dumps(hander_dic)
                json_str_bytes = json_str.encode('gbk')

                print(len(json_str_bytes))
                # 2、先把头的长度发过去
                x = struct.pack('i', len(json_str_bytes))
                conn.send(x)

                # 3、发头信息
                conn.send(json_str_bytes)

                # 4、再发真实的数据
                conn.send(stdout_res)  # 命令的执行结果
                conn.send(stderr_res)  # 命令的执行结果

            except Exception as e:
                break
        conn.close()


if __name__ == '__main__':
    run()


"""
出现  OSError: [Errno 48] Address already in use
1、首先 lsof -i :8081  查看端口
2、kill PID  杀死占用端口的进程即可
"""
