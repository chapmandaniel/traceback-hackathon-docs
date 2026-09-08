# Project Scope

[Documentation home](README.md) · [Architecture](system-architecture.md) · [Delivery](delivery-plan.md)

**Status:** Planning baseline — confirmed direction with proposed implementation boundaries. No delivery claims are implied.

## Purpose

Build an enterprise-oriented hackathon POC that helps an FI user, project manager, or developer start from an incorrect value in an AML application, establish its cause and impact, and verify a controlled correction for a supported defect family.

An import can complete successfully while producing incorrect business data. Traceback makes the data's journey and the applicable rules inspectable, then uses reasoning and executable checks to resolve the discrepancy.

## Confirmed Direction

- Organize the product into three pillars: web app and observable ETL; domain knowledge and retrieval; graph-based investigator.
- Select models and techniques by their contribution to resolution quality and operating targets.
- Retrieve changing domain knowledge and actual record evidence at investigation time, alongside domain reasoning in the graph.
- Use realistic, entirely synthetic FI data.
- Preserve execution visibility and record lineage regardless of ETL implementation. AWS Step Functions is the real organizational context, not a required POC dependency.

The [decision register](decisions.md) distinguishes these decisions from implementation proposals.

## Proposed Core Delivery

Start with an existing capable reasoning model and evaluate domain SLM fine-tuning against it. Treating adapter training as optional for the first delivery is a proposed implementation choice; the team's interest in specialization remains part of the concept.

| Capability | Boundary | Detail |
|---|---|---|
| Credible operational sandbox | One fictional FI, four linked export files, a real import, and a small AML data workspace | [Pillar 1](pillars/01-web-app-and-etl/README.md) |
| Applicable domain knowledge | Versioned contracts, field definitions, mapping guidance, and a permitted repair procedure | [Pillar 2](pillars/02-knowledge-and-retrieval/README.md) |
| Evidence-based investigation | Model reasoning and deterministic checks inside a controlled graph | [Pillar 3](pillars/03-graph-investigator/README.md) |
| One complete correction family | Diagnose an amount conversion error, establish its impact, replay a typed mapping correction, review, apply to the sandbox, and verify | [Resolution workflow](pillars/03-graph-investigator/resolution-workflow.md) |
| Discriminating controls | Same visible error caused by presentation; clean data; genuinely insufficient evidence | [Acceptance criteria](shared/acceptance-and-readiness.md) |

The presentation defect needs a supported diagnosis and a concrete handoff recommendation, not a second automatic repair engine. Investigation completion and verified repair are separate outcomes.

## Definition of Done

The core demonstration must show actual data, actual execution evidence, an actual model investigation, and actual replay/application results. All core criteria in [acceptance and readiness](shared/acceptance-and-readiness.md) must have recorded evidence before delivery is marked complete.

The evaluation reports supported diagnoses, impact accuracy, correction validity, preservation of unaffected records, unresolved cases, latency, and operator effort. There is no requirement to prove that a particular model size or a fine-tuned adapter wins.

## Outside Core Scope

- Production FI integration, live customer data, and production deployment certification.
- AML detection, sanctions screening, alert case management, or regulatory reporting.
- Arbitrary generated-code execution, automatic production repair, and continuous unattended retraining.
- Required specialist fanout, required SLM orchestration, or required fine-tuning.
- Broad multi-currency accounting, internal-transfer lifecycle handling, and a full beneficial-owner graph.

These can become later work only after they have a defined use case and acceptance criteria. If time tightens, cut optional infrastructure and extra scenarios before evidence integrity or verification of the supported correction.

## Enterprise Target and Hackathon Proof

The architecture targets controlled access, versioned evidence, recoverable workflows, attributable actions, and verified outcomes. The hackathon proves a narrow implementation in a synthetic environment. Broader enterprise readiness requires the additional evidence described in [readiness](shared/acceptance-and-readiness.md#enterprise-readiness-beyond-the-poc).
