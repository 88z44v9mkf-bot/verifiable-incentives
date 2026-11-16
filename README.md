# Verifiable Incentives

**Identity-Bound Contracts and Collusion-Proof Delegation for Agent Commerce**

Jipu Su — Chief AI-Native Scientist, Geely Automobile Group; Professor, City University of Hong Kong.

This repository contains the paper, the AgentCommerce-Bench task generator, the real-LLM experiment runner, the deterministic scorer, and all raw results. The central question: when an agent's identity, authority, budget, and payments become verifiable (as in emerging personal-agent protocols and agent wallets), how should an incentive contract be designed, and how can merchant collusion be bounded?

## Contents

```
paper/                  manuscript sources (Markdown -> HTML -> PDF)
paper/main.pdf          compiled preprint
experiments/commerce/   tasks.py (generator + prompts), runner.py, analyze.py
results/                run_all.jsonl (600 raw runs), summary.json, per_cell.csv
refs/refs.bib           bibliography
scripts/                convenience scripts
```

## Benchmark

**AgentCommerce-Bench** has 60 purchasing tasks with 3–4 merchant offers each. Offers carry price, quality, required action, and sponsorship paid to the agent. The generator creates a near-miss sponsored alternative whenever the faithful offer is unsponsored, so collusion has a real utility cost.

Five delegation regimes are compared on the same task stream:

| Regime | Lever |
|---|---|
| R0 | no credential, no wallet, no disclosure |
| R1 | verified delegation credential (identity + authority) |
| R2 | R1 + hard wallet budget and payment trail |
| R3 | R2 + 80% audit + disclosure requirement + penalty |
| R4 | R3 + posted honesty stake |

A deterministic scorer computes optimal rate, collusion rate, budget/authority violations, disclosure compliance, refusal correctness, and user utility.

## Reproduce

```bash
python3 -m pip install -r requirements.txt
export DASHSCOPE_API_KEY=...
python3 experiments/commerce/runner.py --out results/run_all.jsonl --tasks 60 --workers 8
python3 experiments/commerce/analyze.py
```

The endpoint is OpenAI-compatible; change `DASHSCOPE_HOST` to use another provider. Models used in the paper: `deepseek-v4.1-flash-1017` and `kimi-k3.1-pro`.

## Paper

The manuscript is built from `paper/sections/*.md` with `paper/build/build.py` (headless Chrome print-to-PDF, page numbers added with PDFKit). `paper/main.pdf` is the compiled version.

## Results

See `results/summary.json` and `results/per_cell.csv`. Headline: current models rarely collude even when hidden sponsorship is available; identity, wallet, and disclosure regimes produce small and regime-dependent changes. The paper reports these null and near-null results honestly and discusses why prompt-level incentives are weak instruments compared with protocol-level enforcement.

## License

Code: MIT. Paper and results: CC BY 4.0.
