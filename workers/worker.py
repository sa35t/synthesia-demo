"""Worker for processing all queued requests 
"""

from distutils.command.config import config
from json import loads
import boto3
import worker_helper

sqs = boto3.resource(
    "sqs",
    endpoint_url="http://localhost:9324",
    region_name="elasticmq",
    aws_secret_access_key="x",
    aws_access_key_id="x",
    use_ssl=False,
)
queue = sqs.get_queue_by_name(
    QueueName=worker_helper.config["SQS"]["queue_name"]
)

while 1:
    messages = queue.receive_messages(MaxNumberOfMessages=1)
    for message in messages:
        body = loads(message.body)
        print(f"body {body}")
        result = worker_helper.get_message_digest(
            message=body["message"], email=body["email"]
        )
        if result:
            print(result)
        message.delete()
