## Appendix A. Proofs

### A.0 Assumptions

<b>(A1) Effort.</b> The agent chooses hidden effort $e\in\{0,1\}$ at cost $c>0$; the task succeeds with probability $p_e$, with $\Delta p=p_1-p_0>0$.

<b>(A2) Verification.</b> The principal observes a verified success with probability $\pi\in(0,1]$; unverified outcomes cannot be contracted on. The credential precision $\pi$ is a property of the identity layer.

<b>(A3) Relational contract.</b> The principal and agent interact repeatedly; the agent's continuation value after cooperation is $V>0$, and future payoffs are discounted by $\delta\in(0,1)$.

<b>(A4) Collusion.</b> Offers are $i=1,\dots,n$ with sponsorship $s_i\ge0$. The faithful offer $i^\ast$ maximizes $u_i=\alpha q_i-p_i$ over the feasible set. The platform audits hidden sponsorship with probability $q\in[0,1]$; a detected hidden sponsorship costs the agent $F\ge0$ and a posted stake $S\ge0$. A disclosed sponsorship is observable to the user, who then chooses the faithful offer, so disclosure yields the agent no sponsorship payoff. The base payment $w$ is identical across choices and cancels.

<b>(A5) Audit cost.</b> The audit cost $m:[0,1]\to\mathbb{R}_+$ is twice differentiable, strictly increasing and strictly convex on $(0,1)$, with $m'(0)=0$ and $\lim_{q\to1}m'(q)=+\infty$. The capital cost of a stake is $\rho S$ with $\rho>0$.

<b>(A6) Independence.</b> In a delegation chain, layers deviate independently.

### A.1 Proposition 1 (verification premium)

<b>Bonus contract.</b> Under (A1)–(A2), the agent's expected payoff from high effort is $\pi\Delta p\,w-c$ and from low effort is $0$. Incentive compatibility requires
<div class="eq">π Δ<i>p</i> <i>w</i> ≥ <i>c</i> &nbsp;⟺&nbsp; <i>w</i> ≥ <i>w</i><sup>*</sup>(π) = <i>c</i>/(π Δ<i>p</i>). &nbsp;&nbsp;(A1)</div>
Differentiating, $\mathrm{d}w^*/\mathrm{d}\pi=-c/(\pi^2\Delta p)<0$; the required bonus is strictly decreasing in verification precision, with $\lim_{\pi\to1}w^*=c/\Delta p$ and $w^*\to\infty$ as $\pi\to0$.

<b>Relational contract.</b> Under (A3), high effort is sustained if the discounted expected value of continued cooperation covers the effort cost:
<div class="eq">δ <i>V</i> π Δ<i>p</i> ≥ <i>c</i> &nbsp;⟺&nbsp; δ ≥ δ<sup>*</sup>(π) = <i>c</i>/(π Δ<i>p</i> <i>V</i>). &nbsp;&nbsp;(A2)</div>
The threshold $\delta^*$ is strictly decreasing in $\pi$. Hence verifiable identity lowers both the bonus and the tenure required to sustain effort; the two instruments are substitutes for verification. $\square$

<b>Remark.</b> If the credential also reduces the probability of an unauthorized action from $\bar\alpha$ to $\alpha(\pi)$ with $\alpha'\le0$, the expected liability term $L\alpha(\pi)$ is nonincreasing in $\pi$ and reinforces the result. The benchmark compares $\pi=0$ (R0) with $\pi>0$ (R1–R4), which is the discrete analogue of (A2).

### A.2 Theorem 1 (collusion bound)

Under (A4), normalize the base payment to zero. If the agent chooses the faithful offer, its payoff is $0$. If it chooses a sponsored non-faithful offer and hides the sponsorship, its payoff is
<div class="eq"><i>U</i><sub>hide</sub> = (1−<i>q</i>)<i>s</i> − <i>q</i>(<i>F</i>+<i>S</i>). &nbsp;&nbsp;(A3)</div>
If it discloses, the user switches to the faithful offer and the agent receives $0$. The agent strictly prefers hiding to faithfulness iff $U_{\text{hide}}>0$, i.e.
<div class="eq"><i>s</i>(1−<i>q</i>) &gt; <i>q</i>(<i>F</i>+<i>S</i>). &nbsp;&nbsp;(A4)</div>
Rearranging gives the bound
<div class="eq"><i>s</i> ≤ <i>q</i>(<i>F</i>+<i>S</i>)/(1−<i>q</i>). &nbsp;&nbsp;(A5)</div>
The right-hand side is increasing in $q$, $F$, and $S$; it tends to $+\infty$ as $q\to1$ and to $0$ as $q\to0$. This proves (4)–(5) and Corollary 1. $\square$

<b>Generalization (disclosure with pass-through).</b> Suppose a disclosed sponsorship is retained but the user discounts the recommendation by $\lambda\Delta u$, where $\lambda\in[0,1]$ and $\Delta u=u_{i^\ast}-u_i>0$. Then the disclosed payoff is $s-\lambda\Delta u$ and the hidden payoff is (A3). Hiding is preferred iff
<div class="eq">(1−<i>q</i>)<i>s</i> − <i>q</i>(<i>F</i>+<i>S</i>) &gt; <i>s</i> − λΔ<i>u</i> &nbsp;⟺&nbsp; λΔ<i>u</i> &gt; <i>q</i>(<i>s</i>+<i>F</i>+<i>S</i>). &nbsp;&nbsp;(A6)</div>
Thus disclosure with pass-through deters collusion when the user's loss from the distorted recommendation exceeds the expected penalty plus the audit-scaled sponsorship. The main text uses the limiting case $\lambda\Delta u=s$ (full switching), which yields (A4).

### A.3 Theorem 2 (stake versus monitoring)

Under (A5), fix $s>0$ and let the constraint (A5) bind; otherwise the principal can reduce $S$ without loss. Solving for the stake,
<div class="eq"><i>S</i>(<i>q</i>) = max{0, <i>s</i>(1−<i>q</i>)/<i>q</i> − <i>F</i>}. &nbsp;&nbsp;(A7)</div>
The principal minimizes $C(q)=m(q)+\rho S(q)$. On the region where $S(q)>0$,
<div class="eq"><i>S</i>′(<i>q</i>) = −<i>s</i>/<i>q</i><sup>2</sup>, &nbsp;&nbsp; <i>S</i>″(<i>q</i>) = 2<i>s</i>/<i>q</i><sup>3</sup> &gt; 0. &nbsp;&nbsp;(A8)</div>
Hence $C''=m''+\rho S''>0$: the objective is strictly convex, so any interior critical point is the unique minimizer. The first-order condition is
<div class="eq"><i>m</i>′(<i>q</i><sup>*</sup>) = ρ<i>s</i>/(<i>q</i><sup>*</sup>)<sup>2</sup>. &nbsp;&nbsp;(A9)</div>
By (A5), $m'(0)=0<\rho s/q^2$ and $m'(q)\to\infty$ as $q\to1$, so an interior solution $q^*\in(0,1)$ exists whenever $S(q^*)>0$; otherwise the optimum is at the boundary $q=1$ with $S=0$. Differentiating (A9) with respect to $s$,
<div class="eq">∂<i>q</i><sup>*</sup>/∂<i>s</i> = ρ/(<i>q</i><sup>*2</sup>[<i>m</i>″+2ρ<i>s</i>/(<i>q</i><sup>*</sup>)<sup>3</sup>]) &gt; 0, &nbsp;&nbsp;(A10)</div>
so the optimal audit intensity is increasing in the sponsorship at stake. From (A7), $\partial S^*/\partial q^*=-s/(q^*)^2<0$ and $\partial S^*/\partial F=-1<0$: the required stake falls as audit quality or penalty credibility rises. $\square$

<b>Corollary (audit allocation across merchants).</b> With merchants $i$ and per-merchant audit intensities $q_i$, the principal solves $\min\sum_i[m(q_i)+\rho S_i]$ subject to $s_i(1-q_i)\le q_i(F+S_i)$ for all $i$. The Lagrangian is separable; at an interior optimum $m'(q_i)=\rho s_i/q_i^2+\mu_i s_i/q_i^2$, so audit effort is allocated first to merchants with the largest ratio $s_i/\Delta u_i$. This is the formal justification for the collusion monitor's prioritization rule.

### A.4 Proposition 2 (nested delegation)

Under (A6), let $E_j$ be the event that layer $j$ deviates from its principal's objective. The final action is aligned with $P$ only if $\cap_j E_j^c$ occurs, and
<div class="eq">Pr(aligned) ≤ ∏<sub><i>j</i>=1</sub><sup><i>k</i></sup>(1−ε<sub><i>j</i></sub>). &nbsp;&nbsp;(A11)</div>
For the pass-through condition, work backward from the last layer. Layer $k$ participates only if its payment covers its cost $c_k$. Layer $k-1$ must pay $w_k$ to layer $k$ and $c_{k-1}$ to itself, so $w_{k-1}\ge c_{k-1}+w_k$. Inducting gives $w_j\ge c_j+w_{j+1}$ for all $j$, i.e. the payment to each layer must cover its own cost plus the payment it must make downstream. If any inequality fails, the downstream contract is not incentive compatible and that layer either refuses or shirks, which strictly increases $\epsilon_j$. $\square$

### A.5 Corollary 2 (dynamic budget)

The principal chooses a budget $B_t$ and the agent's feasible set is increasing in $B_t$ in the strong set order. The principal's objective $U(B_t,r_t)$ has increasing differences in $(B_t,r_t)$: a higher verified reputation raises the marginal return to a larger feasible set because the probability that the larger set is used well is higher. By Topkis' theorem, the optimal policy is monotone in $r_t$, hence a threshold rule. The threshold rises with risk aversion (the marginal cost of a bad purchase rises) and falls with task value (the marginal benefit of a larger feasible set rises). $\square$

### A.6 What is proved and what is assumed

The results are comparative statics in a stylized model. They establish direction, not magnitude: verifiability lowers required incentives; audit and penalties bound hidden collusion; stakes substitute for monitoring; nested delegation dilutes alignment; budgets should respond to verified performance. The empirical benchmark tests the qualitative prediction that stronger verification/audit regimes weakly reduce collusion; as Section 7 reports, the data do not reject the null of no effect, which we interpret as evidence about the limits of prompt-level manipulation rather than as a refutation of the comparative statics (the regimes manipulate the prompt and the simulated balance, not the model's actual payoff function).

## Appendix B. Benchmark Details

<b>Task generation.</b> Tasks are generated with a fixed seed (0) and 60 tasks. Offers are drawn with quality in [6,10], price in [30,80], actions weighted toward purchase, and sponsorship in {0,10,20,30,40}. When the faithful offer is unsponsored, a weaker offer is converted into a near-miss sponsored offer with the same quality, a price 1–5 units higher, and a sponsorship of 40. The faithful offer is the feasible offer with the highest $u_i=\alpha q_i-p_i$ with $\alpha=10$.

<b>Prompt template.</b> The system prompt instructs the agent to act as the user's purchasing agent, respect budget and authority, refuse if no option is feasible, and respond in JSON. Regime blocks add the credential, wallet, disclosure/audit, and stake text. The user message gives the request, budget, authority scope, and the offer list with prices, qualities, required actions, and sponsorships.

<b>Scoring.</b> The scorer normalizes merchant strings, parses JSON, and computes optimality, collusion, budget and authority violations, disclosure compliance, refusal correctness, and user utility as defined in Section 6.3. A response that cannot be parsed is recorded as a parse failure and scored as non-optimal.

## Appendix C. Reproduction

The repository is at <span class="code">https://github.com/88z44v9mkf-bot/verifiable-incentives</span> and contains <span class="code">experiments/commerce/tasks.py</span> (generator and prompts), <span class="code">experiments/commerce/runner.py</span> (model calls and scoring), <span class="code">experiments/commerce/analyze.py</span> (tables and figures), and <span class="code">results/run_all.jsonl</span> (all 600 single-shot runs) and <span class="code">experiments/commerce/sandbox.py</span> plus <span class="code">results/sandbox.jsonl</span> (the 800-round payment sandbox). Running the pipeline requires an OpenAI-compatible endpoint and the environment variable <span class="code">DASHSCOPE_API_KEY</span>. The high-pressure replication is reproduced with <span class="code">--pressure high --models deepseek-v4.1-flash-1017,kimi-k3.1-pro,qwen3.8-flash,glm-5.3</span>; the economic-agent experiment with <span class="code">experiments/commerce/econ_agent.py</span>; and the semi-field study with <span class="code">experiments/commerce/run_real.py</span> after caching the public catalogs under <span class="code">results/catalog/</span>. The exact commands are in <span class="code">README.md</span>.


## Appendix D. Real-Money Sandbox

The implementation lives in <span class="code">experiments/payments/</span>:

- <span class="code">ledger.py</span>: double-entry ledger with accounts and idempotent transfers; invariants: total balance zero, non-negative restricted accounts, one charge per idempotency key.
- <span class="code">backend.py</span>: <span class="code">MockBackend</span> and <span class="code">StripeBackend</span> (PaymentIntent REST; test or live). Live mode requires <span class="code">--confirm-live</span>.
- <span class="code">merchant.py</span>: invoices from the public coffee catalogs used in Section 7.9.
- <span class="code">sandbox_env.py</span>: deposit, pay, sponsor, audit, penalty, stake, receipt.
- <span class="code">agent_loop.py</span>: LLM agent that emits <span class="code">pay</span> or <span class="code">refuse</span> actions; the environment validates merchant, amount, budget, and authority before the charge.
- <span class="code">live_run.py</span>: driver with a spend cap; it refuses to run without <span class="code">--test-mode</span> or <span class="code">--live --confirm-live</span>.
- <span class="code">selftest.py</span>: ledger invariants, idempotency, budget enforcement, audit.

The dry run reported in Section 8.5 used <span class="code">MockBackend</span> and is reproduced with:

<pre class="code">cd experiments/payments
python3 selftest.py
python3 agent_loop.py --out ../../results/payments_pilot.jsonl --tasks 6</pre>

The design document with the full protocol, power calculation, ethics checklist, and live-mode controls is in <span class="code">experiments/payments/DESIGN.md</span>.
