import os
from flask import Flask
import src.routes.simpleRoutes as simpleRoutes
# import src.routes.contentRoutes as contentRoutes
# import src.routes.cfRoutes as cfRoutes
# import src.routes.hybridRoutes as hybridRoutes

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'will.change.later'
app.register_blueprint(simpleRoutes.simpleRouter, url_prefix = "/api")
# app.register_blueprint(contentRoutes.contentRouter, url_prefix = "/api")
# app.register_blueprint(cfRoutes.cfRouter, url_prefix = "/api")
# app.register_blueprint(hybridRoutes.hybridRouter, url_prefix = "/api")

# @app.route("/")
# def deploy():
#     return "Successfully deployed"


if __name__ == '_main_':
    app.run(threaded=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))