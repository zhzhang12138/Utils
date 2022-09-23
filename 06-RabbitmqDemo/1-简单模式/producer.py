"""
生产者
"""
import json

import pika


def get_channer():
    """
    MQ连接
    :return:
    """
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='***.***.***.***', port=5672, virtual_host='/', credentials=credentials,
                                  heartbeat=600, blocked_connection_timeout=300))
    channel = connection.channel()

    result = {
        "connection": connection,
        "channel": channel
    }

    return result


def send_mq(param, queue_name):
    """
    queue_name：队列名称
    param: 传入mq的参数
    """
    # 1、连接rabbitmq服务器
    result = get_channer()
    channel = result.get("channel")
    connection = result.get("connection")

    # 2、创建一个名为hello的队列
    # channel.queue_declare(queue='hello', durable=True) # 持久化队列
    channel.queue_declare(queue=queue_name)

    # 3、如果exchange为空，即简单模式:向名为hello队列中插入字符串Hello World!
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(param),
                          # 持久化队列配置
                          # properties=pika.BasicProperties(
                          #     delivery_mode=2,
                          # )
                          )

    print("发送 ‘{}’ 成功".format(param))
    connection.close()


if __name__ == '__main__':
    param = "Hello World4"
    queue_name = "hello"
    send_mq(param, queue_name)
