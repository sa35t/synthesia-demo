"""Manage snap account and configuration which will be global on account level."""

from json import dumps
from flask import current_app as app
from flask import g, request
from flask_restplus import Resource

from custom_decorators.auth import authenticate
import requests
from utils import helper


class Controller(Resource):
    """Manage CRUD operation for accounts."""

    @authenticate
    def get(self):
        """Fetch account information based on user's resource access level and permissions."""

        message = request.args.get("message", None)
        if message is None or not message:
            return (
                helper.send_msg("param <message> is required.", success=False),
                200,
            )

        key = app.config["UNRELIABLE_URL"]["RATE_LIMITING"]["redis_key"]
        allowed_request_per_minute = app.config["UNRELIABLE_URL"][
            "RATE_LIMITING"
        ]["request_per_minute"]

        # check for key if it is exists then return the counter
        # else set the key with value and expiry given
        current_request_count = helper.check_key_in_redis(
            key, value=1, expiry=60
        )

        # if we have exhausted the quota of request, then queue the request
        if int(current_request_count) <= allowed_request_per_minute:
            # request the unreliable URL
            try:
                URL = app.config["UNRELIABLE_URL"]["URL"]
                timeout = app.config["UNRELIABLE_URL"]["time_out"]
                params = {"message": message}
                header = {
                    "Authorization": app.config["UNRELIABLE_URL"]["auth"]
                }
                response = requests.get(
                    URL, timeout=timeout, headers=header, params=params
                )
                if response.status_code == 200:
                    return (
                        helper.send_msg(
                            msg="Messaged signed successfully",
                            data=response.text,
                        ),
                        200,
                    )
            except TimeoutError as error:
                pass
            except Exception as error:
                pass

        # if we reach here, that means request has failed due to following 3 reasons:
        # 1. if no._of_request are greater than 10 in a minute
        # 2. if an unreliable API give 500
        # 3. If an unreliable API taking more than 1 second to respond
        # queue the message and send response to the user
        # instead of email id it can be any thing like user id for notification on web
        # phone no. for notification on Mobile

        queue_name = app.config["SQS"]["queue_name"]
        msg = {"message": message, "email": "acdcdcbc@gmail.com"}
        helper.send_to_sqs(queue_name=queue_name, msg=dumps(msg))

        return (
            helper.send_msg(
                msg="Sit back and relax, You will get an email when your signed message is ready",
            ),
            200,
        )
