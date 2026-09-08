# ETL and Lineage

**Status:** Planning baseline — implementation not yet verified

[Pillar overview](README.md) · [Project home](../../README.md) · [FI data contract](fi-data-contract.md) · [Web experience](web-experience.md)

## Purpose and execution choice

Run real transformations and preserve enough evidence to diagnose and correct their business effects. The organization's ETL uses AWS Step Functions. This POC may use named local stages, Step Functions, or another familiar runner; visibility and reproducibility are mandatory.

The investigator graph coordinates resolution; the ETL runner processes data. Integrate them through the [shared interface contracts](../../shared/interface-contracts.md).

## Processing stages

Execute **Landing → Validation → Normalization → Linking → Load**, then render loaded records in the application.

| Stage | Work and evidence retained |
|---|---|
| Landing | Original file bytes, checksum, manifest, run identity, and logical row references |
| Validation | Schema/code/required-field checks, duplicate findings, accepted or rejected rows, and reasons |
| Normalization | Actual input/output values, types, units, applicable code mappings, and inspectable executed logic/version |
| Linking | Exact account/customer resolution, all contributing records, and unresolved references |
| Load | Accepted/skipped/rejected counts, canonical records, and source-to-loaded links |
| Presentation | Captured selected value, API input and database value, renderer version, and actual formatting logic/configuration |

Record stage order, timing, status, errors, and retries when they occur. A green stage means its execution completed. Semantic mistakes can survive validation and load.

Preserve monetary values as exact major-unit decimals in the canonical store and as decimal strings at API boundaries. Source values, inferred or declared units, timestamps, and configuration provenance remain distinguishable. Retain rejected rows; unresolved references never trigger guessed relationships. The [FI contract](fi-data-contract.md) owns field and parsing semantics.

## Storage and evidence ownership

Use a small relational store for customers, accounts, holders, and transactions, with immutable raw/stage artifacts in files or database records. Retain import runs, stage executions, source records, lineage, evidence, configuration versions, and investigation outputs.

Lineage connects source rows through intermediate values and join inputs to canonical records. Captured presentation evidence also binds the application view to the inspected stored result. Customer/account context needs provenance, not just transaction amounts.

Publish contracts and mapping artifacts to the knowledge pillar using canonical references. Tools return observations rather than hidden defect labels or completed root-cause answers. Reprocessing produces new evidence; it never overwrites evidence cited by an earlier investigation. Missing artifacts are recorded as unavailable. Cross-pillar payload schemas belong exclusively to the [shared contract](../../shared/interface-contracts.md).

## Executable fixtures

| Fixture | Implementation and boundary |
|---|---|
| Mapping defect | A real payment mapping omits cents-to-dollars conversion on its EFT branch while WIRE conversion remains correct. The bad branch affects every matching record, never a hard-coded transaction ID. |
| Presentation defect | Correct stored/API `1250.00` becomes displayed `125000.00` through actual versioned formatting logic. Diagnosis only; no mapping change. |
| Clean control | Applicable contract, mapping, stored value, and rendering agree. |
| Unknown control | The applicable source-unit contract and equivalent authoritative declarations are unavailable. Mapping behavior alone does not prove source meaning. |

Keep ground truth and scenario labels in the private fixture/evaluation harness. Each scenario uses an isolated namespace and retained source snapshot. The mapping fixture includes EFT and WIRE records so the replay must prove both correction and preservation of unaffected data.

## Controlled mapping resolution

**Impact.** Evaluate the established defect condition against the actual run, applied mapping branch, source records, and loaded results. Return checked scope and exact matching records. Distinguish confirmed matches from unexamined scope; do not label every record sharing a mapping as affected.

**Preview.** Accept a typed, supported mapping correction through the shared contract. Validate the target, allowed parameter change, source snapshot, and configuration versions. Re-execute the retained four-file package into an isolated candidate snapshot with the proposed mapping. Do not call a calculated mock difference a replay.

Compare candidate and active records using stable identities. Check exact amounts against the applicable contract, direction/currency preservation, relationship integrity, uniqueness, row accounting, and unchanged records outside the defect condition. Retain executed logic, stage observations, detailed differences, and failed checks alongside the candidate.

**Review and apply.** Bind the reviewed artifact to its candidate, correction, input hashes, record scope, and current active state. Before application, the server rechecks authority and those preconditions. Stale state or failed checks stop application. The graph's approval resumes the controlled service; a model cannot bypass its checks.

Prefer atomically activating the reviewed candidate snapshot and mapping revision in one database transaction. The application then uses exactly the previewed result. Retain the previous snapshot. Use the shared operation identity so retries return the same outcome rather than applying twice.

**Verify.** Re-read the active dataset through the application's authoritative path, compare it with the approved candidate, and rerun the relevant invariants. Persist a verified or unresolved outcome. Define explicit handling for failure after activation; retaining an old snapshot alone does not establish that recovery works.

## Replay and operational boundaries

A corrected successful import requires a new reprocessing execution over retained inputs. AWS redrive resumes unsuccessful Standard executions using the original definition; it does not rerun successful processing under a changed definition. [AWS redrive documentation](https://docs.aws.amazon.com/step-functions/latest/dg/redrive-executions.html)

Fixture reset must not destroy evidence for the active presentation. Start a fresh namespace when resetting and retain completed runs until intentionally cleaned up. This is a synthetic sandbox correction, with no payment execution or production FI writes. Recalculation of downstream AML alerts is deferred because those modules are absent.

Use [canonical acceptance and readiness](../../shared/acceptance-and-readiness.md) for required checks and the [delivery plan](../../delivery-plan.md) for sequencing.
