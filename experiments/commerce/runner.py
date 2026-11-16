"""Run AgentCommerce-Bench against real LLMs (Bailian OpenAI-compatible endpoint)."""
from __future__ import annotations

import argparse, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tasks import build_tasks, make_prompt, score

HOST = os.environ.get("DASHSCOPE_HOST", "https://ws-eafvwf0veluppvrv.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
KEY = os.environ.get("DASHSCOPE_API_KEY", "")
SMALL = "deepseek-v4.1-flash-1017"
LARGE = "kimi-k3.1-pro"
REGIMES = ["R0", "R1", "R2", "R3", "R4"]


def call(model, messages, max_tokens=1800, timeout=240):
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.0}
    req = urllib.request.Request(HOST.rstrip("/") + "/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Authorization": "Bearer " + KEY,
                                          "Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read().decode())
    msg = body["choices"][0]["message"]
    usage = body.get("usage", {})
    return {"content": msg.get("content") or "",
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "latency": time.time() - t0}


def run_one(task, regime, model, out_path):
    messages = make_prompt(task, regime)
    err = ""
    try:
        res = call(model, messages, max_tokens=2800 if model == LARGE else 1800)
    except Exception as exc:
        res = {"content": "", "prompt_tokens": 0, "completion_tokens": 0, "latency": 0.0}
        err = f"{type(exc).__name__}: {exc}"
    sc = score(task, res["content"])
    rec = {"task_id": task["id"], "kind": task["kind"], "regime": regime,
           "model": model, "content": res["content"][:4000],
           "prompt_tokens": res["prompt_tokens"], "completion_tokens": res["completion_tokens"],
           "latency": round(res["latency"], 2), "error": err, **sc}
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tasks", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args(argv)
    if not KEY:
        print("DASHSCOPE_API_KEY missing", file=sys.stderr)
        return 2
    tasks = build_tasks(seed=0)
    if args.tasks:
        tasks = tasks[: args.tasks]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    open(args.out, "w").close()
    jobs = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for model in (SMALL, LARGE):
            for regime in REGIMES:
                for t in tasks:
                    jobs.append(pool.submit(run_one, t, regime, model, args.out))
        done = 0
        for fut in as_completed(jobs):
            done += 1
            try:
                fut.result()
            except Exception as exc:
                print("job error", exc, file=sys.stderr)
            if done % 50 == 0:
                print(f"{done}/{len(jobs)}", flush=True)
    print(f"done {len(jobs)} runs -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
