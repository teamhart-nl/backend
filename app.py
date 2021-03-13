import os

from flask import Flask, render_template
from flask_cors import CORS

from definitions import PRODUCTION, RESOURCES
from src.handlers.Dispatcher import Dispatcher
from src.helpers.Logger import Logger
from src.modules.ArduinoConnection import ArduinoConnection
from src.modules.google_api.GoogleApiWrapper import GoogleApiWrapper

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)

dispatcher = None


if os.environ.get("WERKZEUG_RUN_MAIN") or __name__ == "__main__":

    # Initialize dispatcher
    dispatcher = Dispatcher()

    # config singleton ArduinoConnection
    ArduinoConnection().connect_with_config(os.path.join(RESOURCES, 'arduino_config.json'))

    # Check if google api is working correctly
    GoogleApiWrapper()

    # Import routes
    import src.routes.Routes
    Logger.log_info("Routes initialized")


if PRODUCTION:
    @app.route('/', methods=['GET'])
    def standard_route():
        return render_template("index.html")


    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_route(e):
        return render_template("index.html")


if __name__ == "__main__" and PRODUCTION:
    app.run(debug=False, use_reloader=False, threaded=True)
