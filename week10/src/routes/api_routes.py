from flask import Blueprint, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest

from middleware.circuit_breaker import circuit_breaker
from middleware.rate_limiter import rate_limit
from config.logging_config import app_logger, audit_logger

api_bp = Blueprint("api", __name__)

USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency"
)


@api_bp.before_request
def before_request():
    limit_response = rate_limit()

    if limit_response:
        return limit_response

    REQUEST_COUNT.inc()


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


@api_bp.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain"
    }


@api_bp.route("/api/users", methods=["GET"])
def get_users():
    app_logger.info(
        "Get users",
        extra={
            "extra_data": {
                "endpoint": "/api/users",
                "method": "GET"
            }
        }
    )

    return jsonify(USERS)


@api_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for user in USERS:
        if user["id"] == user_id:
            return jsonify(user)

    return jsonify({
        "error": "User not found"
    }), 404


@api_bp.route("/api/users", methods=["POST"])
@circuit_breaker
def create_user():
    data = request.get_json()

    if not data or "name" not in data:
        raise Exception("Invalid payload")

    new_user = {
        "id": len(USERS) + 1,
        "name": data["name"]
    }

    USERS.append(new_user)

    audit_logger.info(
        "Create user",
        extra={
            "extra_data": {
                "action": "CREATE_USER",
                "user": data["name"]
            }
        }
    )

    return jsonify(new_user), 201