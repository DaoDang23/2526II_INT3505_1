from flask import Flask, jsonify
from v1 import v1_bp
from v2 import v2_bp

app = Flask(__name__)

app.register_blueprint(v1_bp)
app.register_blueprint(v2_bp)

@app.route('/')
def home():
    return jsonify({
        "message": "Payment API Versioning Demo",
        "available_versions": ["v1", "v2"],
        "deprecated_versions": ["v1"],
        "active_version": "v2"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "UP"
    })

if __name__ == '__main__':
    app.run(debug=True)