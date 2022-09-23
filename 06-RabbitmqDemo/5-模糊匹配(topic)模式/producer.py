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

    # 2、创建一个名为topic_logs的交换机
    channel.exchange_declare(exchange='topic_logs',
                             exchange_type='topic',
                             )

    message = "welcome to rabbitmq  cc"

    # 3、向交换机发送数据,让交换机只给能匹配lan.adasd.*的队列发消息
    channel.basic_publish(exchange='topic_logs',
                          routing_key='lan.adasd.*',
                          body=message,
                          )

    print("Sent {} 成功".format(message))
    # 关闭连接
    connection.close()


if __name__ == '__main__':
    run()
