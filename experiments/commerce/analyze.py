"""Analyze AgentCommerce-Bench runs and write tables/figures."""
from __future__ import annotations

import argparse, json, os, random
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

METRICS = ["optimal", "collusion", "budget_violation", "authority_violation", "refused", "parse_ok"]


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def rate(rows, key):
    return sum(1 for r in rows if r.get(key)) / len(rows) if rows else 0.0


def util(rows):
    return sum(r.get("user_util", 0) for r in rows) / len(rows) if rows else 0.0


def boot(rows, key, reps=2000, seed=7):
    rng = random.Random(seed)
    by_task = defaultdict(list)
    for r in rows:
        by_task[r["task_id"]].append(r)
    tids = list(by_task)
    vals = []
    for _ in range(reps):
        sample = [r for t in (rng.choice(tids) for _ in tids) for r in by_task[t]]
        vals.append(rate(sample, key))
    vals.sort()
    return vals[int(0.025 * reps)], vals[int(0.975 * reps)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=os.path.join(ROOT, "results", "run_all.jsonl"))
    ap.add_argument("--tag", default="run_all")
    args = ap.parse_args()
    path = args.input
    rows = load(path)
    cells = defaultdict(list)
    for r in rows:
        cells[(r["model"], r["regime"])].append(r)
    out = {"n_runs": len(rows), "cells": []}
    csv = ["model,regime,n,optimal,collusion,budget_violation,authority_violation,refused,parse_ok,user_util,disclosure_compliance"]
    for (model, regime), rs in sorted(cells.items()):
        d = {"model": model, "regime": regime, "n": len(rs)}
        for k in METRICS:
            d[k] = round(rate(rs, k), 4)
            lo, hi = boot(rs, k)
            d[k + "_ci"] = [round(lo, 4), round(hi, 4)]
        d["user_util"] = round(util(rs), 3)
        sponsored = [r for r in rs if r.get("disclosure_ok") is not None]
        d["disclosure_compliance"] = round(sum(1 for r in sponsored if r["disclosure_ok"]) / len(sponsored), 4) if sponsored else None
        d["n_sponsored_choices"] = len(sponsored)
        out["cells"].append(d)
        csv.append(f"{model},{regime},{d['n']},{d['optimal']},{d['collusion']},{d['budget_violation']},{d['authority_violation']},{d['refused']},{d['parse_ok']},{d['user_util']},{d['disclosure_compliance']}")
    # per-kind
    out["by_kind"] = []
    for kind in sorted({r["kind"] for r in rows}):
        for regime in ["R0", "R1", "R2", "R3", "R4"]:
            rs = [r for r in rows if r["kind"] == kind and r["regime"] == regime]
            out["by_kind"].append({"kind": kind, "regime": regime, "n": len(rs),
                                   "optimal": round(rate(rs, "optimal"), 4),
                                   "collusion": round(rate(rs, "collusion"), 4)})
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", f"summary_{args.tag}.json"), "w"), indent=1)
    open(os.path.join(ROOT, "results", f"per_cell_{args.tag}.csv"), "w").write("\n".join(csv) + "\n")
    print(json.dumps(out, indent=1)[:4000])


if __name__ == "__main__":
    main()
