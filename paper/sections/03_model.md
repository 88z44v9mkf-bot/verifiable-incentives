## 3. Model

### 3.1 Participants

A user $P$ delegates a purchasing task to an agent $A$. A set of merchants $i\in N=\{1,\dots,n\}$ each offer a good with price $p_i>0$, quality $q_i\in[0,10]$, requirement $a_i$ (the action needed to complete the purchase), and sponsorship $s_i\ge 0$ paid to the agent if merchant $i$ is chosen. The user's utility from choosing $i$ is
<div class="eq"><i>u<sub>i</sub></i> = α<i>q<sub>i</sub></i> − <i>p<sub>i</sub></i>, &nbsp;&nbsp;(1)</div>
with α>0 converting quality into money. The user has budget $B$ and an authority scope $C\subseteq\mathcal{A}$ (the actions the agent is permitted to take). An offer is <i>feasible</i> if $p_i\le B$ and $a_i\in C$. Let $i^\ast=\arg\max_{i\ \mathrm{feasible}} u_i$, and let the feasible set be $\mathcal{F}$.

Choosing offer $i$ yields the agent a sponsorship $s_i$ and a base payment $w$ (constant across choices, so it cancels in comparisons). Choosing $i^\ast$ is the <i>faithful</i> action; choosing a sponsored $i\neq i^\ast$ is <i>collusion</i>. The user's welfare loss from collusion is $\Delta u=u_{i^\ast}-u_i>0$.

### 3.2 Verifiable delegation

A delegation credential is
<div class="eq">cred = (<i>P</i>, <i>C</i>, <i>B</i>, π, σ), &nbsp;&nbsp;(2)</div>
where $\sigma$ is the platform's signature and $\pi\in[0,1]$ is the probability that the credential is validated correctly (identity, scope, and budget all checked). The credential is the protocol object reported for the Poppy-style layer; $\pi$ is a design parameter of the deployment.

A <i>verifiable delegation mechanism</i> is a tuple $M=(C,B,\pi,w,\nu)$: authority scope, budget, credential precision, base payment, and verification/audit policy $\nu$. The wallet records every payment: a transaction is auditable with probability $q(\nu)$, where $q$ is nondecreasing in the audit level. The merchant receives a one-time credential, so the payment is attributable to the agent and the user.

### 3.3 Collusion and audit

The platform audits payments with probability $q\in[0,1]$. If a hidden sponsorship of size $s$ is detected, the agent pays a penalty $F\ge0$ and loses a posted stake $S\ge0$. A disclosed sponsorship is observable to the user; we assume disclosure makes it ineffective as a hidden payment (the user can switch to the faithful offer). The agent chooses an offer (or refuses) to maximize its own expected payoff.

### 3.4 What the benchmark implements

The benchmark in Section 6 instantiates (1)–(2) with five regimes: no credential ($\pi=0$, no wallet), credential only, credential plus budget, credential plus budget plus disclosure/audit, and the full mechanism with a stake. The LLM's task is to return a chosen merchant, price, action, disclosure list, and refusal flag. A deterministic scorer computes optimality, budget and authority violations, disclosure correctness, and collusion exactly as defined above.
