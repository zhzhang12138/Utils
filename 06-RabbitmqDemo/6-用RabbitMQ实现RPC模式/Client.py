import pika
# 用于生成请求的唯一标识correlation_id
import uuid


class RpcClient(object):

    def __init__(self):
        # 连接rabbitmq服务器
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='***.***.***.***'))
        self.channel = self.connection.channel()
        # 创建随机回调队列，你不随机也是可以的，反正必要要传过去
        result = self.channel.queue_declare(queue='',exclusive=True)
        # 拿到这个随机队列名
        self.callback_queue = result.method.queue
        # 监听这个回调队列，一旦有响应结果就促发回调on_response(就是为了对比id)
        self.channel.basic_consume(
            queue=self.callback_queue,
            auto_ack=True,
            on_message_callback=self.on_response
        )
    # 对比id确定这个结果确实是我的响应结果
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        # 用于生成请求的唯一标识
        self.corr_id = str(uuid.uuid4())
        # 向rpc_queue队列中塞消息body,并添加reply_to和correlation_id两个属性
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   # 消息
                                   body=str(n)
                                   )

        while self.response is None:
            # 防止连接自动断开,消费者主线程定时发心跳交互,耗时较长的消息消费
            self.connection.process_data_events()
        return str(self.response)


rpc = RpcClient()
response = rpc.call(2)
print("客户端已发出RPC请求，我客户端这边传了个2给你，想要调用你服务器端的fun函数")
print("客户端拿到本次RPC请求的响应结果:{}".format(response))

if __name__ == '__main__':
    pass