"""Logistic regression with cluster-robust standard errors (numpy only)."""
from __future__ import annotations
import json, math, sys
import numpy as np

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def fit_logit(X, y, clusters, max_iter=100, tol=1e-8):
    n, k = X.shape
    beta = np.zeros(k)
    for _ in range(max_iter):
        eta = X @ beta
        p = sigmoid(eta)
        W = np.clip(p * (1 - p), 1e-8, None)
        z = eta + (y - p) / W
        XtW = X.T * W
        H = XtW @ X
        beta_new = np.linalg.solve(H, XtW @ z)
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            break
        beta = beta_new
    p = sigmoid(X @ beta)
    W = np.clip(p * (1 - p), 1e-8, None)
    H = (X.T * W) @ X
    Hinv = np.linalg.inv(H)
    # cluster-robust meat
    meat = np.zeros((k, k))
    for c in np.unique(clusters):
        idx = clusters == c
        Xg = X[idx]
        ug = (y[idx] - p[idx])
        s = Xg.T @ ug
        meat += np.outer(s, s)
    V = Hinv @ meat @ Hinv
    se = np.sqrt(np.diag(V))
    return beta, se, p

def main(path, out, fe=False):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    rows = [r for r in rows if r.get("parse_ok")]
    tasks = sorted({r["task_id"] for r in rows})
    models = sorted({r["model"] for r in rows})
    regs = ["R0", "R2", "R3", "R4"]
    ti = {t: i for i, t in enumerate(tasks)}
    mi = {m: i for i, m in enumerate(models)}
    ri = {"R0": 0, "R2": 1, "R3": 2, "R4": 3}
    # design: intercept, R2,R3,R4, model dummies, task dummies (drop first)
    k = 1 + 3 + (len(models) - 1) + ((len(tasks) - 1) if fe else 0)
    X = np.zeros((len(rows), k)); y = np.zeros(len(rows)); cl = np.zeros(len(rows), dtype=int)
    for i, r in enumerate(rows):
        X[i, 0] = 1
        if r["regime"] != "R0":
            X[i, 1 + ri[r["regime"]] - 1] = 1
        if mi[r["model"]] > 0:
            X[i, 4 + mi[r["model"]] - 1] = 1
        if fe and ti[r["task_id"]] > 0:
            X[i, 4 + len(models) - 1 + ti[r["task_id"]] - 1] = 1
        y[i] = 1 if r.get("collusion") else 0
        cl[i] = ti[r["task_id"]]
    beta, se, p = fit_logit(X, y, cl)
    names = ["Intercept", "R2", "R3", "R4"] + [f"model={m}" for m in models[1:]] + (["task FE"] * (len(tasks) - 1) if fe else [])
    outd = {"n": len(rows), "terms": []}
    for j in range(min(k, 4 + len(models) - 1)):
        z = beta[j] / se[j] if se[j] > 0 else float("nan")
        outd["terms"].append({"term": names[j], "coef": round(float(beta[j]), 4),
                              "se": round(float(se[j]), 4), "or": round(float(math.exp(beta[j])), 3),
                              "z": round(float(z), 2), "p": round(float(2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))), 4)})
    # average marginal effects for regime dummies
    base = sigmoid(X @ beta)
    ames = {}
    for name, j in [("R2", 1), ("R3", 2), ("R4", 3)]:
        X2 = X.copy(); X2[:, j] = 1
        ames[name] = round(float(np.mean(sigmoid(X2 @ beta) - base)), 4)
    outd["ame_vs_R0"] = ames
    json.dump(outd, open(out, "w"), indent=1)
    print(json.dumps(outd, indent=1))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], fe=("--fe" in sys.argv))
