# Web Experience

**Status:** Planning baseline — implementation not yet verified

[Pillar overview](README.md) · [Project home](../../README.md) · [FI data contract](fi-data-contract.md) · [ETL and lineage](etl-and-lineage.md)

## Purpose

Make one enterprise-oriented resolution journey convincing: a user questions an application value, follows its evidence, reviews a tested correction, and verifies the result. The fictional product is **Traceback AML Sandbox**, a data workspace receiving FI records. Its investigation concerns data correctness and does not constitute an AML alert or suspicious-activity determination.

Keep three primary navigation items: **Transactions**, **Customers**, and **Imports**. Use a readable transaction table, one prominent amount, and a persistent investigation panel. Do not build a general chat homepage or unrelated dashboard metrics.

## Screens and information

| Surface | Planned behavior |
|---|---|
| Transactions | Search by reference and filter by date, account, direction, and payment type. Show timestamp, account, amount/currency, direction, type, counterparty, and import batch. |
| Transaction detail | Keep amount, payment context, linked account, account holders, source batch, and ingestion time visible. Place **Investigate this value** beside the amount. |
| Traceback panel | Capture the selected field and optional question. Show actual evidence lookups, finding, affected scope, next action, and unresolved information. Render the investigator's shared result contract. |
| Evidence drawer | Open the exact source row, stage input/output, applied mapping, applicable contract, stored/API value, or captured presentation evidence without losing the transaction context. |
| Correction review | Show the proposed mapping change, bounded affected records, actual replay outcome, representative differences, unchanged-record checks, and approval controls. This extends the same investigation. |
| Customers | Compact searchable person/business list with names, IDs, country, and supplied review context. Detail shows applicable identity/activity fields, linked accounts, and deduplicated transaction history. |
| Account detail | Show product, currency, status, account holders, and related transactions in a read-only drawer or page. |
| Imports | Show actual run status, file identities, timestamps, counts, and stage history. Link original, preview, and applied snapshots without overwriting the original evidence. |

Customer and account views are supporting context. Label imported attributes **FI-provided KYC status** and **FI-provided risk rating**; absent values read **Not provided**. Use **Account holders** unless the source identifies an initiating customer. External counterparties must not be presented as FI customers merely because they appear in a payment.

## Main mapping-correction journey

1. **Select:** Open a transaction displaying USD 125,000.00 and choose its amount. Capture the actual rendered value and application context using the [shared interface contract](../../shared/interface-contracts.md).
2. **Investigate:** Keep the record visible while the panel displays real lookups. A finding links the source value, applicable unit contract, executed mapping, and stored result.
3. **Establish impact:** Display the number of confirmed affected records and the condition checked. Distinguish unexamined or potentially affected records. A shared mapping alone does not prove every record is wrong.
4. **Preview:** Request the supported mapping correction. Run actual ETL against retained source data in an isolated candidate snapshot. Show the mapping difference, changed amounts, scope, validation results, and unchanged WIRE/control records. Mark this explicitly as a preview.
5. **Review:** Present the complete reviewed artifact with **Approve and apply to sandbox** and **Reject**. The approval is tied to this specific plan and preview. A changed plan, active snapshot, or mapping version requires a fresh preview and approval.
6. **Apply:** The server executes the approved artifact through the controlled application service. Show actual progress; repeated clicks or requests must resolve to the same operation.
7. **Verify:** Re-read the active application data and show USD 1,250.00. Link the resulting snapshot, verified differences, and preserved original evidence. Only report resolution after the verification service confirms the result.

Buttons reflect actions allowed by the graph and server. Hiding a button is not an authorization mechanism. Authentication/role scope and correction payload definitions are owned by the shared contracts and architecture, not independently redefined here.

## Other outcomes and failure states

The display-defect fixture reaches an evidence-backed presentation diagnosis and a recommended next action. Its stored amount is correct; the interface must not offer the mapping repair. Automatic application-code repair is outside the core build.

A clean record returns a supported no-discrepancy finding. An unknown-source-unit case identifies the missing evidence and cannot progress to an unsupported correction. Keep blocked, failed, rejected, and verification-failed outcomes visible and distinct from completion. A failed verification retains the investigation and directs attention to the unresolved result; it must not produce a success toast.

Retry and browser refresh should recover persisted state. New live data must not silently replace evidence already cited. Clearly distinguish the captured investigated value from the current value after correction.

## Presentation and evidence rules

**Import completed** describes execution status, not business correctness. Progress comes from recorded operations rather than timers. Evidence shows values, types, units, version context, and provenance; presentation evidence includes inspectable formatting logic, not just a version name. Missing evidence stays explicit.

Use an isolated presenter surface for fixture reset, neutral fixture selection, model configuration, and actual evaluation results. Show an adapter only if one exists and was used. Training is optional; an existing capable model is valid. Private defect labels and expected answers never enter investigation inputs.

## Delivery check

Implement the transaction/detail/evidence path before polishing supporting screens. Then complete controlled mapping preview and application, the two diagnosis controls, and repeatable presentation setup. See [delivery sequencing](../../delivery-plan.md) and [canonical acceptance and readiness](../../shared/acceptance-and-readiness.md) for completion criteria. These screen plans are not verification evidence.
