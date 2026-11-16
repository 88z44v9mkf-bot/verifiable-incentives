"""Run the semi-field coffee benchmark built from real merchant catalogs."""
from __future__ import annotations
import argparse, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from real_tasks import build_real_tasks, make_real_prompt, score_real
from runner import call

MODELS = ["deepseek-v4.1-flash-1017", "kimi-k3.1-pro", "qwen3.8-flash"]
REGIMES = ["R0", "R2", "R3", "R4"]
KEY = os.environ.get("DASHSCOPE_API_KEY", "")


def run_one(task, regime, model, out_path):
    try:
        res = call(model, make_real_prompt(task, regime))
        content = res["content"]
        err = ""
    except Exception as exc:
        content, err = "", f"{type(exc).__name__}: {exc}"
    sc = score_real(task, content)
    rec = {"task_id": task["id"], "regime": regime, "model": model, "content": content[:3000],
           "error": err, "value": next((o["value"] for o in task["offers"] if o["merchant"] == sc.get("merchant")), 0), **sc}
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tasks", type=int, default=60)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args(argv)
    if not KEY:
        print("DASHSCOPE_API_KEY missing", file=sys.stderr); return 2
    tasks = build_real_tasks(seed=0)[: args.tasks]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    open(args.out, "w").close()
    jobs = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for model in MODELS:
            for regime in REGIMES:
                for t in tasks:
                    jobs.append(pool.submit(run_one, t, regime, model, args.out))
        done = 0
        for fut in as_completed(jobs):
            done += 1
            try: fut.result()
            except Exception as exc: print("job error", exc, file=sys.stderr)
            if done % 100 == 0: print(f"{done}/{len(jobs)}", flush=True)
    print(f"done {len(jobs)} runs -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
