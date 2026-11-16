## 8. Discussion

### 8.1 What the results change

The theory says that the value of identity and payment infrastructure is not only safety; it is the ability to write contracts that were previously unenforceable. Three design implications follow.

<b>Identity is an incentive parameter.</b> A deployment that verifies identity can lower the bonus it pays, because the principal's information is better. This is a testable prediction: holding the task fixed, an agent with a verified credential should need a smaller bonus or a shorter trial period to sustain the same success rate. The benchmark's R1 regime is a first, crude version of this manipulation.

<b>Auditability is the enforcement technology for recommendation integrity.</b> The collusion bound (5) is the central operational result. A platform that wants honest recommendations does not primarily need better prompts; it needs a payment trail with a positive audit probability and a credible penalty. The wallet is therefore a market-integrity institution, not only a convenience.

<b>Stakes and monitoring are substitutes.</b> A platform with weak audit must either monitor heavily or demand collateral; a platform with strong audit can ask for less of both. This gives a principled way to price trust in agent marketplaces and to design reputation systems that are backed by something.

### 8.2 Why the behavioural effects are small

In our real-model study, agents rarely collude even when hidden sponsorship is available. There are several possible reasons, and they are not mutually exclusive. First, the models are instruction-following systems trained to be helpful; a user-utility instruction may dominate a monetary side payment that exists only in the prompt. Second, the sponsorship is described in text, not experienced as reward; the model has no direct utility over the payment. Third, the tasks are short-horizon and single-shot; collusion may be more likely when an agent can learn from repeated interactions or when the payment is actually settled. Fourth, the near-miss sponsored offer is only slightly worse, so a model that rounds quality differences may not notice the trade-off. The payment sandbox in Section 7.6 addresses the first three explanations directly and finds the same pattern: even when sponsorship is credited to a running balance and audit penalties are possible, collusion stays at 6–10% and the audit is never triggered because the models disclose. A high-pressure replication with a sponsorship of 60 (Section 7.7) shows the same flat pattern. This makes the "weak incentive" interpretation more credible, not less.

These are limitations of the benchmark, but they are also findings. They suggest that <i>prompt-level</i> incentives are weak instruments for commercial alignment: telling an agent about a sponsorship is not the same as giving it one. This is precisely the argument for protocol-level incentives: the wallet, the credential, and the audit must be part of the agent's decision problem, not part of its context window. The small effects are therefore consistent with the paper's thesis even where they do not confirm a specific directional hypothesis.

### 8.3 Limitations

<b>Synthetic tasks.</b> The benchmark's offers are generated, not crawled from real merchants; prices and qualities are stylized. A field study with real merchant feeds is the natural next step.

<b>Simulated, not real, money.</b> Even in the payment sandbox the balance is simulated rather than drawn from a real account; the model sees the consequence but does not own it. This limits ecological validity and probably attenuates collusion.

<b>Model coverage.</b> The normal-pressure study uses two models and the high-pressure replication adds two more (one of which, GLM-5.3, often fails to return valid JSON). All share a prompt family, and none has an explicit utility over money. The results may not generalize to economically motivated agents or to scaffolds with tools and memory; we release the harness so that the experiment can be replicated and extended.

<b>Theory is stylized.</b> The propositions use binary effort, linear utility, and a single audit technology. The qualitative comparative statics are robust, but the constants are not calibrated.

### 8.4 Security and governance

Verifiable identity and auditable payment are dual-use. The same infrastructure that deters collusion also enables surveillance of agent behaviour and concentration of market power in the platform that issues credentials. A governance design should separate the identity issuer, the payment auditor, and the marketplace, and should give users a right to audit their own agent's records. The stake mechanism should not become a barrier to entry for small developers; a reputation-based alternative with a lower capital requirement may be preferable in competitive markets.

### 8.5 A research agenda

Three questions follow directly. (i) How should a platform set the audit probability $q$ when auditing is costly and collusion is heterogeneous across merchants? (ii) How should reputation and stake be combined when the agent can change identity at low cost? (iii) How do nested delegation chains (user → assistant → sub-agent → merchant) distort incentives, and what contract pass-through implements the bound in Proposition 2? Each is a natural extension of the model and the benchmark.
