from flask import Flask
from flasgger import Swagger

from routes import library_bp

app = Flask(__name__)

app.register_blueprint(library_bp)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

Swagger(app, config=swagger_config)

if __name__ == "__main__":
    app.run(debug=True, port=5008)