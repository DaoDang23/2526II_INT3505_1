import time
from functools import wraps

FAILURE_COUNT = 0
LAST_FAILURE_TIME = 0

FAILURE_THRESHOLD = 5
RECOVERY_TIMEOUT = 30


def circuit_breaker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global FAILURE_COUNT
        global LAST_FAILURE_TIME

        current_time = time.time()

        if (
            FAILURE_COUNT >= FAILURE_THRESHOLD
            and current_time - LAST_FAILURE_TIME < RECOVERY_TIMEOUT
        ):
            return {
                "error": "Service temporarily unavailable"
            }, 503

        try:
            response = func(*args, **kwargs)

            FAILURE_COUNT = 0

            return response

        except Exception:
            FAILURE_COUNT += 1
            LAST_FAILURE_TIME = current_time

            return {
                "error": "Internal server error"
            }, 500

    return wrapper