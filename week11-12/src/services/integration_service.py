import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

import requests

from database import DELIVERIES, WEBHOOKS

TIMEOUT_SECONDS = int(
    os.getenv("WEBHOOK_TIMEOUT_SECONDS", "3")
)


class IntegrationService:

    def send_event(self, event):

        event_name = event["type"]

        matched_hooks = [
            hook for hook in WEBHOOKS
            if event_name in hook["events"]
        ]

        for hook in matched_hooks:
            self.deliver(hook, event)

    def build_signature(self, secret, payload):

        raw = json.dumps(
            payload,
            sort_keys=True
        ).encode()

        return hmac.new(
            secret.encode(),
            raw,
            hashlib.sha256
        ).hexdigest()

    def deliver(self, hook, event):

        signature = self.build_signature(
            hook["secret"],
            event
        )

        headers = {
            "Content-Type": "application/json",
            "X-Event-Type": event["type"],
            "X-Webhook-Signature": signature
        }

        delivery = {
            "webhook_id": hook["id"],
            "target_url": hook["url"],
            "event": event["type"],
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        try:

            response = requests.post(
                hook["url"],
                json=event,
                headers=headers,
                timeout=TIMEOUT_SECONDS
            )

            delivery["status"] = "success"
            delivery["http_status"] = response.status_code

        except Exception as exc:

            delivery["status"] = "failed"
            delivery["error"] = str(exc)

        DELIVERIES.append(delivery)