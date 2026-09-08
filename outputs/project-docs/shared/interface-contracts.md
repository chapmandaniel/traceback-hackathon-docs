# Shared Interface Contracts

[Documentation home](../README.md) · [Architecture](../system-architecture.md) · [Acceptance](acceptance-and-readiness.md)

**Status:** Proposed contract baseline — implementation not yet verified.

This document owns the cross-pillar payload meanings. Pillar documents own their internal data and behavior. These are logical contracts; they do not require separate services or a specific transport.

## Common Conventions

- Use text identifiers. External identity is scoped by FI, source system, object type, and external ID. Canonical database IDs remain separate.
- Server-established actor permissions and FI scope accompany calls out of band. Model-supplied identifiers never grant access.
- Represent canonical money as exact decimal strings with currency and explicit major-unit semantics. Preserve raw source text separately.
- Distinguish observed timestamps, source update timestamps, ingestion timestamps, and date-only fields.
- Every immutable artifact has an ID, version or revision, content hash, and resolvable reference. Historical artifacts remain available to authorized investigations.
- Payload schema versions are separate from FI contract versions, mapping versions, and model versions.
- Missing values are explicit. Citation existence, document relevance, and causal support are separate checks.
- Trace IDs correlate activity; operation IDs identify effects. A trace ID is not an idempotency mechanism.
- Keep three objects distinct: the immutable source/reference fixture, the active sandbox target serving the app, and the isolated replay candidate awaiting review. Application promotes the reviewed candidate and mapping revision into the active target.

## Contract Ownership

| Contract | Producer | Consumer | Purpose |
|---|---|---|---|
| `InvestigationContext` | Pillar 1 / authenticated application | Pillar 3 | Establish the selected record and reproducible observation |
| `EvidenceItem` | Pillar 1 or deterministic check service | Pillar 3 and UI | Supply actual observations with provenance |
| `KnowledgeItem` | Pillar 2 | Pillar 3 and UI | Supply applicable domain assertions and citations |
| `Finding` | Pillar 3 | UI, evaluator, and resolution planning | State the supported result or remaining uncertainty |
| `ResolutionPlan` | Pillar 3, validated by execution service | Reviewer and Pillar 1 executor | Describe the exact proposed and previewed change |
| `ExecutionReceipt` | Pillar 1 executor | Pillar 3 and UI | Record the actual effect and subsequent verification |

## InvestigationContext

Minimum fields:

| Field | Meaning |
|---|---|
| `investigation_id`, `schema_version` | Stable investigation identity and payload version |
| `fi_id`, `record_ref`, `field_path` | Authorized target; record reference includes its source identity |
| `user_question` | User-supplied question, treated as input rather than authority |
| `snapshot_id`, `import_run_id` | Immutable operational context for the original observation |
| `presentation_capture_id` | Captured display, API input, renderer version, and formatting-logic reference |
| `observed_value` | Value/type/currency/unit as actually displayed, including original text |
| `source_refs`, `configuration_refs` | Available source, contract, mapping, and renderer identities; absent references remain explicit |

The backend captures or validates the record/display relationship. A user-entered expected value is a reported expectation, not automatically the correct answer.

## EvidenceItem

Each item contains `evidence_id`, `schema_version`, `fi_id`, `kind`, `snapshot_id`, relevant record/run/stage references, `observed_at`, `content_hash`, a resolvable artifact reference, and a bounded payload.

Useful kinds include `source_record`, `stage_observation`, `applied_mapping`, `validation_result`, `link_result`, `load_result`, `presentation_capture`, and `deterministic_check`.

Field observations retain raw/canonical values, types, currencies, and unit provenance. A unit declared by a source contract differs from a unit assumed by a mapping. A deterministic check must name its rule/version and input evidence; it may report a verified rule violation but must not read the private scenario answer.

Lineage links include all contributing records for joins. A summary is not a replacement for the resolvable underlying artifact.

## KnowledgeItem

Minimum metadata:

| Field | Meaning |
|---|---|
| `document_id`, `version`, `section_id` | Stable exact citation identity |
| `fi_id`, `source_system`, `feed_id` | Applicability scope; shared documents must explicitly declare their permitted scope |
| `effective_from`, `effective_to` | Declared temporal applicability, where relevant |
| `authority`, `publication_status` | Contract, mapping documentation, approved procedure, or case guidance; draft/approved/superseded lifecycle |
| `content_hash`, `artifact_ref`, `text` | Immutable source identity and the returned passage |
| `retrieval_method`, `selection_basis` | Exact reference, metadata match, or search; why it was selected |
| `access_scope_ref` | Policy reference enforced by the retrieval service |

A superseded document can remain the correct description of a historical import. A currently approved repair procedure is a separate selection from the historic source contract. Lifecycle status alone must not silently replace the version referenced by the import.

Knowledge responses use `found`, `missing`, `conflicting`, or `not_authorized`, with items and unresolved applicability details where permitted. Relevance scores are not authority scores. User-facing errors must not reveal inaccessible document contents or existence.

Corpus rules and retrieval behavior are owned by [Pillar 2](../pillars/02-knowledge-and-retrieval/README.md).

## Finding

The finding contains `finding_id`, `investigation_id`, `status`, `summary`, applicable stage/cause, supporting evidence/document references, contradictory observations, missing information, and proposed next actions.

`Finding.status` is one of:

- `supported`: The stated finding is supported by specified evidence/checks. This does not mean a repair has been applied.
- `no_supported_discrepancy`: Available evidence supports the observed value or does not establish the reported discrepancy; explain the basis and limits.
- `inconclusive`: Required meaning or evidence remains unresolved.

The investigation lifecycle is separate: `received`, `running`, `needs_input`, `completed`, or `failed`. A completed investigation can have an inconclusive finding.

## ResolutionPlan

A plan names `plan_id`, `plan_revision`, `investigation_id`, `finding_id`, and the current state. The application validates a proposed typed action against the repair catalog before replay or execution.

The plan must bind:

- FI, target sandbox/environment, action type, and validated parameters.
- Retained source snapshot/package hashes and the currently active target revision.
- Current and candidate mapping/configuration versions and content hashes.
- The supported defect predicate, its query/version, and the exact affected-record set or immutable set reference.
- Candidate replay identity, before/after diff artifact, clean-control set, and invariant-check results.
- The approval policy and a `plan_hash` over the concrete reviewable content above.

Use a canonical serialization for hashing. State labels and the approval record itself are not part of the immutable content they reference. Any change to reviewed inputs, target revision, configuration, affected scope, or preview artifacts produces a new hash and invalidates prior approval.

An approval is a separate attributable record containing the authorized actor, decision, timestamp, and exact `plan_hash`. The executor rechecks current permissions and state before applying it. Model text such as “approved” has no authority.

Plan states are:

`draft` → `previewing` → `preview_passed` → `awaiting_approval` → `approved` → `applying` → `applied_pending_verification` → `verified`.

Other outcomes are `preview_failed`, `stale`, `rejected`, `failed`, and `outcome_unknown`. Rejected, stale, or changed plans require a new valid review path; a failed preview does not progress to approval.

The [resolution workflow](../pillars/03-graph-investigator/resolution-workflow.md) defines the transition conditions.

## ExecutionReceipt

The executor returns `operation_id`, `plan_hash`, target identity, prior/activated revisions, observed execution status, timestamps, result artifact references, and error/reconciliation details.

For the proposed sandbox, application can atomically activate the reviewed candidate snapshot and matching mapping revision. It must check the expected prior revision and maintain an operation ledger. Repeating the same operation returns its recorded outcome; a mismatched plan under the same key is rejected.

If a response is lost after a possible effect, record `outcome_unknown` and inspect the ledger and authoritative target before retrying. Graph checkpointing alone does not make writes exactly-once.

Verification reads the authoritative active target and records observed values, record-set checks, and invariants against the reviewed preview. Only that evidence permits `verified`. A successful request or a passed preview is insufficient.

## Independent Development and Contract Changes

Each pillar can provide development stubs matching these meanings, clearly labeled as stubs. The core acceptance run must use real operational records, retrieval, model calls, replay, and execution receipts.

When a field meaning or transition changes, update this document first, then the producer, consumers, and linked [acceptance criteria](acceptance-and-readiness.md). Transport-specific schemas and endpoints can be generated from the implementation later; do not create a second competing definition here.
