# Pillar 2 — Domain Knowledge and Retrieval

**Status:** Planning baseline — implementation not yet verified

[Documentation home](../../README.md) · [Project scope](../../project-scope.md) · [System architecture](../../system-architecture.md)

## Purpose

Supply **what the data means and what should happen**: applicable FI contracts, field definitions, mapping documentation, and approved correction procedures.

The core implementation is a small, versioned corpus with precise retrieval. A vector database, embedding pipeline, and document-management interface are not required. Search can supplement exact lookups when the investigation needs broader guidance.

## Boundary

Pillar 1 owns source files, records, executed transformations, presentation behavior, and their lineage. Pillar 2 owns published knowledge and its applicability. Pillar 3 requests both, reasons over the results, and governs the investigation. A mapping description explains intended behavior; it cannot establish which code actually ran.

Start with an existing capable model using these services. Fine-tuning is a later option supported by measured weaknesses or operating benefits, rather than a dependency of this pillar.

## Core deliverables

- A reviewed corpus covering the four FI feeds and the amount-resolution workflow.
- Immutable versions, applicability metadata, and citations that reopen the exact supporting passage.
- Exact contract lookup plus optional search for supplementary guidance.
- Explicit missing, ambiguous, and conflicting-result behavior.
- Retrieval checks covering versions, permissions, citation integrity, and evidence gaps.

## Drill down

| Document | Use it to decide |
|---|---|
| [Knowledge contract](knowledge-contract.md) | What belongs in the corpus, how it is versioned, and what metadata it requires |
| [Retrieval workflow](retrieval-workflow.md) | How knowledge is selected, returned, and evaluated |
| [Shared interface contracts](../../shared/interface-contracts.md) | The canonical payloads exchanged with other pillars |
| [Acceptance and readiness](../../shared/acceptance-and-readiness.md) | The project-wide acceptance gates |

Build sequencing belongs in the [delivery plan](../../delivery-plan.md); changes to the agreed boundaries belong in the [decision record](../../decisions.md).
