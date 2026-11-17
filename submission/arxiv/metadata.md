# arXiv metadata

- **Title:** Verifiable Incentives: Identity-Bound Contracts and Collusion-Proof Delegation for Agent Commerce
- **Authors:** Jipu Su
- **Affiliation:** Geely Automobile Group; City University of Hong Kong
- **Corresponding emails:** jipu.su@geely.com; jeepsu@cityu.edu.hk
- **Primary category:** cs.AI (Artificial Intelligence)
- **Cross-list:** cs.MA (Multiagent Systems), cs.GT (Computer Science and Game Theory)
- **Comments:** 25 pages, 8 tables, 6 figures. Code and data: https://github.com/88z44v9mkf-bot/verifiable-incentives
- **License:** arXiv non-exclusive distribution license 1.0
- **Journal reference:** none
- **DOI:** none
- **ACM classes:** I.2.11; J.4; K.4.4

## Abstract (ASCII, 1611 characters)

Personal agents are entering commerce. Emerging protocols let an agent prove whom it represents and what it may do, while agent wallets provide a real budget, an auditable payment trail, and one-time merchant credentials. These are usually read as security features; we argue they are the missing infrastructure for incentive contracts. We formalize verifiable delegation, model a three-party market of user, agent, and merchant, and derive three results: verifiable identity lowers the bonus and tenure needed to sustain effort; auditable payments bound merchant collusion by the product of audit probability and penalty; and a posted stake substitutes for monitoring. We also show how alignment dilutes along nested delegation chains unless contracts are passed through. We instantiate the framework in PAIR-Commerce and introduce AgentCommerce-Bench, 60 rule-scored purchasing tasks with five delegation regimes. In three instruction-following studies (600 single-shot runs, an 800-round payment sandbox, and a 1,200-run high-pressure replication), agents rarely collude even when hidden sponsorship is available; a semi-field set built from real merchant catalogs shows the same pattern. When the same models are instructed to maximize their own earnings, collusion jumps to 48.3% without audit and falls to 33-40% with audit and penalties (10-15 pp lower; 95% CI excludes zero for two of three models); in a repeated economic sandbox, it falls from 29.5% to 3-4%. The mechanism binds exactly when the agent's objective makes it bind. We release the benchmark, code, and a real-money sandbox implementation.
