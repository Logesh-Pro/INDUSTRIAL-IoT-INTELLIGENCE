from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.config.settings import settings
from backend.api.routes import api
from backend.api.errors import register_error_handlers
from backend.api.health_routes import register_database_health_route

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path="/static"
)

CORS(app)

app.register_blueprint(api, url_prefix="/api")
register_database_health_route(app)
register_error_handlers(app)


@app.route("/")
def dashboard():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def frontend_files(path):
    requested = FRONTEND_DIR / path

    if requested.is_file():
        return send_from_directory(FRONTEND_DIR, path)

    return send_from_directory(FRONTEND_DIR, "index.html")


if __name__ == "__main__":
    app.run(
        host=settings.API_HOST,
        port=settings.API_PORT,
        debug=False,
        use_reloader=False
    )
