"""Live/test-mode driver for the real-money sandbox.

This file never runs automatically. `--live` additionally requires
`--confirm-live`, a Stripe secret key, and a spend cap. Test mode uses Stripe's
test payment method and moves no real money.
"""
from __future__ import annotations
import argparse, os, sys, threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "commerce"))

import agent_loop
from backend import StripeBackend, MockBackend


class CappedBackend:
    def __init__(self, inner, max_spend: float):
        self.inner = inner
        self.max_spend = float(max_spend)
        self.spent = 0.0
        self._lock = threading.Lock()

    def charge(self, amount, currency, description, idempotency_key, merchant):
        with self._lock:
            if self.spent + amount > self.max_spend + 1e-9:
                raise RuntimeError(f"spend cap reached: {self.spent:.2f} + {amount:.2f} > {self.max_spend:.2f}")
        res = self.inner.charge(amount, currency, description, idempotency_key, merchant)
        if res.ok:
            with self._lock:
                self.spent += amount
        return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/payments_live.jsonl")
    ap.add_argument("--tasks", type=int, default=10)
    ap.add_argument("--test-mode", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--confirm-live", action="store_true")
    ap.add_argument("--max-spend", type=float, default=200.0)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--payment-method", default="pm_card_visa")
    args = ap.parse_args(argv)
    if not args.test_mode and not args.live:
        print("refusing to run without --test-mode or --live", file=sys.stderr)
        return 2
    key = os.environ.get("STRIPE_SECRET_KEY", "")
    if not key:
        print("STRIPE_SECRET_KEY missing", file=sys.stderr)
        return 2
    inner = StripeBackend(key, live=args.live, confirm_live=args.confirm_live,
                          payment_method=args.payment_method)
    agent_loop.BACKEND = CappedBackend(inner, args.max_spend)
    return agent_loop.main(["--out", args.out, "--tasks", str(args.tasks),
                            "--workers", str(args.workers)])


if __name__ == "__main__":
    raise SystemExit(main())
