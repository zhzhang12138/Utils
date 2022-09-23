"""
消费者
"""
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


# 构建回调函数
def callback(ch, method, properties, body):
    print("Received {} 成功.......".format(body))

    # 给mq发送应答信号，表明数据已经处理完成，可以删除
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run():
    # 1、连接rabbitmq服务器
    result = get_channer()
    channel = result.get("channel")
    connection = result.get("connection")

    # 跟队列同理,因为不确定生产者和消费者谁先跑起来,消费者端也要创建交换机
    # 2、创建一个名为direct_logs的交换机，类型为关键字模式。
    channel.exchange_declare(exchange='direct_logs',
                             exchange_type='direct',
                             )

    # 3、创建一个随机队列
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # 4、为随机队列绑定名为direct_logs的交换机,关键字为lan和yue
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key='yue')  # 也推荐用for循环

    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key='chuan')

    print('当前MQ关键字模式正在等待交换机往消息队列塞消息.......要退出请按 CTRL+C.......')

    # 监听随机队列，一旦有值出现，则触发回调函数：callback
    channel.basic_consume(queue=queue_name,
                          auto_ack=False,  # 默认就是False,可以直接不写
                          on_message_callback=callback,
                          )

    # 消费者不止这一个时，谁先处理完谁就去消息队列取
    channel.basic_qos(prefetch_count=1)
    channel.start_consuming()


if __name__ == '__main__':
    run()
