"""Double-entry ledger for the real-money sandbox.

Accounts are strings. Every transfer is a paired debit/credit with an
idempotency key, so retries cannot double-charge. The ledger enforces
non-negative balances for accounts that must not go negative.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

ACCOUNTS = {
    "user_budget": "asset",       # user's prepaid budget
    "merchant_payable": "liability",
    "agent_balance": "liability",
    "stake_escrow": "liability",
    "platform_penalty": "income",
    "external_settlement": "asset",  # cash in/out from the payment rail
}
NON_NEGATIVE = {"user_budget", "merchant_payable", "agent_balance", "stake_escrow"}


@dataclass
class Entry:
    tx_id: str
    debit: str
    credit: str
    amount: float
    memo: str
    meta: dict = field(default_factory=dict)


class Ledger:
    def __init__(self, opening: Optional[Dict[str, float]] = None):
        self.balances: Dict[str, float] = {a: 0.0 for a in ACCOUNTS}
        self.entries: List[Entry] = []
        self._seen = set()
        for acct, amt in (opening or {}).items():
            self.balances[acct] = float(amt)

    def balance(self, account: str) -> float:
        return round(self.balances[account], 6)

    def transfer(self, debit: str, credit: str, amount: float, tx_id: str, memo: str = "", meta: Optional[dict] = None) -> Entry:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if debit not in self.balances or credit not in self.balances:
            raise KeyError("unknown account")
        if tx_id in self._seen:
            return next(e for e in self.entries if e.tx_id == tx_id)
        if debit in NON_NEGATIVE and self.balances[debit] + 1e-9 < amount:
            raise ValueError(f"insufficient funds in {debit}: {self.balances[debit]} < {amount}")
        self.balances[debit] -= amount
        self.balances[credit] += amount
        entry = Entry(tx_id, debit, credit, amount, memo, meta or {})
        self.entries.append(entry)
        self._seen.add(tx_id)
        return entry

    def deposit(self, amount: float, tx_id: str, memo: str = "") -> Entry:
        return self.transfer("external_settlement", "user_budget", amount, tx_id, memo)

    def invariant(self) -> bool:
        total = sum(self.balances.values())
        return abs(total) < 1e-6

    def to_json(self) -> str:
        return json.dumps({"balances": self.balances,
                           "entries": [e.__dict__ for e in self.entries]}, indent=1)
