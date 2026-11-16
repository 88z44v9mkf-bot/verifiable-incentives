"""Reconcile the sandbox ledger against Stripe test-mode PaymentIntents."""
from __future__ import annotations
import json, os, sys, urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def fetch(charge_id, key):
    req = urllib.request.Request(f"https://api.stripe.com/v1/payment_intents/{charge_id}")
    req.add_header("Authorization", "Bearer " + key)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main(path):
    key = os.environ.get("STRIPE_SECRET_KEY", "")
    if not key.startswith("sk_test_"):
        print("refusing: reconciliation is test-mode only (sk_test_)", file=sys.stderr)
        return 2
    rows = [json.loads(l) for l in open(path) if l.strip()]
    ids, amounts, errors = [], defaultdict(float), []
    for r in rows:
        o = r.get("outcome") or {}
        cid = o.get("charge_id")
        if cid:
            ids.append(cid); amounts[cid] += float(o.get("price", 0))
    unique = sorted(set(ids))
    matched, missing, mismatched = 0, 0, 0
    total = 0.0
    for cid in unique:
        try:
            pi = fetch(cid, key)
        except Exception as exc:
            missing += 1; errors.append(f"{cid}: {exc}"); continue
        expected = int(round(amounts[cid] * 100))
        if pi.get("amount") == expected and pi.get("status") in ("succeeded", "requires_capture"):
            matched += 1
            total += pi.get("amount", 0) / 100
        else:
            mismatched += 1
            errors.append(f"{cid}: expected {expected}, got {pi.get('amount')} status {pi.get('status')}")
    out = {"n_records": len(rows), "n_charges": len(ids), "n_unique": len(unique),
           "matched": matched, "missing": missing, "mismatched": mismatched,
           "total_usd": round(total, 2), "errors": errors[:10]}
    json.dump(out, open(os.path.join(HERE, "..", "..", "results", "stripe_reconciliation.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
