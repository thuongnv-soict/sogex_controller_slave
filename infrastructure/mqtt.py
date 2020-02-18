import json
import logging
import os
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

import constant
from task.module.util import send_request


class MQTT:
    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        load_dotenv()

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))

        def on_message(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))

        def on_message_task(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))
            message = json.loads(msg.payload)
            print(message['execute_at'])
            update_job_message = send_request(message)
            self.send_message(constant.MQTT_TOPIC_JOB_UPDATE, update_job_message)

        def on_message_test(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))

        def on_publish(client, obj, mid):
            print("mid: " + str(mid))

        def on_subscribe(client, obj, mid, granted_qos):
            print("Subscribed: " + str(mid) + " " + str(granted_qos))

        def on_log(client, obj, level, string):
            print(string)

        self.client = mqtt.Client()

        self.client.on_connect = on_connect
        # self.client.on_message = on_message
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe
        self.client.on_log = on_log

        self.client.message_callback_add('task', on_message_task)
        self.client.message_callback_add('test', on_message_test)

        try:
            rc = self.client.connect(host=os.getenv('MQTT_HOST'), port=int(os.getenv('MQTT_PORT')))
            print(rc)
        except Exception as ex:
            print(ex)
            time.sleep(5)
            logging.info("Reconnect to MQTT Server ...")
            rc = self.connect()
        return rc

    def send_message(self, topic, content):
        try:
            message_json = content.to_json()
            self.client.publish(topic, message_json)
        except Exception as exc:
            print(exc)
            rc = self.connect()
            while rc == 0:
                print('Reconnect to MQTT Server ...')
                rc = self.connect()
                if rc == 1:
                    break
                time.sleep(5)

            self.send_message(topic, content)

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.loop_forever()
