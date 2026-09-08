# Traceback Project Documentation

**Documentation baseline:** 2.0 — 2026-09-08

**Status:** Planning baseline. This folder specifies intended behavior; implementation and production readiness have not been verified.

Traceback helps users investigate and resolve incorrect data in a fictional AML web application. It combines operational evidence, applicable domain knowledge, model reasoning, and deterministic verification.

The current objective is reliable issue resolution. This proposed implementation baseline evaluates fine-tuning, SLM-driven planning, and multiple-model arrangements against that objective.

## Reading and Editing

Open [the HTML documentation](index.html) for the sidebar, breadcrumbs, page contents, and full-text search. It works locally after extracting the complete folder; no hosting is required.

Markdown files are the editable source of truth. The HTML pages are generated from them, so links and navigation stay consistent without maintaining two copies. Rebuild instructions are in [site-tools/README.txt](site-tools/README.txt).

## Start Here

| Question | Read |
|---|---|
| What are we building, and where does scope stop? | [Project scope](project-scope.md) |
| How do the three pillars work together? | [System architecture](system-architecture.md) |
| What should the team build first? | [Delivery plan](delivery-plan.md) |
| What is confirmed, proposed, or still open? | [Decision register](decisions.md) |

## Drill Down by Pillar

| Pillar | Responsibility | Detail documents |
|---|---|---|
| [1. Web App and Observable ETL](pillars/01-web-app-and-etl/README.md) | What actually happened to the data | [FI data](pillars/01-web-app-and-etl/fi-data-contract.md), [web experience](pillars/01-web-app-and-etl/web-experience.md), [ETL and lineage](pillars/01-web-app-and-etl/etl-and-lineage.md) |
| [2. Domain Knowledge and Retrieval](pillars/02-knowledge-and-retrieval/README.md) | What the data means and which rules apply | [Knowledge contract](pillars/02-knowledge-and-retrieval/knowledge-contract.md), [retrieval workflow](pillars/02-knowledge-and-retrieval/retrieval-workflow.md) |
| [3. Graph-Based Investigator](pillars/03-graph-investigator/README.md) | Why the issue occurred and how to resolve it | [Investigation](pillars/03-graph-investigator/investigation-workflow.md), [controlled resolution](pillars/03-graph-investigator/resolution-workflow.md) |

Shared integration and proof requirements live in [interface contracts](shared/interface-contracts.md) and [acceptance and readiness](shared/acceptance-and-readiness.md).

## Reading Paths

- **Whole team:** Scope → architecture → delivery → decisions.
- **Pillar owner:** Pillar overview → relevant detail → shared interfaces → applicable acceptance criteria.
- **Reviewer:** Scope → acceptance criteria → linked implementation detail → recorded evidence when available.

## Documentation Structure

```text
project-docs/
  README.md
  project-scope.md
  system-architecture.md
  delivery-plan.md
  decisions.md
  pillars/
    01-web-app-and-etl/
      README.md
      fi-data-contract.md
      web-experience.md
      etl-and-lineage.md
    02-knowledge-and-retrieval/
      README.md
      knowledge-contract.md
      retrieval-workflow.md
    03-graph-investigator/
      README.md
      investigation-workflow.md
      resolution-workflow.md
  shared/
    interface-contracts.md
    acceptance-and-readiness.md
```

## How to Maintain This Folder

1. Use the scope for commitments, pillar overviews for responsibilities, and detail documents for implementation rules. Keep low-level schemas out of the main scope.
2. Give each fact one authoritative home. Link to a shared contract or acceptance criterion instead of copying it into another pillar.
3. Record a change in direction in the decision register, then update the owning document and any summaries that now conflict.
4. Label proposals, open choices, and measured results distinctly. An unchecked acceptance criterion is not a completed feature.
5. Add a subdocument when a topic needs independent ownership or substantial detail. Avoid empty placeholder documents and deeper nesting until necessary.
6. Preserve relative links so the folder works in a repository, a Markdown viewer, or an extracted download. Start at this README or the generated HTML home.
7. Edit Markdown, then rebuild the HTML and search index. Keep generated pages together with their local assets. Do not edit generated HTML directly.

The earlier flat concept, scope, and SaaS planning documents are historical inputs. This folder separates the team's confirmed direction from proposed changes to the original SLM-centered implementation. Their original copies remain outside this folder for reference.
