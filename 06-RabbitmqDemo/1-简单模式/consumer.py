"""
消费者
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


# 一旦有消息就执行该回调函数(比如减库存操作就在这里面)
def callback(ch, method, properties, body):
    print("消费者端收到来自消息队列中的{}成功".format(json.loads(body)))
    # 数据处理完成，MQ收到这个应答就会删除消息
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # 消费者停止监听队列 开启后每次触发回调函数，就会停止监听队列
    # ch.stop_consuming()


def run():
    # 1、连接rabbitmq服务器
    result = get_channer()
    channel = result.get("channel")

    # 2、两边谁先启动谁创建队列
    # channel.queue_declare(queue='hello',durable=True) # 持久化队列
    channel.queue_declare(queue='hello')

    # 消费者这边监听的队列是hello,一旦有值出现,则触发回调函数：callback
    channel.basic_consume(queue='hello',
                          auto_ack=False,  # 默认就是False,可以直接不写
                          on_message_callback=callback,
                          )

    print('当前MQ简单模式正在等待生产者往消息队列塞消息.......要退出请按 CTRL+C.......')
    # 消费者开始监听队列
    channel.start_consuming()


if __name__ == '__main__':
    run()
