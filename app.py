"""Define routes for different modules. """

from flask import Blueprint
from flask_restplus import Api

from modules.sign.controller import Controller as Sign

API_BP = Blueprint("api", __name__)
API = Api(
    API_BP,
    title="Snapchat Marketing API",
    version="0.0.1",
    description="API to manage Snapchat marketing platform",
)

API.add_resource(Sign, "/sign", endpoint="get signed hash", methods=["GET"])
