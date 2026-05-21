from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from books import books_bp

app = Flask(__name__)

app.register_blueprint(books_bp)

SWAGGER_URL = '/docs'
API_URL = '/openapi.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Book Management API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/openapi.yaml')
def openapi():
    with open('openapi.yaml', 'r', encoding='utf-8') as f:
        return f.read(), 200, {
            'Content-Type': 'text/yaml'
        }

@app.route('/')
def home():
    return {
        "message": "Book API is running",
        "swagger": "http://localhost:5000/docs"
    }

if __name__ == '__main__':
    app.run(debug=True)