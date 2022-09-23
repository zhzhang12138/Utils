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


def run():
    # 1、连接rabbitmq服务器
    result = get_channer()
    channel = result.get("channel")
    connection = result.get("connection")

    # 2、创建一个名为logs的交换机(用于分发日志),模式是发布订阅模式
    channel.exchange_declare(exchange='logs',
                             exchange_type='fanout')

    message = "I am producer this is my message"
    # 生产者向交换机logs塞消息message
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message,
                          )

    print("发送 {} 成功".format(message))
    # 关闭连接
    connection.close()


if __name__ == '__main__':
    run()
