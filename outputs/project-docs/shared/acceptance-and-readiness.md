# Acceptance and Readiness

[Documentation home](../README.md) · [Scope](../project-scope.md) · [Delivery](../delivery-plan.md) · [Interfaces](interface-contracts.md)

**Status:** Planned criteria. All implementation checks below are unverified.

This document is the authoritative home for completion criteria. Pillar documents explain how to meet them; the delivery plan references their IDs. Record the artifact/run proving each criterion when implementation exists.

## AC-01

**Realistic synthetic FI data — Pillar 1**

- [ ] Import the four linked feeds with individual/business profiles, separate accounts, joint holders, and external counterparties.
- [ ] Preserve text identifiers, namespaces, date/timestamp distinctions, exact decimal money, and unknown optional values.
- [ ] Demonstrate that joint-account joins do not duplicate transaction totals.

Proof: generator/configuration version, retained source package, loaded records, and relationship checks. See the [FI contract](../pillars/01-web-app-and-etl/fi-data-contract.md).

## AC-02

**Actual execution evidence — Pillar 1**

- [ ] Trace a selected value through raw source, stage inputs/outputs, applied logic, load, and presentation.
- [ ] Persist run/stage identities, order, timestamps, outcomes, and versioned artifacts after execution.
- [ ] Presentation evidence includes the actual input, displayed output, and inspectable formatting logic from the same captured context.

Proof: a reproducible evidence bundle and working UI links. See [ETL and lineage](../pillars/01-web-app-and-etl/etl-and-lineage.md).

## AC-03

**Applicable and authorized knowledge — Pillar 2**

- [ ] Retrieve the exact FI/feed/version required by a historical import, even when a newer document exists.
- [ ] Reject or explicitly surface wrong-scope, missing, and conflicting authoritative knowledge.
- [ ] Keep equivalent authoritative information available when legitimate; do not require an inconclusive answer simply because one document is absent.
- [ ] Enforce access before returning content or sensitive existence details.

Proof: retrieval cases, selected document/version references, and negative-scope tests. See the [retrieval workflow](../pillars/02-knowledge-and-retrieval/retrieval-workflow.md).

## AC-04

**Grounded, bounded investigation — Pillar 3**

- [ ] Run a real reasoning model with actual evidence access, applicable knowledge, and deterministic checks.
- [ ] Include at least one reserved case in which the model makes a meaningful investigation contribution: selects a discriminating evidence lookup, reconciles conflicting observations, or revises a hypothesis. Capture that observable contribution; paraphrasing a rule's final answer alone is insufficient. Keep deterministic exits for cases already settled by code.
- [ ] Support additional lookups or revised hypotheses within graph limits.
- [ ] Findings cite supporting observations and distinguish missing or contradictory evidence.
- [ ] Model output and retrieved/source text cannot grant permissions or bypass checks.
- [ ] Known deterministic diagnoses are permitted; private scenario labels never enter the investigator.

Proof: complete investigation trace, model/prompt/tool versions, cited artifacts, and boundary tests. See the [investigation workflow](../pillars/03-graph-investigator/investigation-workflow.md).

## AC-05

**Different causes and uncertainty controls — All pillars**

- [ ] Diagnose an executable amount-conversion defect and an executable presentation defect producing the same visible amount discrepancy.
- [ ] Preserve a clean-record control without inventing a defect.
- [ ] Return an unresolved finding when source-unit meaning is genuinely unavailable from all trustworthy sources.
- [ ] Do not propose ETL reprocessing as the remedy for correctly stored data with a presentation error.

Proof: reserved scenario definitions in the private evaluator, observed evidence, and scored findings. The core mapping fixture should include a faulty EFT conversion path and correctly processed WIRE controls in the same batch.

## AC-06

**Correct impact — Pillars 1 and 3**

- [ ] Execute a bounded defect predicate over actual records and applied configuration.
- [ ] Distinguish confirmed affected records from records that merely share a batch or mapping.
- [ ] Match the known affected set and preserve its immutable reference in the plan.

Proof: predicate/query version, input snapshot, actual result set, and precision/recall against private fixture truth. No model-estimated counts.

## AC-07

**Real correction preview — Pillars 1 and 3**

- [ ] Validate one typed repair against the permitted action catalog.
- [ ] Reprocess retained source inputs into an isolated candidate using the proposed configuration.
- [ ] Show actual before/after differences for affected records and unchanged results for WIRE/clean controls.
- [ ] Record semantic, identity, relationship, and relevant amount checks. A failed preview cannot progress to approval.

Proof: candidate snapshot, configuration hash, replay receipt, diff, and check results. A replay that only patches the displayed value does not satisfy this criterion.

## AC-08

**Concrete approval and stale-plan handling — Pillars 1 and 3**

- [ ] Bind an authorized review decision to the exact plan hash and previewed artifacts.
- [ ] Reject unauthorized approval/application using lightweight server-issued fixture roles; a full login UI is not required.
- [ ] Change a target/configuration revision after review and demonstrate that application is blocked until the plan is regenerated and reviewed.
- [ ] Restrict effects to the designated sandbox target.

Proof: approval record, negative authorization cases, stale-state test, and execution denial. See [interface contracts](interface-contracts.md).

## AC-09

**Retry and interruption recovery — Pillars 1 and 3**

- [ ] Persist graph state and execution identity across interruption or refresh.
- [ ] Repeated application of the same operation does not duplicate effects.
- [ ] Simulate a lost response after a possible write; reconcile the operation ledger and active target before retrying or claiming success.
- [ ] Reject a reused operation key with a different plan.

Proof: retry/failure-injection traces, execution ledger entries, and authoritative state. A frontend-disabled button alone is insufficient.

## AC-10

**Verified closure — Pillars 1 and 3**

- [ ] Read the active sandbox state after application and compare it with the reviewed candidate.
- [ ] Verify corrected values, expected identities/relationships, and preservation of unaffected controls.
- [ ] Refresh the application and show the corrected display from the verified state.
- [ ] Keep preview success, application acknowledgment, and verified resolution distinct. Failed verification remains open or escalates.

Proof: post-application observations and final status with evidence references.

## AC-11

**Outcome-first evaluation — Shared responsibility**

- [ ] Reserve meaningful scenario variants before final tuning; keep their answers out of prompts, RAG documents, model training, and tools.
- [ ] Measure diagnosis support, impact accuracy, correction appropriateness, clean-record preservation, uncertainty, latency, and operator effort.
- [ ] Separate retrieval failures from reasoning failures using controlled evidence cases when needed.
- [ ] Compare optional model or fine-tuning changes against the existing baseline using equivalent available evidence, actions, and declared budgets; report all model/tool work.

An initial 12–20 incident evaluation is a planning target for the hackathon, not proof of broad generalization. Report counts and denominators; repeat representative runs to expose variability. Fix operating thresholds before the final evaluation and record them in [decisions](../decisions.md).

Proof: scenario split, configuration versions, raw outcomes, and a short results report. No specific model or adapter is required to win.

## AC-12

**Complete and inspectable demonstration — Shared responsibility**

- [ ] Run the full supported correction path with real data, retrieval, reasoning, replay, review, application, and verification.
- [ ] Reset fixtures and repeat the presentation on the actual demo setup.
- [ ] Open citations and navigate source-to-screen evidence without losing investigation context.
- [ ] Clearly label any development stub, recorded segment, or unavailable dependency; do not count it as live verified behavior.

Proof: rehearsed demonstration and retained run references. Demo script: [delivery plan](../delivery-plan.md#proposed-demonstration).

## Enterprise Readiness Beyond the POC

Passing the synthetic scope is a bounded product demonstration. Production readiness additionally needs evidence for real FI integration and schema variation; enterprise identity and tenant isolation; approved inference and data residency; retention and audit policy; load/concurrency and failure recovery; monitoring, support and incident response; and downstream effects of corrections.

Where downstream AML calculations or alerts depend on corrected data, the production design must identify which outputs require recalculation or an explicit stale state. The hackathon does not implement a full AML engine.

These are follow-on acceptance areas, not completed capabilities. Keep planned, implemented, tested, and production-approved status separate.
