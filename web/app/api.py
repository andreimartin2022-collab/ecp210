from flask import Blueprint, current_app, jsonify, request
from .control import KitError

bp = Blueprint("api", __name__, url_prefix="/api")


def kit():
    return current_app.extensions["kit"]


@bp.get("/status")
def status():
    return jsonify(kit().status())


@bp.post("/power/on")
def power_on():
    kit().power_on()
    return jsonify(ok=True)


@bp.post("/power/off")
def power_off():
    kit().power_off()
    return jsonify(ok=True)


@bp.post("/input")
def send_input():
    data = request.get_json(silent=True) or {}
    try:
        volts = float(data["volts"])
    except (KeyError, TypeError, ValueError):
        return jsonify(ok=False, error="volts must be a number"), 400
    try:
        kit().set_input(volts)
    except KitError as e:
        return jsonify(ok=False, error=str(e)), 409
    return jsonify(ok=True)


@bp.post("/estop")
def estop():
    kit().emergency_stop()
    return jsonify(ok=True)


@bp.post("/reset")
def reset():
    kit().reset()
    return jsonify(ok=True)