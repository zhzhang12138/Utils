"""
生产者
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


def run():
    # 1、连接rabbitmq服务器
    result = get_channer()
    channel = result.get("channel")
    connection = result.get("connection")

    # 2、声明一个名为direct_logs的交换机,类型为关键字模式
    channel.exchange_declare(exchange='direct_logs',
                             exchange_type='direct',
                             )

    message = "I am producer this is my message Hello!"

    # 3、向交换机发送消息,并告诉交换机只发给绑定了lan或yue关键字的消费者队列
    channel.basic_publish(exchange='direct_logs',
                          routing_key='lan',  # 可以用for循环，不用像这样一个一个加
                          body=message,
                          )
    channel.basic_publish(exchange='direct_logs',
                          routing_key='yue',
                          body=message,
                          )

    print("Sent {} 成功".format(message))
    # 关闭连接
    connection.close()


if __name__ == '__main__':
    run()
