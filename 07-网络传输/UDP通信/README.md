### **udp是无链接的，先启动哪一端都不会报错**

### udp服务端

```
ss = socket()   										 # 创建一个服务器的套接字
ss.bind()       										 # 绑定服务器套接字
inf_loop:       										 # 服务器无限循环
    cs = ss.recvfrom()/ss.sendto()	 # 对话(接收与发送)
ss.close()                        	 # 关闭服务器套接字
```

### udp客户端

```
cs = socket()   								# 创建客户套接字
comm_loop:      						    # 通讯循环
    cs.sendto()/cs.recvfrom()   # 对话(发送/接收)
cs.close()                      # 关闭客户套接字
```