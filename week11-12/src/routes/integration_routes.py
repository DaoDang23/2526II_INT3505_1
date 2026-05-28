import uuid
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from database import DELIVERIES, WEBHOOKS

integration_bp = Blueprint(
    "integration_bp",
    __name__
)


@integration_bp.route(
    "/api/integrations/webhooks",
    methods=["POST"]
)
def create_webhook():

    data = request.get_json(silent=True) or {}

    url = data.get("url")
    events = data.get("events")
    secret = data.get("secret")

    if not url or not events or not secret:
        return jsonify({
            "error": "Missing fields"
        }), 400

    webhook = {
        "id": str(uuid.uuid4()),
        "url": url,
        "events": events,
        "secret": secret,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    WEBHOOKS.append(webhook)

    return jsonify(webhook), 201


@integration_bp.route(
    "/api/integrations/webhooks",
    methods=["GET"]
)
def list_webhooks():

    return jsonify({
        "count": len(WEBHOOKS),
        "data": WEBHOOKS
    })


@integration_bp.route(
    "/api/integrations/deliveries",
    methods=["GET"]
)
def list_deliveries():

    return jsonify({
        "count": len(DELIVERIES),
        "data": DELIVERIES
    })