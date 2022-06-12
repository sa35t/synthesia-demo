"""Create flask app instance and configuring app settings."""

import os

from flask import make_response, request
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.exceptions import HTTPException

from app import API_BP
from libs.redis import Redis
from utils.flask_extended import Flask

from celery import Celery


# Flask instance
APP = Flask(__name__, instance_relative_config=True)
# maintain the order of keys in dictionary
APP.config["JSON_SORT_KEYS"] = False
ENV = os.environ.get("FLASK_ENV", "dev")
APP.config["ENV"] = ENV

# loading config yaml according to environment, currently I have made config
# only for DEV environment
APP.config.from_yaml(os.path.join(APP.root_path, "config/" + ENV + ".yaml"))

# registering blueprint
APP.register_blueprint(API_BP, url_prefix="/crypto")
APP.wsgi_app = ProxyFix(APP.wsgi_app)

# APP level connection with REDIS
APP.config["_redis_conn"] = Redis(APP)

if __name__ == "__main__":
    APP.run(debug=False, port=5001)
