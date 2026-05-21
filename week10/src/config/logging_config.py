import json
import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "time": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "extra_data"):
            payload["extra"] = record.extra_data

        return json.dumps(payload)


def setup_logger(name, file_path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(file_path)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger


app_logger = setup_logger("app_logger", "logs/app.log")
audit_logger = setup_logger("audit_logger", "logs/audit.log")