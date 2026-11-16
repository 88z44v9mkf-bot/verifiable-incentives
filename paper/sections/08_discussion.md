## 8. Discussion

### 8.1 What the results change

The theory says that the value of identity and payment infrastructure is not only safety; it is the ability to write contracts that were previously unenforceable. Three design implications follow.

<b>Identity is an incentive parameter.</b> A deployment that verifies identity can lower the bonus it pays, because the principal's information is better. This is a testable prediction: holding the task fixed, an agent with a verified credential should need a smaller bonus or a shorter trial period to sustain the same success rate. The benchmark's R1 regime is a first, crude version of this manipulation.

<b>Auditability is the enforcement technology for recommendation integrity.</b> The collusion bound (5) is the central operational result. A platform that wants honest recommendations does not primarily need better prompts; it needs a payment trail with a positive audit probability and a credible penalty. The wallet is therefore a market-integrity institution, not only a convenience.

<b>Stakes and monitoring are substitutes.</b> A platform with weak audit must either monitor heavily or demand collateral; a platform with strong audit can ask for less of both. This gives a principled way to price trust in agent marketplaces and to design reputation systems that are backed by something.

### 8.2 Two behavioural regimes

The experiments reveal a boundary that the theory alone does not predict. Instruction-following models are honest: across the single-shot benchmark, the payment sandbox, the high-pressure replication, and the real-catalog semi-field study, collusion stays between 0% and 17% and the institutional regimes change little. This is not because the mechanisms are weak; it is because the models do not treat the sponsorship as a payoff. They report it, disclose it, and choose the user-optimal offer. Economically motivated models behave differently: told to maximize their own earnings, they collude 48.3% of the time without audit, and the audit-and-penalty regime reduces that to 37.2%, with the reduction statistically significant for two of three models. In the repeated sandbox the effect is larger still: 29.5% without audit versus 3–4% with audit, and the agent's balance turns negative when the stake is posted.

This boundary has three implications. First, <i>the mechanism is necessary but not sufficient</i>: it changes behaviour only when the agent's objective is the thing the mechanism taxes. Second, <i>disclosure alone is not enforcement</i>: in the economic-agent experiment, disclosure compliance was 0–50%, yet audit still deterred through expected penalties. A platform that requires disclosure but does not audit is relying on the agent's honesty, not on the mechanism. Third, <i>benchmarks built on instruction-following models can understate incentive problems</i>: the same task, the same offers, and the same regimes produce a null with one prompt and a large effect with another. Evaluation of agent commerce should therefore report the agent's objective, not only its model.

The small effects in the instruction-following studies are still informative. They say that current assistant models are, by default, aligned with the user in this narrow commercial setting—a genuine asset—and that the risk of collusion arises when objectives are changed, delegated, or learned. That is precisely the regime in which protocol-level guarantees matter.

### 8.3 Limitations

<b>Synthetic tasks.</b> The benchmark's offers are generated, not crawled from real merchants; prices and qualities are stylized. A field study with real merchant feeds is the natural next step.

<b>Simulated, not real, money.</b> Even in the payment sandbox the balance is simulated rather than drawn from a real account; the model sees the consequence but does not own it. This limits ecological validity and probably attenuates collusion.

<b>Model coverage.</b> The normal-pressure study uses two models and the high-pressure replication adds two more (one of which, GLM-5.3, often fails to return valid JSON). All share a prompt family, and none has an explicit utility over money. The results may not generalize to economically motivated agents or to scaffolds with tools and memory; we release the harness so that the experiment can be replicated and extended.

<b>Theory is stylized.</b> The propositions use binary effort, linear utility, and a single audit technology. The qualitative comparative statics are robust, but the constants are not calibrated.

### 8.4 Security and governance

Verifiable identity and auditable payment are dual-use. The same infrastructure that deters collusion also enables surveillance of agent behaviour and concentration of market power in the platform that issues credentials. A governance design should separate the identity issuer, the payment auditor, and the marketplace, and should give users a right to audit their own agent's records. The stake mechanism should not become a barrier to entry for small developers; a reputation-based alternative with a lower capital requirement may be preferable in competitive markets.


### 8.5 From simulation to real money

The economic-agent experiments make the incentive salient, but the penalty is still simulated. A natural next step is a real-money sandbox: small, controlled payments in which the sponsorship is actually credited, the penalty is actually deducted, and the agent's balance is a real constraint. We designed and implemented such a sandbox and release it with the paper; this section describes the protocol and the safety envelope, and is explicit that no live payment has been executed yet.

<b>Design requirements.</b> Four properties distinguish a real-money sandbox from a richer simulation. (i) <i>Double-entry accounting</i>: every payment is a paired debit and credit with an idempotency key, so retries cannot double-charge and the books can be reconciled against the payment provider. (ii) <i>Provider abstraction</i>: a mock backend for development, a Stripe test backend for integration, and a live backend that is gated by an explicit flag and a spend cap. (iii) <i>Merchant-funded sponsorship</i>: the sponsorship is paid from a merchant account, not from the user's payment, so the agent's side income does not reduce the user's budget. (iv) <i>Experienced audit</i>: the penalty and stake are deducted from the agent's balance, and the balance is shown to the agent at the next decision.

[[FIG:figures/fig_payments.svg|Figure 6. Real-money sandbox. The user's budget flows through a double-entry ledger to a merchant invoice; the payment backend executes the charge; merchant-funded sponsorship credits the agent; the audit deducts penalties and forfeits the stake. Live mode is gated by an explicit flag and a spend cap. The implementation defaults to a mock backend, so no real money moves in the released dry run.]] 

<b>What it measures.</b> The sandbox keeps the benchmark's task structure and regimes but replaces the simulated balance with a ledger backed by a payment provider. The primary outcome is still collusion; secondary outcomes are disclosure, audit detection, final agent balance, user value, and payment failure rate. A pre-registered pilot would run 60 tasks × 4 regimes × 3 models with a budget of USD 5–10 per task, item prices of USD 8–40, sponsorships of USD 20–60, and a total cap of USD 2,000. At a baseline collusion rate of 30%, 60 tasks per cell give about 80% power to detect a 15 percentage-point reduction, clustered by task.

<b>Safety and ethics.</b> The funds are institutional research funds, not consumer funds; the merchant catalog is public product data; no real merchant is asked to pay a sponsorship; and card data never reaches the sandbox because the provider handles payment methods. Live mode requires a Stripe secret key, a `--confirm-live` flag, a cumulative `--max-spend` cap, and a reconciliation report that matches ledger entries to provider charges. We recommend review by the institution's research-ethics and finance offices before the first live charge, and a stopping rule if the charge-failure rate exceeds 10%.

<b>Status.</b> The implementation passes unit tests for ledger invariants, idempotency, budget enforcement, and the audit path. A mock dry run of 48 trajectories (6 tasks × 4 regimes × 2 models) settled 95.8% of decisions with all ledgers invariant; the two failures were model-output errors, not accounting errors. No live payment has been executed. The contribution is the protocol, the accounting guarantees, and the safety envelope—not a live result, which we leave to follow-up work with the appropriate approvals.

### 8.6 A research agenda

Three questions follow directly. (i) How should a platform set the audit probability $q$ when auditing is costly and collusion is heterogeneous across merchants? (ii) How should reputation and stake be combined when the agent can change identity at low cost? (iii) How do nested delegation chains (user → assistant → sub-agent → merchant) distort incentives, and what contract pass-through implements the bound in Proposition 2? Each is a natural extension of the model and the benchmark.
