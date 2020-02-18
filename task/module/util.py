import logging
import requests
import constant
import json
from datetime import datetime

from model.message import UpdateJobMessage
from task.module.validation import checkValidExecuteAt


def send_request(message):
    update_job_message = UpdateJobMessage()
    update_job_message.id = message['id']

    if checkValidExecuteAt(message['execute_at']):
        api_endpoint = message['server_ip'] + "/schedule.json"
        data = {
            "project": message['project'],
            "spider": message['spider'],
            "max_pagination_article_depth": constant.MAX_PAGINATION_ARTICLE_DEPTH,
            "max_pagination_comment_depth": constant.MAX_PAGINATION_COMMENT_DEPTH,
            "max_pagination_reply_depth": constant.MAX_PAGINATION_REPLY_DEPTH,
            "user_email": message['username'],
            "password": message['password'],
            "fan_page_urls": message['followings'],
            "user_agent": constant.USER_AGENT
        }
        r = requests.post(url=api_endpoint, data=data)
        # print(r.text)
        job = json.loads(str(r.text))

        update_job_message.real_execute_at = str(datetime.now().strftime(constant.FORMAT_DATETIME))
        update_job_message.status = constant.JOB_STATUS_STARTED_SUCCESSFULLY
        print("The paste bin URL is:%s" % job["jobid"])
    else:
        update_job_message.error_code = constant.JOB_ERROR_CODE_EXCEED_VALID_EXECUTED_AT
        update_job_message.status = constant.JOB_STATUS_STARTED_FAILED
        logging.error("Message exceed valid time: " + message['execute_at'])

    return update_job_message
    # rabbitmq.send_message(constant.RABBITMQ_MONITOR_QUEUE, monitor_message)
    # broker.send_message(constant.MQTT_TOPIC_JOB_UPDATE, monitor_message)
