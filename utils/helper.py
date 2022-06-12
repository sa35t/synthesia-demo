"""Helper functions in Flask app context
"""
from flask import current_app as app
import boto3


def send_msg(msg, success=True, data=""):
    """Funtion to formulate success or error messsage

    Args:
        msg (string): Message
        data (string, optional): Data. Defaults to "".
        status_code (int, optional): status code. Defaults to 200.
    """

    return (
        {
            "success": success,
            "data": data,
            "msg": msg,
        },
    )


def check_key_in_redis(key, value, expiry=None):
    """Check key in redis if it exists then return the value else set it

    Args:
        key (string): Key
        value (int): Value
        expity (integer): Expiry time in seconds
    """
    if app.config["_redis_conn"].exists_key(key=key):
        total_request = app.config["_redis_conn"].incr_key(key=key)
    else:
        app.config["_redis_conn"].set_key(key=key, value=value, expiry=expiry)
        total_request = value
    return total_request


def send_to_sqs(queue_name, msg):
    """Send JOB to SQS

    Args:
        queue_name (string): name of the queue
        msg (dict): Message dictionary

    Returns:
        bool: Return success or Failure
    """

    try:
        sqs = boto3.resource(
            "sqs",
            endpoint_url="http://localhost:9324",
            region_name="elasticmq",
            aws_secret_access_key="x",
            aws_access_key_id="x",
            use_ssl=False,
        )
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        response = queue.send_message(MessageBody=msg)
        return True
    except ValueError as error:
        return False
