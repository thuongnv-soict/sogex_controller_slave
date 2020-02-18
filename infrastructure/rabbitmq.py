import json
import os

from dotenv import load_dotenv
import constant
import pika
from pika import exceptions


class RabbitMQ:
    def __init__(self):
        self.channel = None
        self.connection = None
        self.properties = pika.BasicProperties(delivery_mode=constant.RABBITMQ_DELIVERY_MODE)
        self.connect()

    def connect(self):
        load_dotenv()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), port=os.getenv('RABBITMQ_PORT')))
        self.channel = self.connection.channel()
        print("Connected to RabbitMQ Server")

        self.channel.exchange_declare(exchange=constant.RABBITMQ_EXCHANGE_NAME,
                                      exchange_type=constant.RABBITMQ_EXCHANGE_TYPE)

        # # Declare 'task_queue'
        # self.channel.queue_declare(queue=constant.RABBITMQ_TASK_QUEUE, durable=constant.RABBITMQ_QUEUE_DURABLE)
        # self.channel.queue_bind(exchange=constant.RABBITMQ_EXCHANGE_NAME,
        #                         queue=constant.RABBITMQ_TASK_QUEUE,
        #                         routing_key=constant.RABBITMQ_TASK_QUEUE)

        # Declare 'monitor_queue'
        self.channel.queue_declare(queue=constant.RABBITMQ_MONITOR_QUEUE, durable=constant.RABBITMQ_QUEUE_DURABLE)
        self.channel.queue_bind(exchange=constant.RABBITMQ_EXCHANGE_NAME,
                                queue=constant.RABBITMQ_MONITOR_QUEUE,
                                routing_key=constant.RABBITMQ_MONITOR_QUEUE)

    def send_message(self, routing_key, data):
        message = data.to_json()
        try:
            self.channel.basic_publish(
                exchange=constant.RABBITMQ_EXCHANGE_NAME,
                routing_key=routing_key,
                body=message,
                # properties=self.properties
            )
        except Exception as exc:
            print(exc)
            print('Reconnect to RabbitMQ')
            self.connect()
            self.send_message(routing_key, data)
            print("Send message successfully")
