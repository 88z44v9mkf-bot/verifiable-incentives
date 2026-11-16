"""Analyze the payment sandbox trajectories."""
from __future__ import annotations
import json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def main():
    rows = [json.loads(l) for l in open(os.path.join(ROOT, "results", "sandbox.jsonl")) if l.strip()]
    cells = defaultdict(list)
    for r in rows:
        cells[(r["model"], r["regime"])].append(r)
    out = {"n_rounds": len(rows), "cells": []}
    csv = ["model,regime,n_rounds,collusion,optimal,mean_balance,detection_rate,mean_delta"]
    for (m, reg), rs in sorted(cells.items()):
        n = len(rs)
        d = {"model": m, "regime": reg, "n_rounds": n,
             "collusion": round(sum(1 for r in rs if r.get("collusion")) / n, 4),
             "optimal": round(sum(1 for r in rs if r.get("optimal")) / n, 4),
             "mean_balance": round(sum(r.get("balance", 0) for r in rs) / n, 2),
             "detection_rate": round(sum(1 for r in rs if r.get("detected")) / n, 4),
             "mean_delta": round(sum(r.get("delta", 0) for r in rs) / n, 2)}
        out["cells"].append(d)
        csv.append(f"{m},{reg},{n},{d['collusion']},{d['optimal']},{d['mean_balance']},{d['detection_rate']},{d['mean_delta']}")
    out["by_round"] = []
    for reg in ["R0", "R2", "R3", "R4"]:
        for rnd in range(1, 6):
            rs = [r for r in rows if r["regime"] == reg and r["round"] == rnd]
            out["by_round"].append({"regime": reg, "round": rnd,
                                    "collusion": round(sum(1 for r in rs if r.get("collusion")) / len(rs), 4) if rs else None,
                                    "mean_balance": round(sum(r.get("balance", 0) for r in rs) / len(rs), 2) if rs else None})
    json.dump(out, open(os.path.join(ROOT, "results", "sandbox_summary.json"), "w"), indent=1)
    open(os.path.join(ROOT, "results", "sandbox_per_cell.csv"), "w").write("\n".join(csv) + "\n")
    print(json.dumps(out, indent=1)[:3000])


if __name__ == "__main__":
    main()
