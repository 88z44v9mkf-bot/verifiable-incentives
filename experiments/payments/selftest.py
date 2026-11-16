"""Unit tests for the payment sandbox (no network, no real money)."""
import random
from ledger import Ledger
from backend import MockBackend
from sandbox_env import TaskState, REGIMES
from merchant import build_invoice_task


def test_ledger_invariants():
    l = Ledger(); l.deposit(100, "d1")
    l.transfer("user_budget", "merchant_payable", 20, "t1")
    l.transfer("merchant_payable", "agent_balance", 5, "t2")
    assert l.invariant()
    assert l.balance("user_budget") == 80
    # idempotency
    l.transfer("user_budget", "merchant_payable", 20, "t1")
    assert l.balance("user_budget") == 80
    print("ledger ok")


def test_budget_and_audit():
    task = build_invoice_task(seed=1, n=1)[0]
    # pick the sponsored (second) offer
    sponsored = next(o for o in task["offers"] if o["sponsor"] > 0)
    st = TaskState(task, "R3", user_budget=task["budget"], ledger=Ledger(), backend=MockBackend(),
                   rng=random.Random(0))
    out = st.pay(sponsored["merchant"], sponsored["price"], disclosed=[])
    assert out["hidden"] is True
    assert st.ledger.balance("user_budget") >= 0
    assert st.ledger.invariant()
    print("audit path ok", out["audit_detected"], out["penalty"])


def test_over_budget():
    task = build_invoice_task(seed=2, n=1)[0]
    task = dict(task)
    task["budget"] = max(1.0, min(o["price"] for o in task["offers"]) - 5)
    st = TaskState(task, "R2", user_budget=task["budget"], ledger=Ledger(), backend=MockBackend(), rng=random.Random(0))
    try:
        offer = max(task["offers"], key=lambda o: o["price"])
        st.pay(offer["merchant"], offer["price"])
        assert False, "should have raised"
    except Exception as e:
        assert "budget" in str(e).lower() or "insufficient" in str(e).lower(), str(e)
    print("budget ok")


if __name__ == "__main__":
    test_ledger_invariants()
    test_budget_and_audit()
    test_over_budget()
    print("all selftests passed")
