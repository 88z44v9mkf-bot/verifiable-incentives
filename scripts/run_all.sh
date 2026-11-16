#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 experiments/commerce/runner.py --out results/run_all.jsonl --tasks 60 --workers 8
python3 experiments/commerce/analyze.py
