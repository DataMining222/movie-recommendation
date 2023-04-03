from flask import Blueprint
from src.controllers.contentControllers import ContentControllers

contentRouter = Blueprint("contentRouter", __name__)

contentRouter.route("/content/<title>", methods =['GET'])(ContentControllers.getContent)