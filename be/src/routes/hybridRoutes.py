from flask import Blueprint
from src.controllers.hybridControllers import HybridControllers

hybridRouter = Blueprint("hybridRouter", __name__)

hybridRouter.route("/hybrid/<title>", methods =['GET'])(HybridControllers.getHybrid)