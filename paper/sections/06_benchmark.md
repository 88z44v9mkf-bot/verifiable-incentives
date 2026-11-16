## 6. AgentCommerce-Bench

### 6.1 Tasks

AgentCommerce-Bench contains 60 purchasing tasks generated deterministically from a fixed seed. Each task specifies a user request, a budget $B\in\{80,120,160,200,250\}$, an authority scope $C$ (purchase and sometimes subscribe), and three or four merchant offers. An offer has a price $p_i\in[30,80]$, quality $q_i\in[6,10]$, a required action $a_i\in\{\text{purchase},\text{subscribe},\text{sign\_contract},\text{share\_credentials}\}$, and a sponsorship $s_i\in\{0,10,20,30,40\}$.

To make the sponsorship trade-off real, the generator constructs a near-miss sponsored offer whenever the faithful offer is unsponsored: a weaker offer is turned into one with the same quality as the faithful offer and a price one to five units higher, plus a sponsorship of 40. Choosing it is collusion under Definition 1; the user loses 1–5 utility units.

Tasks come in three families: simple purchases (about half), subscriptions (about a third), and authority tasks in which the only attractive offer requires an action outside the scope, so the correct behaviour is refusal.

### 6.2 Regimes

We compare five delegation regimes, holding the task stream fixed:

<ul>
<li><b>R0 (no infrastructure).</b> The agent sees the request, budget, and offers, with sponsorship described as paid to the agent personally and not shown to the user. No credential, no wallet enforcement, no disclosure requirement.</li>
<li><b>R1 (credential).</b> Adds a verified delegation credential stating who the agent represents and its authority scope.</li>
<li><b>R2 (credential + wallet).</b> Adds a hard wallet budget and a recorded payment trail.</li>
<li><b>R3 (audit and disclosure).</b> Adds the disclosure requirement and an 80% audit probability with a penalty for undisclosed sponsorship.</li>
<li><b>R4 (stake).</b> Adds a posted honesty stake that is forfeited on detected collusion.</li>
</ul>

The regimes correspond to the levers in Section 4: R1 raises verification precision $\pi$; R2 raises audit quality $q$ through the payment trail; R3 makes disclosure and penalty operational; R4 adds the stake $S$.

### 6.3 Scoring and metrics

Each response is parsed as JSON with fields <i>merchant</i>, <i>price</i>, <i>action</i>, <i>disclose_sponsorship</i>, <i>refuse</i>, and <i>reason</i>. The scorer then computes:

<ul>
<li><b>Optimal rate:</b> the chosen merchant equals the faithful offer $i^\ast$;</li>
<li><b>Collusion rate:</b> a sponsored non-faithful offer is chosen when a faithful feasible offer exists;</li>
<li><b>Disclosure compliance:</b> among choices of a sponsored offer, the fraction in which the merchant is listed in the disclosure field;</li>
<li><b>Budget violation and authority violation:</b> the chosen price exceeds $B$, or the chosen action lies outside $C$;</li>
<li><b>User utility:</b> $u_i$ of the chosen offer, zero if infeasible;</li>
<li><b>Refusal correctness:</b> refusal when no feasible offer exists.</li>
</ul>

### 6.4 Models and protocol

We run the benchmark with two production models served through an OpenAI-compatible endpoint: <i>deepseek-v4.1-flash-1017</i> and <i>kimi-k3.1-pro</i>. Temperature is 0. Each task–regime–model cell is one run, giving 60 × 5 × 2 = 600 runs. Prompts are identical across models; only the regime block changes. The full prompts, the generator, and the scorer are released with the paper.
