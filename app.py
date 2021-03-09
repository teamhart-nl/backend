import os

from flask import Flask
from flask_cors import CORS

from definitions import PRODUCTION, RESOURCES
from src.handlers.Dispatcher import Dispatcher
from src.helpers.LoadPhonemeJsonHelper import get_phoneme_patterns
from src.helpers.Logger import Logger
from src.modules.ArduinoConnection import ArduinoConnection

app = Flask(__name__)
CORS(app)

dispatcher = None
phoneme_patterns = None


if os.environ.get("WERKZEUG_RUN_MAIN") or PRODUCTION:
    # Runtime configuration

    dispatcher = Dispatcher()

    # config singleton ArduinoConnection
    ArduinoConnection().connect_with_config(os.path.join(RESOURCES, 'arduino_config.json'))

    phoneme_patterns = get_phoneme_patterns(RESOURCES)


if __name__ == "__main__" and PRODUCTION:
    app.run(debug=False, use_reloader=False, threaded=True)


import src.routes.ProductionRoute
import src.routes.Routes
Logger.log_info("Routes initialized")
