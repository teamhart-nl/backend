from flask import render_template

from app import app
from definitions import PRODUCTION

if PRODUCTION:
    @app.route('/')
    def standard_route():
        return render_template("index.html")

    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_route(e):
        return render_template("index.html")