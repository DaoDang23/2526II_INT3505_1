from datetime import datetime, timezone
from functools import wraps
import hashlib
import json

from flask import Flask, jsonify, make_response, request
from flasgger import Swagger

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Week2 Unified API",
        "description": "Unified API for RPC + REST/Auth/Cache demos",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Format: Bearer <token>",
        }
    },
}

Swagger(app, template=swagger_template)

# ── Data store ────────────────────────────────────────────────────────────────

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob",   "email": "bob@example.com"},
    {"id": 3, "name": "Carol", "email": "carol@example.com"},
]

VALID_TOKENS = {
    "secret-token-alice": 1,
    "secret-token-bob":   2,
}

# ── Hooks ─────────────────────────────────────────────────────────────────────

@app.before_request
def log_request():
    app.logger.info(f"→ {request.method} {request.path}")


@app.after_request
def log_response(response):
    app.logger.info(f"← {response.status_code}")
    return response

# ── Helpers ───────────────────────────────────────────────────────────────────

def require_auth(func):
    """Decorator: reject requests that lack a valid Bearer token."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing Authorization"}), 401
        token = auth_header.removeprefix("Bearer ")
        if token not in VALID_TOKENS:
            return jsonify({"error": "Invalid token"}), 401
        return func(*args, **kwargs)
    return wrapper


def compute_etag(data: object) -> str:
    serialised = json.dumps(data, sort_keys=True).encode()
    return hashlib.md5(serialised).hexdigest()


def cached_response(data, max_age: int = 30):
    """Return 304 when ETag matches, otherwise 200 with caching headers."""
    etag = compute_etag(data)
    if request.headers.get("If-None-Match") == etag:
        res = make_response("", 304)
        res.headers["ETag"] = etag
        return res

    res = make_response(jsonify(data), 200)
    res.headers["ETag"] = etag
    res.headers["Cache-Control"] = f"public, max-age={max_age}"
    res.headers["Last-Modified"] = datetime.now(timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    return res


def find_user(uid: int):
    matches = [u for u in users if u["id"] == uid]
    return matches[0] if matches else None


def next_id() -> int:
    ids = [u["id"] for u in users]
    return (max(ids) if ids else 0) + 1

# ── RPC endpoint ──────────────────────────────────────────────────────────────

RPC_ACTIONS = {}

def rpc_action(name):
    """Register a function as an RPC action handler."""
    def decorator(func):
        RPC_ACTIONS[name] = func
        return func
    return decorator


@rpc_action("get_users")
def _rpc_get_users(data):
    return jsonify(users), 200


@rpc_action("get_user")
def _rpc_get_user(data):
    user = find_user(data.get("id"))
    return (jsonify(user), 200) if user else (jsonify({"msg": "not found"}), 200)


@rpc_action("create_user")
def _rpc_create_user(data):
    if "name" not in data or "email" not in data:
        return jsonify({"msg": "missing name or email"}), 400
    new_user = {"id": next_id(), "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify({"msg": "ok", "user": new_user}), 201


@rpc_action("update_email")
def _rpc_update_email(data):
    if "email" not in data:
        return jsonify({"msg": "missing email"}), 400
    user = find_user(data.get("id"))
    if not user:
        return jsonify({"msg": "not found"}), 200
    user["email"] = data["email"]
    return jsonify({"msg": "ok"}), 200


@rpc_action("delete_user")
def _rpc_delete_user(data):
    user = find_user(data.get("id"))
    if not user:
        return jsonify({"msg": "not found"}), 200
    users.remove(user)
    return jsonify({"msg": "deleted"}), 200


@app.route("/action", methods=["POST"])
def action():
    """
    Legacy RPC endpoint
    ---
    tags:
        - RPC
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          schema:
              type: object
              required:
                  - action
              properties:
                  action:
                      type: string
                      example: get_users
                  id:
                      type: integer
                      example: 1
                  name:
                      type: string
                      example: Dave
                  email:
                      type: string
                      example: dave@example.com
    responses:
        200:
            description: Action processed
        201:
            description: User created
        400:
            description: Invalid payload/action
    """
    data = request.get_json(silent=True) or {}
    act = data.get("action")
    handler = RPC_ACTIONS.get(act)
    if handler:
        return handler(data)
    return jsonify({"msg": "unknown action"}), 400

# ── REST endpoints ────────────────────────────────────────────────────────────

@app.route("/users", methods=["GET"])
@require_auth
def get_users():
    """
    Get all users (cached with ETag)
    ---
    tags:
        - Users
    security:
        - BearerAuth: []
    parameters:
        - in: header
          name: If-None-Match
          type: string
          required: false
          description: Previous ETag for conditional GET
    responses:
        200:
            description: User list
        304:
            description: Not modified
        401:
            description: Unauthorized
    """
    return cached_response(users, max_age=30)


@app.route("/users/<int:uid>", methods=["GET"])
@require_auth
def get_user(uid):
    """
    Get one user by ID (cached with ETag)
    ---
    tags:
        - Users
    security:
        - BearerAuth: []
    parameters:
        - in: path
          name: uid
          type: integer
          required: true
        - in: header
          name: If-None-Match
          type: string
          required: false
    responses:
        200:
            description: User detail
        304:
            description: Not modified
        401:
            description: Unauthorized
        404:
            description: User not found
    """
    user = find_user(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return cached_response(user, max_age=60)


@app.route("/users", methods=["POST"])
@require_auth
def create_user():
    """
    Create a new user
    ---
    tags:
        - Users
    security:
        - BearerAuth: []
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          schema:
              type: object
              required:
                  - name
                  - email
              properties:
                  name:
                      type: string
                      example: Eve
                  email:
                      type: string
                      example: eve@example.com
    responses:
        201:
            description: User created
        400:
            description: Missing fields
        401:
            description: Unauthorized
    """
    data = request.get_json(silent=True) or {}
    missing = [f for f in ("name", "email") if f not in data]
    if missing:
        return jsonify({"error": "Missing name or email"}), 400

    new_user = {"id": next_id(), "name": data["name"], "email": data["email"]}
    users.append(new_user)

    res = make_response(jsonify(new_user), 201)
    res.headers["Location"] = f"/users/{new_user['id']}"
    res.headers["Cache-Control"] = "no-store"
    return res


@app.route("/users/<int:uid>", methods=["PUT"])
@require_auth
def update_user(uid):
    """
    Update user fields
    ---
    tags:
        - Users
    security:
        - BearerAuth: []
    consumes:
        - application/json
    parameters:
        - in: path
          name: uid
          type: integer
          required: true
        - in: body
          name: body
          required: true
          schema:
              type: object
              properties:
                  name:
                      type: string
                  email:
                      type: string
    responses:
        200:
            description: User updated
        400:
            description: No data
        401:
            description: Unauthorized
        404:
            description: User not found
    """
    user = find_user(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"error": "No data"}), 400

    allowed_fields = {"name", "email"}
    for field, value in data.items():
        if field in allowed_fields:
            user[field] = value

    res = make_response(jsonify(user), 200)
    res.headers["Cache-Control"] = "no-store"
    return res


@app.route("/users/<int:uid>", methods=["DELETE"])
@require_auth
def delete_user(uid):
    """
    Delete user by ID
    ---
    tags:
        - Users
    security:
        - BearerAuth: []
    parameters:
        - in: path
          name: uid
          type: integer
          required: true
    responses:
        204:
            description: User deleted
        401:
            description: Unauthorized
        404:
            description: User not found
    """
    user = find_user(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)
    res = make_response("", 204)
    res.headers["Cache-Control"] = "no-store"
    return res

# ── Error handlers ────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    print("Unified Server running on http://localhost:5005")
    app.run(port=5005, debug=True)
