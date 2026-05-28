from flask import Blueprint, jsonify

from database import EVENTS

activity_bp = Blueprint(
    "activity_bp",
    __name__
)


@activity_bp.route("/api/events", methods=["GET"])
def list_events():

    return jsonify({
        "count": len(EVENTS),
        "data": EVENTS
    })