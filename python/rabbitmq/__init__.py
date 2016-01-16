# -*- coding: utf-8 -*-
"""
@auther: haining <ci_knight@msn.cn>
"""

import pika


RABBITMQ_USER = 'wifiplus'
RABBITMQ_PASS = 'wifiplus'
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = 5672


class Manager(object):
    """
    RabbitMQ API, you can use it and send or receive message.
    usage :
        >>> rabbit = Manage()
        >>> test_manage.send('queue', 'msg')
        >>> test_manage.receive('queue', callback)
    """
    def __init__(self):
        self.__credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)  # 证书
        # 这里可以连接远程IP，请记得打开远程端口  heartbeat_interval=10
        self.__parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT,
                                                      '/', self.__credentials, heartbeat_interval=600)
        self.__connection = pika.BlockingConnection(self.__parameters)
        self.__channel = self.__connection.channel()

    def connection(self):
        self.__connection = pika.BlockingConnection(self.__parameters)
        self.__channel = self.__connection.channel()

    def __set_channel(self, queue, durable=True):
        # channel durable == queue durable
        self.__channel.queue_declare(queue=queue, durable=durable)  # 生命持久化,rabbit重启后,queue依然存在

    def send(self, queue='', message='', content_type='text/plain'):
        self.__set_channel(queue)
        self.__channel.basic_publish(exchange='',  # 交换机类型
                                     routing_key=queue,  # MQ name == routing_key
                                     body=message,
                                     properties=pika.BasicProperties(delivery_mode=2, content_type=content_type),  # message持久化,但不保证完全不丢失,存到硬盘也需要时间, modo 2 is durable
                                     )

    def receive(self, queue='', operate=None, **kwargs):
        if not operate:
            raise NotImplementedError

        # 回调函数
        def callback(ch, method, properties, body):
            operate(body, **kwargs)
            # 对message进行消费确认
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.__connection.process_data_events()
        # 为了实现负载均衡，可以在消费者端通知RabbitMQ，一个消息处理完之后才会接受下一个消息。
        # 可以使用prefetch_count=1的basic_qos方法可告知RabbitMQ只有在consumer处理并确认了上一个message后才分配新的message给他
        # 否则分给另一个空闲的consumer
        # fair dispatch
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(callback, queue=queue)
        self.__channel.start_consuming()

    def close(self):
        self.__connection.close()

rabbitmq = Manager()


if __name__ == '__main__':
    # TODO 线程池
    def operate(body):
        print body

    test = Manager()
    test.receive('queue', operate)