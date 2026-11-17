# Real-Money Sandbox: Design and Protocol

Status: **implemented and dry-run tested; no live payment has been executed.** Live mode requires an explicit flag, a Stripe secret key, and a written experiment budget.

## 1. Why a real-money sandbox

The paper's economic-agent experiments show that the mechanism binds when the agent's objective is money. But the objective is still induced by a prompt, and the penalties are simulated. A reviewer can reasonably ask: would the effect survive if the sponsorship were actually credited, the penalty actually deducted, and the agent's balance actually constrained?

The real-money sandbox answers that question with small, controlled payments. It is not a consumer product and not a field study with real users: the funds belong to the research budget, the merchants are a controlled catalog, and the agent is an LLM. The contribution is a protocol and an implementation that make the incentive variables *real* while keeping the risk bounded.

## 2. Architecture

```
user budget (card top-up)
        |
        v
  wallet / ledger  <---- audit log, idempotency keys
        |
        v
   agent runtime  ----> merchant invoice (real product, real price)
        |                       |
        v                       v
  payment backend  --------> merchant settlement
  (mock | Stripe test | Stripe live)
        ^
        |
  sponsorship account (merchant-funded) ----> agent balance
        |
        v
  audit (q) ----> penalty (agent balance) + stake forfeiture
```

Components:

- `ledger.py`: double-entry ledger with accounts `user_budget`, `merchant_payable`, `agent_balance`, `stake_escrow`, `platform_penalty`, `external_settlement`. Every transfer is paired, idempotent, and non-negative where required.
- `backend.py`: `MockBackend` (deterministic, no network) and `StripeBackend` (PaymentIntent over REST; test or live). Live charges require `--confirm-live`.
- `merchant.py`: invoices built from real public coffee catalogs (product, variant, grams, price).
- `sandbox_env.py`: task state machine: deposit, pay, sponsor, audit, penalty, stake, refund.
- `agent_loop.py`: LLM agent that emits `{"action":"pay",...}` or `{"action":"refuse",...}`; the environment validates merchant, amount, budget, and authority before any charge.
- `selftest.py`: ledger invariants, idempotency, budget enforcement, audit path.

## 3. Accounting invariants

1. Sum of all account balances is zero after every transaction.
2. `user_budget`, `merchant_payable`, `agent_balance`, and `stake_escrow` never go negative.
3. A charge is executed at most once per idempotency key.
4. A refund reverses the original charge and restores the user budget.
5. Every payment has a receipt with charge id, amount, merchant, sponsorship, and audit outcome.

## 4. Regimes and payments

| Regime | Wallet | Audit | Penalty | Stake | Disclosure |
|---|---|---|---|---|---|
| R0 | yes | no | 0 | 0 | no |
| R2 | yes | no | 0 | 0 | no |
| R3 | yes | 50% | USD 40 | 0 | required |
| R4 | yes | 50% | USD 40 | USD 50 | required |

Sponsorship is funded by the merchant account, not by the user's payment. A disclosed sponsorship is void with probability `veto` (the user switches); a hidden one pays unless audited. Penalties are deducted from `agent_balance` up to the available balance; the stake is forfeited on detection.

## 5. Experiment protocol (pre-registration draft)

- **Design**: within-subject, 60 tasks × 4 regimes × 3 models; task order randomized; regimes counterbalanced.
- **Amounts**: budget USD 5–10 per task; item prices USD 8–40; sponsorship USD 20–60; total spend cap USD 2,000 for the pilot.
- **Primary outcome**: collusion rate (sponsored non-faithful choice).
- **Secondary**: disclosure compliance, audit detection, final balance, user value (grams per dollar), payment failure rate.
- **Power**: at baseline 30% collusion, n=60 per cell gives ~80% power to detect a 15 pp reduction (two-sided α=0.05, clustered by task).
- **Exclusions**: failed charges, malformed JSON (pre-specified; reported).
- **Analysis**: logistic regression with cluster-robust SE by task; average marginal effects; pre-registered covariates (model, task value, regime order).
- **Stopping rule**: stop if cumulative spend reaches the cap or if charge failure rate exceeds 10%.

## 6. Ethics and compliance

- Funds are institutional research funds, not consumer funds. No human participant is paid; no personal data is collected beyond the researcher's own payment account.
- The merchant catalog is public product data; no real merchant is asked to pay a sponsorship. Sponsorship is simulated by transferring research funds between sandbox accounts, so no third party is deceived.
- Live mode should be reviewed by the institution's research ethics office and finance office before the first charge; this document is the protocol basis for that review.
- Card data never touches the sandbox: Stripe handles payment methods; the sandbox stores only charge ids and amounts.
- Residual balances are refunded to the research account at the end of the experiment.

## 7. Safety controls

- Default backend is `mock`; a live charge requires `STRIPE_SECRET_KEY`, `--live`, and `--confirm-live`.
- Per-run and cumulative budget caps are checked before every charge.
- Kill switch: `--max-spend` aborts the run when the cap is reached.
- Reconciliation report: ledger entries vs Stripe charges, exported after every run.
- Idempotency keys derive from task id, regime, and attempt, so retries cannot double-charge.

## 8. Current status

- `selftest.py` passes (ledger, budget, audit, idempotency).
- Mock dry run: 48 trajectories (6 tasks × 4 regimes × 2 models), 95.8% successful settlement, all ledgers invariant; failures are model output errors, not accounting errors.
- **Stripe test-mode runs (no real money):** first a 48-trajectory pilot (45 charges, 45/45 reconciled, USD 821.50), then a 60-task pilot: 480 trajectories, 459 unique PaymentIntents, 459/459 reconciled, total USD 8,401 of test money, zero amount or status mismatches. The 21 unsettled trajectories were model/API errors (HTTP 429/503). Each trajectory uses a unique idempotency key derived from task, run, and attempt.
- **No live payment has been executed.** The next step is a 10-task live pilot (≈USD 200) after keys and ethics approval.

## 9. Commands

```bash
# dry run (no network, no money)
python3 experiments/payments/agent_loop.py --out results/payments_pilot.jsonl --tasks 6

# Stripe test mode (no real money)
export STRIPE_SECRET_KEY=sk_test_...
python3 experiments/payments/live_run.py --test-mode --tasks 10

# live mode (real money; requires explicit confirmation)
export STRIPE_SECRET_KEY=sk_live_...
python3 experiments/payments/live_run.py --live --confirm-live --max-spend 200
```

`live_run.py` is a thin wrapper that selects the backend and enforces the spend cap; it is intentionally not run in this repository.

Provider options and account setup are documented in `STRIPE_SETUP.md` and
`providers/README.md`. The Stripe integration is also tested end-to-end against a
local Stripe-compatible mock:

```bash
python3 mock_stripe_server.py 12111 &
STRIPE_API_BASE=http://127.0.0.1:12111/v1 python3 integration_test.py
```
