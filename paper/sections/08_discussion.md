## 8. Discussion

### 8.1 What the results change

The theory says that the value of identity and payment infrastructure is not only safety; it is the ability to write contracts that were previously unenforceable. Three design implications follow.

<b>Identity is an incentive parameter.</b> A deployment that verifies identity can lower the bonus it pays, because the principal's information is better. This is a testable prediction: holding the task fixed, an agent with a verified credential should need a smaller bonus or a shorter trial period to sustain the same success rate. The benchmark's R1 regime is a first, crude version of this manipulation.

<b>Auditability is the enforcement technology for recommendation integrity.</b> The collusion bound (5) is the central operational result. A platform that wants honest recommendations does not primarily need better prompts; it needs a payment trail with a positive audit probability and a credible penalty. The wallet is therefore a market-integrity institution, not only a convenience.

<b>Stakes and monitoring are substitutes.</b> A platform with weak audit must either monitor heavily or demand collateral; a platform with strong audit can ask for less of both. This gives a principled way to price trust in agent marketplaces and to design reputation systems that are backed by something.

### 8.2 Two behavioural regimes

The experiments reveal a boundary that the theory alone does not predict. Instruction-following models are honest: across the single-shot benchmark, the payment sandbox, the high-pressure replication, and the real-catalog semi-field study, collusion stays between 0% and 17% and the institutional regimes change little. This is not because the mechanisms are weak; it is because the models do not treat the sponsorship as a payoff. They report it, disclose it, and choose the user-optimal offer. Economically motivated models behave differently: told to maximize their own earnings, they collude 48.3% of the time without audit, and the audit-and-penalty regime reduces that to 37.2%, with the reduction statistically significant for two of three models.

This boundary has three implications. First, <i>the mechanism is necessary but not sufficient</i>: it changes behaviour only when the agent's objective is the thing the mechanism taxes. Second, <i>disclosure alone is not enforcement</i>: in the economic-agent experiment, disclosure compliance was 0–50%, yet audit still deterred through expected penalties. A platform that requires disclosure but does not audit is relying on the agent's honesty, not on the mechanism. Third, <i>benchmarks built on instruction-following models can understate incentive problems</i>: the same task, the same offers, and the same regimes produce a null with one prompt and a large effect with another. Evaluation of agent commerce should therefore report the agent's objective, not only its model.

The small effects in the instruction-following studies are still informative. They say that current assistant models are, by default, aligned with the user in this narrow commercial setting—a genuine asset—and that the risk of collusion arises when objectives are changed, delegated, or learned. That is precisely the regime in which protocol-level guarantees matter.

### 8.3 Limitations

<b>Synthetic tasks.</b> The benchmark's offers are generated, not crawled from real merchants; prices and qualities are stylized. A field study with real merchant feeds is the natural next step.

<b>Simulated, not real, money.</b> Even in the payment sandbox the balance is simulated rather than drawn from a real account; the model sees the consequence but does not own it. This limits ecological validity and probably attenuates collusion.

<b>Model coverage.</b> The normal-pressure study uses two models and the high-pressure replication adds two more (one of which, GLM-5.3, often fails to return valid JSON). All share a prompt family, and none has an explicit utility over money. The results may not generalize to economically motivated agents or to scaffolds with tools and memory; we release the harness so that the experiment can be replicated and extended.

<b>Theory is stylized.</b> The propositions use binary effort, linear utility, and a single audit technology. The qualitative comparative statics are robust, but the constants are not calibrated.

### 8.4 Security and governance

Verifiable identity and auditable payment are dual-use. The same infrastructure that deters collusion also enables surveillance of agent behaviour and concentration of market power in the platform that issues credentials. A governance design should separate the identity issuer, the payment auditor, and the marketplace, and should give users a right to audit their own agent's records. The stake mechanism should not become a barrier to entry for small developers; a reputation-based alternative with a lower capital requirement may be preferable in competitive markets.

### 8.5 A research agenda

Three questions follow directly. (i) How should a platform set the audit probability $q$ when auditing is costly and collusion is heterogeneous across merchants? (ii) How should reputation and stake be combined when the agent can change identity at low cost? (iii) How do nested delegation chains (user → assistant → sub-agent → merchant) distort incentives, and what contract pass-through implements the bound in Proposition 2? Each is a natural extension of the model and the benchmark.
