from flask import Blueprint, jsonify

security_bp = Blueprint("security", __name__)


@security_bp.route("/security/audit")
def audit():
    """
    Security audit report
    ---
    tags:
      - Security
    responses:
      200:
        description: Security audit
    """

    risks = [
        {
            "risk": "Token Leakage",
            "description": "JWT token exposed in logs or frontend storage",
            "solution": "Use HTTPS and HttpOnly cookies"
        },
        {
            "risk": "Replay Attack",
            "description": "Attacker reuses stolen token",
            "solution": "Short token expiration and refresh token rotation"
        },
        {
            "risk": "Weak Secret Key",
            "description": "Easy to brute force JWT secret",
            "solution": "Use strong environment secret"
        }
    ]

    return jsonify({
        "security_audit": risks
    })