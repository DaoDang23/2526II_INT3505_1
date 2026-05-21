import time
from collections import defaultdict

from flask import jsonify, request

REQUEST_HISTORY = defaultdict(list)

RATE_LIMIT = 60
WINDOW_SECONDS = 60


def rate_limit():
    ip = request.remote_addr
    current_time = time.time()

    REQUEST_HISTORY[ip] = [
        ts
        for ts in REQUEST_HISTORY[ip]
        if current_time - ts < WINDOW_SECONDS
    ]

    if len(REQUEST_HISTORY[ip]) >= RATE_LIMIT:
        return jsonify({
            "error": "Too many requests"
        }), 429

    REQUEST_HISTORY[ip].append(current_time)

    return None