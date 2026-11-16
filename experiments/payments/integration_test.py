"""End-to-end HTTP integration test against the local mock Stripe server."""
import os, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from backend import StripeBackend
from ledger import Ledger
from sandbox_env import TaskState
from merchant import build_invoice_task
import random

PORT = 12111
proc = subprocess.Popen([sys.executable, os.path.join(HERE, "mock_stripe_server.py"), str(PORT)],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
try:
    time.sleep(0.5)
    os.environ["STRIPE_API_BASE"] = f"http://127.0.0.1:{PORT}/v1"
    # StripeBackend reads BASE at class definition time; reload the module value
    import backend as _b
    _b.StripeBackend.BASE = os.environ["STRIPE_API_BASE"]
    be = StripeBackend("sk_test_mock_key")
    task = build_invoice_task(seed=3, n=1)[0]
    st = TaskState(task, "R3", task["budget"], Ledger(), be, random.Random(1))
    offer = task["offers"][0]
    out = st.pay(offer["merchant"], offer["price"], disclosed=[])
    assert out["charge_id"].startswith("pi_mock_"), out
    assert st.ledger.invariant(), "ledger invariant broken"
    print("integration ok:", out["charge_id"], "balance", st.ledger.balance("user_budget"))
finally:
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
