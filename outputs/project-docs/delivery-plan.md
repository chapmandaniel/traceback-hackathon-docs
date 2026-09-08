# Delivery Plan

[Documentation home](README.md) · [Scope](project-scope.md) · [Acceptance criteria](shared/acceptance-and-readiness.md)

**Status:** Proposed milestone plan. Team size, duration, owners, and dates are not yet assigned.

## Build by Dependency

| Milestone | Deliverable | Completion evidence |
|---|---|---|
| M0 — Align contracts and runtime | Confirm the four FI feeds, shared interfaces, model endpoint feasibility, and document applicability rules | Sample payloads reviewed; model and tool smoke path runs; open choices recorded |
| M1 — Establish evidence and knowledge | Import clean synthetic records; retain source/stage evidence; retrieve their exact contracts | [AC-01](shared/acceptance-and-readiness.md#ac-01), [AC-02](shared/acceptance-and-readiness.md#ac-02), [AC-03](shared/acceptance-and-readiness.md#ac-03) |
| M2 — Complete an investigation | Transaction screen, actual model/tool loop, findings, and clickable evidence | [AC-04](shared/acceptance-and-readiness.md#ac-04), [AC-05](shared/acceptance-and-readiness.md#ac-05) |
| M3 — Prove a correction | Actual impact query, typed plan, isolated replay, and before/after comparison | [AC-06](shared/acceptance-and-readiness.md#ac-06), [AC-07](shared/acceptance-and-readiness.md#ac-07) |
| M4 — Control application and closure | Concrete review, sandbox application, stale-plan handling, retry recovery, and authoritative verification | [AC-08](shared/acceptance-and-readiness.md#ac-08), [AC-09](shared/acceptance-and-readiness.md#ac-09), [AC-10](shared/acceptance-and-readiness.md#ac-10) |
| M5 — Evaluate and rehearse | Reserved-case results, resettable fixtures, polished evidence journey, and a timed demo | [AC-11](shared/acceptance-and-readiness.md#ac-11), [AC-12](shared/acceptance-and-readiness.md#ac-12) |

Only documentation has been created so far in this workspace. These milestones are not marked complete.

## Parallel Workstreams

- **Pillar 1 owner:** FI data and web/ETL evidence; implement operational replay and sandbox application services.
- **Pillar 2 owner:** Versioned corpus, retrieval, applicability checks, and knowledge citations.
- **Pillar 3 owner:** Investigation graph, model interaction, findings, and resolution control flow.
- **Integration responsibility:** One named team member coordinates the shared interfaces, scenario harness, and acceptance results. This is a role, not a fourth product pillar.

Start Pillar 2 from the same versioned FI contract that Pillar 1 implements. Pillar 3 can develop against labeled development stubs, but the demonstration and acceptance results must use real services and model calls.

## Proposed Demonstration

1. Show a completed import and a questioned amount of USD 125,000.00.
2. Investigate the value using actual operational evidence and the applicable FI contract.
3. Identify the faulty conversion path and calculate the records that satisfy its defect condition.
4. Preview a typed correction over retained source data, showing changed records and unchanged controls.
5. Review the concrete plan, apply it to the sandbox, and verify the corrected record and preserved controls.
6. Briefly show that the same visible symptom caused by presentation receives a different diagnosis and does not trigger an ETL repair.

Keep clean and genuinely ambiguous cases in the evaluation even if presentation time does not allow showing all of them live. Set the demo duration after the event allowance and actual latency are known.

## Optional Work, Ordered by Observed Need

1. Improve a measured retrieval, reasoning, or usability weakness.
2. Add a missing-relationship incident using the existing account identifiers.
3. Evaluate a domain SLM, alternative planner, or fine-tuning against the established baseline.
4. Add verified-resolution capture for a future knowledge or training update.

Do not add a model stage merely to satisfy the original SLM-centered concept. Record any measured reason for a new stage in [decisions](decisions.md).

## Change and Handoff Rules

When a change alters the product commitment, update [scope](project-scope.md) and the decision register. When it alters a payload or execution condition, update the [shared contract](shared/interface-contracts.md), its consumers, and the linked acceptance criteria together.

Before handoff, verify local links, example consistency, and documentation status. Store actual evaluation and operational proof under an implementation-owned results location when those artifacts exist; do not fabricate result placeholders as if checks have passed.
