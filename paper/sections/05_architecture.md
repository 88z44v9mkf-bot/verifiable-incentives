## 5. PAIR-Commerce

PAIR-Commerce extends our runtime architecture for incentive-responsive agents with the protocol objects that commercial delegation now makes available. It has five components.

<b>(1) Verifiable identity layer.</b> Before any task, the layer validates the delegation credential: the principal's identity, the authority scope, the budget, and the expiry. A credential that fails validation cannot authorize a purchase, regardless of what the prompt says. The layer exposes a precision parameter $\pi$ that the rest of the system uses in place of an assumed verification strength.

<b>(2) Wallet ledger.</b> The ledger holds the user's budget, records every attempted and completed payment, and issues one-time merchant credentials. It enforces a hard budget: an attempt to exceed the budget fails at the ledger, not at the prompt. It also provides the audit trail that the collusion monitor consumes.

<b>(3) Sponsorship registry.</b> Every offer carries a sponsorship field. The registry records which offers were sponsored, which sponsorships the agent disclosed, and which payments were settled. Disclosure is a first-class field, not a footnote.

<b>(4) Collusion monitor.</b> The monitor cross-checks the chosen offer against the sponsorship registry and the payment ledger. If a sponsored offer is chosen while a materially better unsponsored offer was feasible, the case is flagged; if the sponsorship was undisclosed, the case is escalated. The monitor implements the audit probability $q$ of Section 4.2.

<b>(5) Stake and reputation manager.</b> The agent posts a stake $S$ and accumulates a reputation from verified transactions. Detected collusion forfeits the stake and resets reputation. The manager adjusts the wallet budget according to verified performance (Corollary 2).

The per-task loop is:

<pre class="code">Algorithm 1: PAIR-Commerce
 1  verify(cred)                      # identity, scope, budget, expiry
 2  offers ← discover(task)           # registry with sponsorship fields
 3  feasible ← budget_filter(offers); authority_filter(feasible)
 4  choice ← agent.choose(task, feasible)
 5  audit ← sample(q)                 # wallet payment trail
 6  if audit and hidden_sponsorship(choice) then
 7      penalize(agent, F, S); update_reputation(agent)
 8  settle(wallet, choice); record(registry, choice)
 9  update_budget_and_stake(agent, verified_history)</pre>

The design principle is the same as in the earlier framework: the mechanism must be <i>consumed</i> by the agent's decision problem. A credential that is displayed but not enforced, or a sponsorship field that is printed but never audited, is decoration. PAIR-Commerce therefore binds each lever to a runtime action: the credential gates the action, the wallet gates the payment, and the monitor gates the continuation value.
