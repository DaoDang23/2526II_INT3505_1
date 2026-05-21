from flask import Flask

from routes.api_routes import api_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(api_bp)

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response

    return app