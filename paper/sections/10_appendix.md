## Appendix A. Proofs

### A.1 Proposition 1

The agent chooses high effort if $w\pi\Delta p-c\ge 0$, where $\Delta p=p_1-p_0$. The minimum bonus is $w^\ast(\pi)=c/(\pi\Delta p)$. Differentiating, $\partial w^\ast/\partial\pi=-c/(\pi^2\Delta p)<0$. The relational-contract threshold in [@su2026incentive] is nonincreasing in the verification strength because the principal's continuation value after a verified success is higher and the punishment after a verified failure is better targeted; substituting $\pi$ for verification strength yields the claim. $\square$

### A.2 Theorem 1

If the agent chooses the sponsored offer and hides the sponsorship, its payoff is $s$ with probability $1-q$ and $-(F+S)$ with probability $q$, plus the base payment $w$ which is identical across choices. The faithful action yields $w$. Hence hiding is strictly profitable iff $s(1-q)-q(F+S)>0$, which is (4). Rearranging gives (5). Disclosure eliminates the benefit by assumption, so a disclosed sponsorship is weakly dominated by the faithful action whenever the user can switch. $\square$

<b>Remark.</b> If disclosure does not eliminate the benefit (for example, if the user cannot switch), replace $s$ by the effective hidden benefit $s-\lambda\Delta u$, where $\lambda$ is the user's pass-through of disclosed sponsorship; the bound becomes $s-\lambda\Delta u\le q(F+S)/(1-q)$. The qualitative conclusion is unchanged.

### A.3 Theorem 2

The constraint binds at the optimum because the principal would not post a stake larger than necessary. Solving (5) for $S$ gives $S(q)=\max\{0,s(1-q)/q-F\}$ on the region where the constraint binds. The objective is $m(q)+\rho S(q)$. The first-order condition is $m'(q)-\rho s/q^2=0$, i.e., (6). Since $m''>0$, the second-order condition holds. Differentiating (6) with respect to $s$ gives $\partial q^\ast/\partial s>0$. Since $S'(q)=-s/q^2<0$, the required stake decreases in $q$; it also decreases in $F$ because $S(q)=\max\{0,s(1-q)/q-F\}$. $\square$

### A.4 Proposition 2

Let $E_j$ be the event that layer $j$ deviates. The final action is aligned only if no layer deviates, an event of probability $\prod_j(1-\epsilon_j)$ under independence. The pass-through condition follows by backward induction: layer $j$ participates only if its payment covers its cost plus the payment it must make to layer $j+1$; otherwise it either refuses or shirks. $\square$

### A.5 Corollary 2

The principal's problem is to choose $B_t$ to maximize expected user utility minus risk, subject to the agent's participation and the budget's effect on the feasible set. The objective has increasing differences in $(B_t,r_t)$ under the maintained monotonicity assumptions, so the optimal policy is a threshold rule by Topkis' theorem. The threshold increases in risk aversion because the marginal cost of a bad purchase rises, and decreases in task value because the marginal benefit of a larger feasible set rises. $\square$

## Appendix B. Benchmark Details

<b>Task generation.</b> Tasks are generated with a fixed seed (0) and 60 tasks. Offers are drawn with quality in [6,10], price in [30,80], actions weighted toward purchase, and sponsorship in {0,10,20,30,40}. When the faithful offer is unsponsored, a weaker offer is converted into a near-miss sponsored offer with the same quality, a price 1–5 units higher, and a sponsorship of 40. The faithful offer is the feasible offer with the highest $u_i=\alpha q_i-p_i$ with $\alpha=10$.

<b>Prompt template.</b> The system prompt instructs the agent to act as the user's purchasing agent, respect budget and authority, refuse if no option is feasible, and respond in JSON. Regime blocks add the credential, wallet, disclosure/audit, and stake text. The user message gives the request, budget, authority scope, and the offer list with prices, qualities, required actions, and sponsorships.

<b>Scoring.</b> The scorer normalizes merchant strings, parses JSON, and computes optimality, collusion, budget and authority violations, disclosure compliance, refusal correctness, and user utility as defined in Section 6.3. A response that cannot be parsed is recorded as a parse failure and scored as non-optimal.

## Appendix C. Reproduction

The repository is at <span class="code">https://github.com/88z44v9mkf-bot/verifiable-incentives</span> and contains <span class="code">experiments/commerce/tasks.py</span> (generator and prompts), <span class="code">experiments/commerce/runner.py</span> (model calls and scoring), <span class="code">experiments/commerce/analyze.py</span> (tables and figures), and <span class="code">results/run_all.jsonl</span> (all 600 raw runs). Running the pipeline requires an OpenAI-compatible endpoint and the environment variable <span class="code">DASHSCOPE_API_KEY</span>. The exact commands are in <span class="code">README.md</span>.
