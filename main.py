# from rabbitmq import RabbitMQ
#
# rabbit = RabbitMQ()
# rabbit.start_task_receiving()
import constant
from infrastructure.mqtt import MQTT

broker = MQTT()
broker.subscribe(constant.MQTT_TOPIC_TASK)
# broker.subscribe('#')

