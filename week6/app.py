from flask import Flask, jsonify
from flasgger import Swagger

from auth import auth_bp
from security import security_bp

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Week6 Authentication API",
        "description": "JWT Authentication + Authorization Demo",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Bearer <JWT_TOKEN>"
        }
    }
}

Swagger(app, template=swagger_template)

app.register_blueprint(auth_bp)
app.register_blueprint(security_bp)


@app.route("/")
def home():
    return jsonify({
        "message": "Week6 JWT API",
        "docs": "/apidocs"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5009)