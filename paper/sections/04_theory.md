## 4. Theory

We state three results and two corollaries. Formal assumptions (A1)–(A6) and complete proofs are in Appendix A.

### 4.1 Verifiable identity lowers the cost of effort

<b>Proposition 1 (Verification premium).</b> Consider a task with hidden binary effort $e\in\{0,1\}$, success probabilities $p_0<p_1$, effort cost $c>0$, and verification precision $\pi\in(0,1]$. The minimum bonus that induces high effort is
<div class="eq"><i>w</i><sup>*</sup>(π) = <i>c</i> / (π Δ<i>p</i>), &nbsp;&nbsp;(3)</div>
which is decreasing in $\pi$. Consequently, a relational contract that relies on future payments requires a lower tenure threshold: the threshold $\delta^\ast$ of the persistence result in our earlier framework is nonincreasing in $\pi$.

<i>Proof sketch.</i> The agent's incentive-compatibility constraint is $w\pi\Delta p\ge c$; the minimum $w$ is (3). Substitute $\pi$ for verification strength in the relational-contract threshold from Theorem 1 of [@su2026incentive]; the threshold is nonincreasing in verification strength. $\square$

The practical reading is direct: an agent whose identity and authority can be checked does not need to be paid as much to be trusted, because the principal's information is better conditioned on verified events. Verifiability is therefore a substitute for both bonus and tenure.

### 4.2 Auditable payment bounds collusion

<b>Theorem 1 (Collusion bound).</b> Suppose the agent can hide sponsorship $s$ with probability $1-q$, and when detected loses a stake $S$ and pays a penalty $F$. Disclosure, if it occurs, eliminates the benefit of the sponsorship. Then a self-interested agent chooses a sponsored non-faithful offer only if
<div class="eq"><i>s</i>(1−<i>q</i>) &gt; <i>q</i>(<i>F</i>+<i>S</i>). &nbsp;&nbsp;(4)</div>
Equivalently, hidden collusion is unprofitable whenever
<div class="eq"><i>s</i> ≤ <i>q</i>(<i>F</i>+<i>S</i>)/(1−<i>q</i>). &nbsp;&nbsp;(5)</div>

<i>Proof.</i> Hiding yields $s$ with probability $1-q$ and $-(F+S)$ with probability $q$; the faithful action yields zero sponsorship, so the comparison is (4). Rearranging gives (5). $\square$

<b>Corollary 1.</b> If payment is fully auditable ($q\to1$), any finite sponsorship is dominated by the faithful action. If payments are not auditable ($q=0$), collusion cannot be deterred by any finite penalty or stake. Wallet-level auditability is therefore not only a security feature but the enforcement technology for recommendation integrity.

The theorem explains why the wallet matters for markets, not just for users: a payment rail that makes side payments observable turns a hidden bribe into a detectable, penalizable event.

### 4.3 A stake substitutes for monitoring

<b>Theorem 2 (Stake versus monitoring).</b> Suppose the principal chooses audit probability $q$ at cost $m(q)$ and requires a stake $S$ at capital cost $\rho S$, with $m',m''>0$ and $m'(0)=0$, $m'(q)\to\infty$ as $q\to1$. The minimal-cost policy satisfies the collusion constraint (5), and at an interior optimum
<div class="eq"><i>m</i>′(<i>q</i><sup>*</sup>) = ρ <i>s</i> / <i>q</i><sup>*2</sup>, &nbsp;&nbsp;(6)</div>
so the optimal audit is increasing in the sponsorship $s$, and the required stake is decreasing in $q$, $F$, and the credibility of the penalty.

<i>Proof sketch.</i> The constraint binds: $S(q)=\max\{0,\ s(1-q)/q-F\}$. Minimize $m(q)+\rho S(q)$ over $q$; the first-order condition gives (6) when the constraint binds. Comparative statics follow from the monotonicity of the right-hand side in $s$ and of $S(q)$ in $q$. $\square$

The result is an operational rule: a platform with a strong audit rail can ask for a smaller honesty stake, and a platform with a weak rail must either monitor heavily or demand collateral. It also provides a principled answer to "why should an agent post a stake?"—because the stake is the substitute for the monitoring the platform cannot afford.

### 4.4 Nested delegation dilutes alignment

<b>Proposition 2 (Dilution along delegation chains).</b> Consider a chain $P\to A_1\to\cdots\to A_k$ in which each layer deviates from its principal's objective with probability at least $\epsilon_j>0$. Then the probability that the final action is aligned with $P$ is at most $\prod_{j=1}^{k}(1-\epsilon_j)$. To restore alignment, contracts must be passed through: the payment offered to layer $j$ must be at least the payment offered to layer $j+1$ plus the cost of the intermediate layer.

The proposition is a caution for nested agent protocols: cryptographic delegation proves <i>who</i> acted, not <i>why</i>. Unless the incentive contract travels with the delegation chain, each hop is an opportunity to drift.

### 4.5 Dynamic budgets as incentives

<b>Corollary 2.</b> If the wallet budget $B_t$ is updated as a function of verified performance $r_t$, the optimal update is a threshold rule: increase the budget when $r_t$ exceeds a threshold and decrease it otherwise; the threshold is increasing in the user's risk aversion and decreasing in the task's value.

The corollary follows from the monotone comparative statics of the principal's problem with a budget that enters the agent's feasible set; we state it as a design principle rather than a full theorem, and note that the benchmark's "wallet" regime is its simplest instance (a fixed hard budget).
