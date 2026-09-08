# Investigation Workflow

**Status:** Planning baseline — implementation not yet verified

[Pillar overview](README.md) · [Project home](../../README.md) · [System architecture](../../system-architecture.md) · [Next: resolution workflow](resolution-workflow.md)

## Purpose and control boundary

Produce a supported finding from the selected application value and its actual data journey. The baseline uses an existing capable reasoning model, mandatory knowledge retrieval, exact diagnostic tools, and deterministic checks. Known checks may establish a cause directly; the graph does not manufacture reasoning work to demonstrate AI involvement.

LangGraph owns permitted transitions, tool execution, budgets, and persistence. The model may propose evidence requests and interpretations. It cannot extend its permissions, authorize a repair, or declare an unsupported result verified. This mix of code and model nodes follows LangGraph's [custom workflow pattern](https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow).

The [shared contracts](../../shared/interface-contracts.md) define `InvestigationContext`, `EvidenceItem`, `KnowledgeItem`, and `Finding`, including their exact statuses. Preserve the distinctions between a supported discrepancy, no supported discrepancy, insufficient evidence, and an execution failure.

## 1. Establish the investigation context

Application code captures the selected record and field, displayed value, FI/source namespace, relevant run references, and sandbox identity. Resolve these from trusted application state and validated requests. A user-supplied label or model-generated identifier does not establish identity or access.

Record the selected presentation observation and its renderer version. Keep the context linked to an immutable investigation snapshot so subsequent evidence cannot silently come from a newer import. A resume can reuse retained observations; a changed target requires explicit reconciliation or a fresh investigation.

## 2. Collect facts and retrieve knowledge

Gather a small factual baseline: displayed and stored values, record lineage, executed mapping references, and available source/stage observations. Parallelize independent reads where useful. Preserve exact values, types, currencies, timestamps, and provenance.

Retrieve the applicable FI contract and relevant mapping guidance. Select known documents by FI, feed, version, and effective context before using semantic retrieval for supplemental sections. RAG does not require a vector database for this small document collection. Never substitute the latest contract silently when the applied version is unavailable.

Record observations and authoritative knowledge separately. A log saying that a mapper treated a value as cents proves what the mapper did; it does not independently prove that the FI supplied cents. Retain evidence of errors and absent documents rather than inventing a complete trace.

The ambiguous control must genuinely lack enough authoritative information to settle source-unit meaning. Hiding one document is insufficient if equivalent authoritative guidance remains available elsewhere. Conversely, a missing document should not force an inconclusive result when other evidence supports the conclusion.

## 3. Run checks, then reason where needed

Code checks arithmetic, identity/link consistency, mapping predicates, and differences between observed stages. A known diagnosis is supported only when its required conditions and applicable contract are established. For example, the EFT conversion defect requires the EFT branch, authoritative minor-unit semantics, and actual stage evidence of omitted conversion.

For unresolved questions, the model considers competing explanations and proposes a permitted lookup or a finding. An amount discrepancy may originate in source semantics, normalization, loading, or presentation. A provisional focus must not make other relevant evidence inaccessible.

The graph validates requested operations and arguments before execution, then returns observations to the reasoning step. Keep a bounded opportunity to revise the investigation when new facts contradict an earlier hypothesis. Missing evidence, contradictory observations, invalid actions, and exhausted budgets are explicit conditions; the model's confidence score alone cannot settle routing or completion.

A fine-tuned domain SLM, specialist fanout, or SLM planner may be evaluated later. None is required to sit in every investigation. Introduce additional nodes only when their contribution warrants their latency, cost, and failure paths.

## 4. Produce and check the finding

The finding identifies the supported cause and location where established, its evidence, remaining uncertainty, and a useful next action. Checking that an evidence identifier exists does not prove it supports the explanation. Verify calculable claims with code and retain explicit distinctions between observations and model interpretation.

Use the canonical statuses to distinguish outcomes:

| Outcome | Meaning and next step |
|---|---|
| Supported discrepancy | Evidence establishes an issue; evaluate resolution eligibility. |
| No supported discrepancy | Available evidence agrees; do not claim universal correctness. |
| Inconclusive | Evidence cannot settle the issue; identify the missing information. |
| Failed investigation | An execution problem prevented completion; retain partial evidence and recovery context. |

Lifecycle and finding are separate: a `completed` investigation can return any defined `Finding.status`. Use `needs_input` when continuation awaits information, and `failed` for an execution failure; neither implies that the selected value is correct.

Only the supported EFT mapping family enters the [resolution workflow](resolution-workflow.md). A presentation defect receives a cited diagnosis and developer handoff. Neither tool output nor retrieved text can grant execution authority.

## Demonstration and evaluation

Demonstrate the EFT defect, the similar presentation symptom, a correct record, and a genuinely ambiguous case. Keep hidden fault labels outside records, retrieval, and model context. Compare optional model adaptations under equivalent evidence access and report actual outcomes.

Use the [shared acceptance criteria](../../shared/acceptance-and-readiness.md) for required checks and evidence; use the [delivery plan](../../delivery-plan.md) and [decisions](../../decisions.md) for implementation priorities. This workflow is a planning baseline, not a claim that those checks have passed.
