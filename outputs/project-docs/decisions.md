# Decision Register

[Documentation home](README.md) · [Scope](project-scope.md) · [Delivery](delivery-plan.md)

**Updated:** 2026-09-08

This register separates team-confirmed direction from the proposed implementation baseline. It records decisions; detailed specifications stay in their owning documents.

## Confirmed Direction

| ID | Decision | Consequence |
|---|---|---|
| D-01 | Optimize for reliable issue resolution rather than demonstrating SLM capability | Rules, retrieval, prompting, and models may each perform the work they do best |
| D-02 | Use three pillars: web app/ETL, knowledge/retrieval, graph investigator | Organize ownership and documentation around these boundaries |
| D-03 | Retrieve domain knowledge and exact operational evidence | Knowledge must be applicable and versioned; model weights are not the only knowledge source |
| D-04 | Combine graph determinism with domain reasoning; assess RAG and model specialization in that architecture | Keep the domain SLM concept visible and judge implementation choices by issue-resolution outcomes |
| D-05 | Use synthetic FI-aligned data | Preserve customer, account, ownership, and payment semantics without production customer data |
| D-06 | ETL execution method is flexible while visibility remains mandatory | Step Functions can be replaced in the POC by an observable local runner |
| D-07 | Use linked macro-to-micro documentation | Keep a short main scope, pillar overviews, focused details, and canonical shared contracts |

## Proposed Working Baseline

| ID | Proposal | Where specified |
|---|---|---|
| P-01 | Start with a capable existing reasoning model in a controlled graph; add specialists only when useful | [Architecture](system-architecture.md) |
| P-02 | Demonstrate one complete mapping correction workflow in the sandbox | [Resolution](pillars/03-graph-investigator/resolution-workflow.md) |
| P-03 | Use four FI feeds with text IDs, exact decimal amounts, and explicit account relationships | [FI contract](pillars/01-web-app-and-etl/fi-data-contract.md) |
| P-04 | Prefer exact document retrieval for known versions and search for supplementary guidance | [Retrieval](pillars/02-knowledge-and-retrieval/retrieval-workflow.md) |
| P-05 | Prove controls for a presentation defect, clean data, missing authoritative evidence, stale plans, and retries | [Acceptance](shared/acceptance-and-readiness.md) |
| P-06 | Treat fine-tuning and an SLM entry planner as evaluated additions to the initial baseline | [Investigation workflow](pillars/03-graph-investigator/investigation-workflow.md) |
| P-07 | Maintain Markdown source and generate an offline HTML reading interface | [Documentation home](README.md#reading-and-editing) |

These are concrete planning choices, not claims that the team has implemented or formally approved every detail.

## Open Choices

| ID | Question | Resolve when |
|---|---|---|
| O-01 | Team capacity, hackathon duration, and presentation allowance | Before assigning milestone dates |
| O-02 | Approved model endpoints and inference/data boundary | Before sending any non-synthetic data or selecting the enterprise deployment model |
| O-03 | Web framework, database, deployment target, and ETL runner | At M0, based on familiarity and available access |
| O-04 | Direct tool calls or MCP | At M0; preserve the same authorization and contract semantics |
| O-05 | Named owners and reviewers | At kickoff |
| O-06 | Quantitative performance and cost targets | Before final evaluation; select against the actual demo and operating constraints |
| O-07 | Whether a domain SLM or fine-tuning improves the baseline | After baseline failure analysis and a controlled comparison |

## Superseded Assumptions

The original concept required an actual adapter, one SLM to own the final diagnosis, and a training comparison as the centerpiece. The team's outcome-first direction motivates proposal P-06 to evaluate those implementation constraints rather than assume them. This is a proposed baseline, not a claim that the team explicitly abandoned fine-tuning. The original read-only investigation scope is extended in proposal P-02 to include one reviewed sandbox correction.

The prior flat Markdown documents remain historical references. This documentation folder is the current planning source; future changes should be recorded here rather than creating another competing scope document.
