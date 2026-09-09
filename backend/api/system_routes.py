from flask import Blueprint, jsonify


system_api = Blueprint("system_api", __name__)


@system_api.route("/info")
def info():
    return jsonify({
        "application": "Industrial IoT Intelligence Platform",
        "version": "2.0",
        "architecture": "MQTT + InfluxDB + Flask",
        "status": "online"
    })
