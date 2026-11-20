from flask import Flask
from .backend import SimulatedBackend
from .config import Config
from .control import Kit


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.extensions["kit"] = Kit(SimulatedBackend(), app.config["V_MAX"])

    from . import api, telemetry
    app.register_blueprint(api.bp)
    app.register_blueprint(telemetry.bp)

    @app.get("/")
    def index():
        return "ECP 210 server is running. Dashboard coming soon."

    return app