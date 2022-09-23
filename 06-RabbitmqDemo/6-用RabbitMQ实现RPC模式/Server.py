import pika

# 连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='***.***.***.***'))
channel = connection.channel()

# 创建rpc_queue队列
channel.queue_declare(queue='rpc_queue')


# 这个fun就是我们远程要调用的这么一个简单的接口
def fun(n):
    return 100 * n


# body就是来自客户端塞进队列的消息，props就是来自客户端properties里的两个键值对
def on_request(ch, method, props, body):
    n = int(body)
    response = fun(n)
    # 向接收到的props.reply_to队列塞进响应结果response
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    print("服务器端已经把响应结果放进客户端的回调队列了，结果是:{}".format(response))

    # 通知MQ这条消息对应处理成功，可以删除这条消息了
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 消费者不止这一个时，谁先处理完谁就去消息队列取，这句话最好在每个消费者端都加上，这儿服务器端同样也加上
channel.basic_qos(prefetch_count=1)

# 监听rpc_queue队列，一收到来自客户端的消息则促发回调on_request
channel.basic_consume('rpc_queue', on_request)

print("服务器端正在等待客户端往rpc_queue放消息......")

channel.start_consuming()

if __name__ == '__main__':
    pass
