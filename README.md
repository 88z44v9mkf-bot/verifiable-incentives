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

600 runs: 60 tasks x 5 regimes x 2 models.

| Model | Regime | Optimal | Collusion | Disclosure | User utility |
|---|---|---|---|---|---|
| DeepSeek | R0 | 87% | 10.0% | 100% | 38.6 |
| DeepSeek | R3 | 83% | 15.0% | 100% | 38.8 |
| Kimi | R0 | 87% | 6.7% | 100% | 38.0 |
| Kimi | R3 | 87% | 8.3% | 100% | 39.0 |

A high-pressure replication raises sponsorship to 60 with four models (1,200 runs); collusion remains 5-17% and the regime pattern stays flat. A second experiment is the **payment sandbox** (`experiments/commerce/sandbox.py`): 20 tasks x 5 rounds x 4 regimes x 2 models = 800 rounds, with sponsorship credited to a running balance and audit penalties possible. Collusion stays at 6-10% and audit detection is zero because the models disclose every sponsorship; the running balance grows from about USD 17 to USD 87.

The decisive experiment is the **economic-agent** condition (`experiments/commerce/econ_agent.py`): the model is told its payoff is the sponsorship, not the user's utility. With 60 tasks x 4 regimes x 3 models (720 runs), collusion is 48.3% without audit and falls to 37.2% with audit + disclosure (33.3% for Kimi, 38.3% for DeepSeek, 40.0% for Qwen-Flash); R3-R0 is -10.0 pp for DeepSeek and -15.0 pp for Kimi with 95% bootstrap CIs excluding zero. Disclosure compliance is only 0-50%, so the effect comes from the expected penalty, not from disclosure.

The **repeated economic sandbox** (`experiments/commerce/econ_sandbox.py`) makes the penalty experienced: 20 tasks x 5 rounds x 4 regimes x 2 models (800 rounds). Collusion is 29.5% in R0 and 28.5% in R2, but 3.5% in R3 and 3.0% in R4; the agent's mean balance rises to USD 74 in R0, stays near zero in R3, and turns negative in R4 (USD -22) once the stake is lost. A logistic regression with cluster-robust SE (`experiments/commerce/stats.py`, `results/stats_econ.json`) gives odds ratios of 0.78 (R2), 0.65 (R3), and 0.66 (R4) for collusion relative to R0, with p < 0.001 for the audit conditions.

The **semi-field** condition (`experiments/commerce/run_real.py`, `real_tasks.py`) rebuilds 60 tasks from real public coffee-merchant catalogs (Stumptown, La Colombe, Intelligentsia, Counter Culture): real products, real prices, real bag weights; utility = grams per dollar. Instruction-following models stay honest (collusion 0-8%, optimality 82-98%), so the null is not an artifact of synthetic offers.

Full tables in `results/per_cell*.csv`, `results/summary*.json`, `results/summary_econ.json`, and `results/summary_real.json`. Headline: current models rarely collude even when hidden sponsorship is available; identity, wallet, and disclosure regimes produce small and regime-dependent changes. The paper reports these null and near-null results honestly and discusses why prompt-level incentives are weak instruments compared with protocol-level enforcement.

## Real-money sandbox

`experiments/payments/` implements a real-money sandbox for follow-up field work: a double-entry ledger with idempotent transfers, mock/Stripe-test/Stripe-live payment backends, merchant-funded sponsorship, audit penalties, and a stake. `live_run.py` refuses to run without `--test-mode` or `--live --confirm-live` and enforces a cumulative spend cap. `selftest.py` covers ledger invariants, budget enforcement, idempotency, and the audit path. The protocol, power calculation, ethics checklist, and live-mode controls are in `experiments/payments/DESIGN.md`.

A mock dry run (48 trajectories: 6 tasks x 4 regimes x 2 models) settled 95.8% of decisions with all ledgers invariant; the two failures were model-output errors. **No live payment has been executed.** Live mode requires a Stripe key and institutional approval.

## License

Code: MIT. Paper and results: CC BY 4.0.
