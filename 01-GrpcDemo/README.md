## Protobuf 介绍

Protobuf 是 Google 给出的一种通用的数据表示方式，通过 proto 文件定义的数据格式，可以一键式的生成 C++，Python，Java 等各种语言实现

protobuf经历了protobuf2和protobuf3，pb3比pb2简化了很多，目前主流的版本是pb3

![image-20220111143156845](https://picture-typora-bucket.oss-cn-shanghai.aliyuncs.com/typora/image-20220111143156845.png)

## Python使用grpc相互通信

### 目录结构

```python
-grpc  																  # 包名
  -proto                   			 				# 文件夹
    -HrlloWorldService.proto     				# 自己定义的proto 
    -HrlloWorldService_pb2.py 	 				# 命令生成
    -HrlloWorldService_pb2_grpc.py      # 命令生成
  -client.py               					    # rpc客户端
  -server.py              		   			  # rpc服务端
```

### helloworld.proto

```protobuf
syntax = "proto3";

// 请求参数对象
message HelloWorldRequest {
  string name = 1;
}

// 返回参数对象
message HelloWorldResponse {
  string message = 1;
}

// 对外暴露的服务
service HelloWorld {
  // 对外暴露的函数名，参数和返回值
  rpc SendSms (HelloWorldRequest) returns (HelloWorldResponse) {};
}

```

### 生成proto的python文件

```python
# 通过book.proto生成py脚本文件，
# --python_out=.        跟proto相关的python脚本，输出到当前路径
# --grpc_python_out=.   给grpc用的文件，输出到当前路径
# -I. HrlloWorldService.proto        从当前路径下找HrlloWorldService.proto
python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. HrlloWorldService.proto

# 切换到proto文件夹下执行
# 会生成HrlloWorldService_pb2.py    HrlloWorldService_pb2_grpc.py
```

### server.py

```python
from concurrent import futures

import grpc

from proto import HrlloWorldService_pb2
from proto import HrlloWorldService_pb2_grpc


class SendResponse(HrlloWorldService_pb2_grpc.HelloWorldServicer):  # 必须继承RonService_pb2_grpc.RonService

    def SendSms(self, request, context):  # 参数固定
        print("接收：", 'Hello, %s!' % request.name)
        return HrlloWorldService_pb2.HelloWorldResponse(message='Hello, %s!' % request.name)


def serve():
    # 1 实例化server，grpc提供的，使用线程池跑，具备并发能力
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 2  把server和我们定义的Greeter()绑定，本质是把Greeter()注册到server中
    HrlloWorldService_pb2_grpc.add_HelloWorldServicer_to_server(SendResponse(), server)
    # 3 启动server
    # server.add_insecure_port('[::]:50051')
    server.add_insecure_port('0.0.0.0:50051')
    # 4 启动server
    server.start()
    # 5 不让主程序结束，阻塞
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

```

### client.py

```python
import grpc

from proto import HrlloWorldService_pb2
from proto import HrlloWorldService_pb2_grpc

if __name__ == "__main__":
    client = HrlloWorldService_pb2_grpc.HelloWorldStub(grpc.insecure_channel("0.0.0.0:50051"))
    response = client.SendSms(
        HrlloWorldService_pb2.HelloWorldRequest(name="Word"))
    print(response.message)

```

### 注意

```python
# 生成的RonService_pb2_grpc.py 因为引用了RonService_pb2.py，包导入会有问题
# 需要修改第五行为
from proto import RonService_pb2 as RonService__pb2
```

### 运行服务端，运行客户端

```python
python3 server.py # 运行服务端

python3 client.py # 运行客户端
```

