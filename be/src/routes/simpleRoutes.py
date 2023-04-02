from flask import Blueprint
from src.controllers.simpleControllers import SimpleControllers

simpleRouter = Blueprint("simpleRouter", __name__)

simpleRouter.route("/simple/<genre>", methods =['GET'])(SimpleControllers.getSimple)