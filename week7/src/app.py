from flask import Flask
from flasgger import Swagger
from src.routes.product_routes import product_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(product_bp)
    swagger = Swagger(app)
    return app