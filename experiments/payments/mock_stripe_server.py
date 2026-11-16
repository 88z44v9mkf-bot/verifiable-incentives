"""A tiny Stripe-compatible mock for integration tests.

It implements POST /v1/payment_intents and GET /v1/payment_intents/{id},
accepts any Bearer sk_test_* key, honours Idempotency-Key, and returns a
succeeded PaymentIntent. It moves no money and talks to no network.
"""
from __future__ import annotations
import json, sys, threading, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

STATE = {"intents": {}, "by_idem": {}, "counter": 0}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/v1/payment_intents":
            return self._send(404, {"error": {"message": "not found"}})
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer sk_test_"):
            return self._send(401, {"error": {"message": "mock requires a test key"}})
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode()
        data = {k: v[0] for k, v in urllib.parse.parse_qs(raw).items()}
        idem = self.headers.get("Idempotency-Key", "")
        if idem and idem in STATE["by_idem"]:
            return self._send(200, STATE["by_idem"][idem])
        STATE["counter"] += 1
        pid = f"pi_mock_{STATE['counter']:06d}"
        obj = {"id": pid, "object": "payment_intent", "status": "succeeded",
               "amount": int(data.get("amount", "0")), "currency": data.get("currency", "usd"),
               "description": data.get("description", ""), "metadata": {"mock": "true"}}
        STATE["intents"][pid] = obj
        if idem:
            STATE["by_idem"][idem] = obj
        self._send(200, obj)

    def do_GET(self):
        if self.path.startswith("/v1/payment_intents/"):
            pid = self.path.rsplit("/", 1)[-1]
            obj = STATE["intents"].get(pid)
            return self._send(200 if obj else 404, obj or {"error": {"message": "not found"}})
        self._send(404, {"error": {"message": "not found"}})


def serve(port=12111):
    srv = HTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12111
    print(f"mock stripe listening on 127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
