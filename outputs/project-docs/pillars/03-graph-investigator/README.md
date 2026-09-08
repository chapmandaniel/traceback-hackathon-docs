# Pillar 3 — Graph Investigator and Resolution

**Status:** Planning baseline — implementation not yet verified

[Project home](../../README.md) · [Project scope](../../project-scope.md) · [System architecture](../../system-architecture.md)

This pillar turns a questionable application value into a supported finding and, for the supported mapping defect, a tested and approved sandbox repair. LangGraph coordinates the work; deterministic code owns evidence access, calculations, policies, and state transitions. An existing capable reasoning model investigates questions that the available checks do not settle.

Version-aware knowledge retrieval is required. The investigator must connect authoritative FI contracts and mapping guidance with exact source records, executed transformations, and presentation evidence. A fine-tuned domain SLM or SLM entry planner is an optional optimization, adopted only when comparison with the baseline establishes useful improvement. A second model is not a required stage.

The core resolution journey is **evidence → cause → impact → typed correction plan → isolated replay → concrete approval → sandbox application → verification**. The proposed fixture repairs an EFT mapping branch that omitted cents-to-major-unit conversion while preserving correctly processed WIRE records. Presentation defects receive a supported diagnosis and handoff; arbitrary application-code repair remains outside this pillar.

Read the detailed workflows in order:

1. [Investigation workflow](investigation-workflow.md): evidence collection, knowledge retrieval, reasoning, uncertainty, and finding production.
2. [Resolution workflow](resolution-workflow.md): repair eligibility, impact, replay, approval, execution, and verification.

The [shared interface contracts](../../shared/interface-contracts.md) own payload schemas and exact status values. The [acceptance and readiness document](../../shared/acceptance-and-readiness.md) owns acceptance identifiers and verification evidence. These documents describe behavior without creating competing contracts.

Use the [delivery plan](../../delivery-plan.md) for sequencing and the [decision register](../../decisions.md) for changes to scope. The visible finish is a verified target state, rather than a model answer or successful replay alone.
