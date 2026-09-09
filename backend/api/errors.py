import logging

from flask import jsonify


logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": "error",
            "code": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "Endpoint not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.exception("Internal server error")

        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Internal server error"
        }), 500
