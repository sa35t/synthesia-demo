"""Worker helper functions 
"""
import redis
import requests
import boto3
from json import dumps

config = {
    "SYNTHESIA_DEMO": "v0.0.1",
    "REDIS": {"host": "127.0.0.1", "port": "6379", "db": "0"},
    "UNRELIABLE_URL": {
        "URL": "https://hiring.api.synthesia.io/crypto/sign",
        "time_out": 1,
        "auth": "1a1c4a0edaa7b8cbc82eb52a6baf4c8d",
        "RATE_LIMITING": {
            "request_per_minute": 10,
            "redis_key": "unreliable_url",
        },
    },
    "SQS": {"queue_name": "process"},
}


def get_redis_connection():
    return redis.Redis(
        host=config["REDIS"]["host"],
        port=config["REDIS"]["port"],
        db=config["REDIS"]["db"],
    )


def set_key(key, value, expiry=None):
    """Set key in redis

    Args:
        key (string): Key
        value (string): Value
        expiry (seconds, optional): Key expiry time. Defaults to None.

    Returns:
        bool: Status if key set or not
    """
    conn = get_redis_connection()
    if expiry:
        response = conn.setex(key, expiry, value)
    else:
        response = conn.set(key, value)
    return response


def incr_key(key):
    """
    Increment key in redis by 1

    Args:
        key (string): Key to increment

    Returns:
        integer: Value corresponding to the Key
    """
    conn = get_redis_connection()
    return conn.incr(key)


def exists_key(key):
    """
    Increment key in redis by 1

    Args:
        key (string): Key to increment

    Returns:
        integer: Value corresponding to the Key
    """
    conn = get_redis_connection()
    return conn.exists(key)


def check_key_in_redis(key, value, expiry=None):
    """Check key in redis if it exists then return the value else set it

    Args:
        key (string): Key
        value (int): Value
        expity (integer): Expiry time in seconds
    """
    if exists_key(key=key):
        total_request = incr_key(key=key)
    else:
        set_key(key=key, value=value, expiry=expiry)
        total_request = value
    return total_request


def get_message_digest(message, email):

    key = config["UNRELIABLE_URL"]["RATE_LIMITING"]["redis_key"]
    allowed_request_per_minute = config["UNRELIABLE_URL"]["RATE_LIMITING"][
        "request_per_minute"
    ]

    # check for key if it is exists then return the counter
    # else set the key with value and expiry given
    current_request_count = check_key_in_redis(key, value=1, expiry=60)

    # if we have exhausted the quota of request, then queue the request
    if int(current_request_count) <= allowed_request_per_minute:
        # request the unreliable URL
        try:
            URL = config["UNRELIABLE_URL"]["URL"]
            timeout = config["UNRELIABLE_URL"]["time_out"]
            params = {"message": message}
            header = {"Authorization": config["UNRELIABLE_URL"]["auth"]}
            response = requests.get(
                URL, timeout=timeout, headers=header, params=params
            )
            if response.status_code == 200:
                # here we can again queue this for email in separate queue
                return response.text
        except TimeoutError as error:
            pass
        except Exception as error:
            pass

    # if fail then again queued it for processing
    msg = {"message": message, "email": email}
    print("requeuing")
    send_to_sqs(queue_name="process", msg=dumps(msg))


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
