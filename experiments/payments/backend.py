"""Payment backends: mock (default) and Stripe (test/live) via REST.

The sandbox never moves real money unless the caller explicitly enables the
live backend with STRIPE_SECRET_KEY and --confirm-live. Test mode uses Stripe's
test payment method tokens and is safe.
"""
from __future__ import annotations

import json, os, urllib.parse, urllib.request
from dataclasses import dataclass


@dataclass
class ChargeResult:
    ok: bool
    charge_id: str
    amount: float
    currency: str
    mode: str
    error: str = ""


class MockBackend:
    """Deterministic, no network. Used for dry runs and unit tests."""
    def __init__(self):
        self.charges = []

    def charge(self, amount: float, currency: str, description: str, idempotency_key: str, merchant: str) -> ChargeResult:
        cid = f"mock_{len(self.charges)+1:04d}"
        self.charges.append({"id": cid, "amount": amount, "currency": currency, "merchant": merchant,
                             "description": description, "idempotency_key": idempotency_key})
        return ChargeResult(True, cid, amount, currency, "mock")


class StripeBackend:
    """Minimal Stripe PaymentIntent client using the REST API."""
    BASE = "https://api.stripe.com/v1"

    def __init__(self, secret_key: str, live: bool = False, confirm_live: bool = False,
                 payment_method: str = "pm_card_visa"):
        if not secret_key:
            raise ValueError("STRIPE_SECRET_KEY missing")
        if live and not confirm_live:
            raise PermissionError("live charges require explicit --confirm-live")
        self.key = secret_key
        self.live = live
        self.payment_method = payment_method

    def _post(self, path: str, data: dict, idempotency_key: str):
        body = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(self.BASE + path, data=body, method="POST")
        req.add_header("Authorization", "Bearer " + self.key)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("Idempotency-Key", idempotency_key)
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())

    def charge(self, amount: float, currency: str, description: str, idempotency_key: str, merchant: str) -> ChargeResult:
        # amount in minor units
        data = {
            "amount": str(int(round(amount * 100))),
            "currency": currency.lower(),
            "description": description,
            "metadata[merchant]": merchant,
            "capture_method": "automatic",
            "confirm": "true",
            "payment_method": self.payment_method,
        }
        try:
            res = self._post("/payment_intents", data, idempotency_key)
        except Exception as exc:
            return ChargeResult(False, "", amount, currency, "live" if self.live else "test", str(exc))
        ok = res.get("status") in ("succeeded", "requires_capture")
        return ChargeResult(ok, res.get("id", ""), amount, currency, "live" if self.live else "test",
                            "" if ok else str(res.get("last_payment_error") or res.get("status")))
