from flask import Blueprint, jsonify, request

bp = Blueprint("telemetry", __name__)
_latest = {}


@bp.post("/telemetry")
def receive():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(ok=False, error="Expected a JSON object"), 400
    _latest.clear()
    _latest.update(data)
    return jsonify(ok=True)


@bp.get("/api/telemetry/latest")
def latest():
    return jsonify(_latest)