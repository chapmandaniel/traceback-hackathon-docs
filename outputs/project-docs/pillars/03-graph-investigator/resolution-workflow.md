# Resolution Workflow

**Status:** Planning baseline — implementation not yet verified

[Pillar overview](README.md) · [Project home](../../README.md) · [Previous: investigation workflow](investigation-workflow.md) · [Project scope](../../project-scope.md)

## Supported repair and authority

Complete one repair family: correct an EFT mapping branch that omitted the documented conversion from cents to decimal major units. Preserve the correctly functioning WIRE branch. This is a typed mapping correction executed by application code; arbitrary code generation, production deployment, and presentation-code repair are outside the core workflow.

Apply only to the plan's designated active sandbox target. Keep the immutable source/reference fixture, active sandbox target, and isolated replay candidate distinct. Preserve the source fixture and historical evidence throughout.

The [shared interface contracts](../../shared/interface-contracts.md) define `Finding`, `ResolutionPlan`, `ExecutionReceipt`, fingerprints, and exact statuses. This document specifies their behavior. A model can recommend a plan. Only the configured application policy and an authorized sandbox operator can authorize its execution. Retrieved text, logs, and model output cannot supply that authorization.

## 1. Establish eligibility and actual impact

Require a supported finding, the applicable authoritative unit contract, inspectable executed mapping, an identified sandbox target, and complete enough lineage to select affected records. Missing source semantics or an unsupported repair family ends in an explicit unresolved result or handoff.

Calculate impact with an exact predicate: the relevant FI/feed, executed mapping version, EFT branch, source-unit conditions, and approved dataset scope. Sharing a mapping version alone establishes potential exposure. Report confirmed matches separately from records whose status remains unknown.

The correction targets qualifying EFT records. It must not divide every amount in the batch or modify correctly normalized WIRE payments. If impact cannot be bounded adequately, do not advance to an executable plan.

## 2. Build a concrete typed plan

Create a candidate mapping version and `ResolutionPlan` under the shared contract. Bind the plan to its target, repair scope, evidence and contract versions, input artifacts, and expected starting state. Preserve the original mapping and import evidence.

The plan states the specific conversion change, affected population, expected result, and checks that must pass. Use exact decimal arithmetic. The model may help explain the proposal; code validates that the typed action belongs to the supported family and that its preconditions hold.

A successful import containing wrong business data requires a new execution with the corrected mapping. Retrying the old successful run with the old mapping reproduces the defect.

## 3. Replay in isolation

Execute the candidate against an isolated copy of the bound input and target state. Replay must run real transformation and load logic without modifying the active sandbox dataset.

Compare the result against the plan: qualifying EFT amounts convert correctly; WIRE controls and other out-of-scope records remain unchanged; identifiers, currencies, relationships, and row counts remain consistent; no duplicate postings are introduced. Preserve replay evidence and result hashes.

Use `preview_passed` only when the required checks pass. A failed or incomplete replay cannot advance to approval. Passing replay establishes the tested candidate's behavior, not application to the active target.

## 4. Obtain approval bound to that result

Present the actual correction, target, affected records, representative before/after values, replay results, and material limitations. The operator approves this concrete plan through the application.

Bind approval to `plan_hash` and its tested dependencies as defined in the shared contract. A change to the mapping, scope, input, authoritative contract, replay result, or target starting state invalidates the old approval. Display `stale` and require an updated replay and approval for the changed plan.

Validate the actor and approval on the backend. Immediately before writing, recheck preconditions and use a transactional comparison or equivalent guard so a target change between checking and applying cannot silently reuse approval.

## 5. Apply once and reconcile uncertainty

Execute the approved action through a controlled sandbox runner using a stable idempotency identity bound to the plan. Reject reuse of that identity with different content. Record durable operation progress and receipts, and ensure target writes also enforce the operation identity; an in-memory flag is insufficient.

The proposed baseline atomically activates the reviewed replay candidate and its tested mapping revision in the active sandbox. Application is a separately recorded promotion operation, not a second transformation run. Require the bound target revision and all reviewed dependencies to remain valid; otherwise mark the plan stale. Preserve the previous run and investigation evidence.

If a request times out or a response is lost, use `outcome_unknown`. Inspect the operation ledger, mapping state, run identity, and target records before retrying. A confirmed committed operation advances to verification. A provably unstarted operation may resume with the same identity. An indeterminate or partial outcome remains blocked from blind reapplication until reconciled. Do not mark an uncertain write failed merely to enable a new attempt.

## 6. Verify the active target

Read the sandbox target after application. Confirm the active mapping, repaired EFT values, preserved controls, expected record population, and absence of duplicate application. A successful command response is insufficient.

Only these reads and passing checks permit `verified`. Keep replay success, awaiting approval, stale approval, application in progress, unknown outcome, applied-but-unverified, and verified distinct using canonical statuses. Verification failure preserves the observed state and failure evidence; it does not imply automatic rollback or successful resolution.

## Completion evidence

Show the finding, confirmed impact, plan fingerprint, isolated replay, concrete approval, execution receipt, and final target observations as one traceable journey. A display fault ends with diagnosis and handoff rather than entering this repair path.

The [shared acceptance and readiness criteria](../../shared/acceptance-and-readiness.md) own required verification identifiers. Implementation sequencing belongs in the [delivery plan](../../delivery-plan.md); changes to supported repair authority belong in [decisions](../../decisions.md). Until implemented and checked, this remains a proposed hackathon workflow.
