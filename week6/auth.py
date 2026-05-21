import os
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, request, g
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "week6-secret-key"

users = {
    "admin": {
        "password": generate_password_hash("123456"),
        "role": "admin"
    },
    "user": {
        "password": generate_password_hash("123456"),
        "role": "user"
    }
}

blacklist = []


def create_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def token_required(f):
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]

            if token in blacklist:
                return jsonify({"error": "Token revoked"}), 401

            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            g.user = data

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


def admin_required(f):
    @token_required
    def wrapper(*args, **kwargs):

        if g.user["role"] != "admin":
            return jsonify({"error": "Admin only"}), 403

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register account
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Register success
    """

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"error": "User already exists"}), 409

    users[username] = {
        "password": generate_password_hash(password),
        "role": "user"
    }

    return jsonify({"message": "Register success"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login and get JWT token
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login success
    """

    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = users.get(username)

    if not user:
        return jsonify({"error": "Invalid username"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Wrong password"}), 401

    access_token = create_token(username, user["role"])

    refresh_token = create_token(username, user["role"])

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "role": user["role"]
    })


@auth_bp.route("/profile")
@token_required
def profile():
    """
    Current user profile
    ---
    tags:
      - Authentication
    security:
      - BearerAuth: []
    responses:
      200:
        description: User profile
    """

    return jsonify({
        "username": g.user["username"],
        "role": g.user["role"]
    })


@auth_bp.route("/admin")
@admin_required
def admin_panel():
    """
    Admin protected route
    ---
    tags:
      - Authorization
    security:
      - BearerAuth: []
    responses:
      200:
        description: Admin content
    """

    return jsonify({
        "message": "Welcome admin"
    })


@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    """
    Logout and revoke token
    ---
    tags:
      - Authentication
    security:
      - BearerAuth: []
    responses:
      200:
        description: Logout success
    """

    token = request.headers.get("Authorization").split(" ")[1]

    blacklist.append(token)

    return jsonify({
        "message": "Token revoked"
    })