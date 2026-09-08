# Pillar 1 — Web Application and Observable ETL

**Status:** Planning baseline — implementation not yet verified

[Project home](../../README.md) · [Project scope](../../project-scope.md) · [System architecture](../../system-architecture.md)

## Purpose

Build the credible product and executable data journey that Traceback investigates and corrects. A fictional financial institution supplies realistic customer, account, relationship, and payment records to a small AML data workspace. Every displayed value remains traceable to retained source data and actual processing evidence.

The principal experience is: **question a transaction amount → investigate → establish impact → preview a mapping correction → approve → apply to the sandbox → verify**. The application investigates data correctness; it does not determine whether activity constitutes money laundering.

## Documents

| Document | Owns |
|---|---|
| [FI data contract](fi-data-contract.md) | Four source files, customer and payment semantics, identifiers, canonical mappings, and synthetic examples |
| [Web experience](web-experience.md) | Transaction journey, supporting views, evidence inspection, and correction review |
| [ETL and lineage](etl-and-lineage.md) | Executable stages, retained observations, impact calculation, isolated replay, and sandbox application |

## Delivery boundary

This pillar owns the application, fixture generation, processing runner, evidence capture, and deterministic preview/application/verification services. The knowledge pillar makes applicable contracts and configuration evidence retrievable. The investigator pillar coordinates the resolution workflow and interprets observations.

Use an existing capable model initially. Model specialization is an optional, evidence-led choice; this pillar must function independently of model selection.

AWS Step Functions is optional. Execution visibility, record lineage, and inspectable applied logic are mandatory. Implement one complete mapping-correction family; retain the display defect as diagnosis only and include clean and insufficient-evidence controls.

## Shared contracts and readiness

Cross-pillar requests, evidence references, correction artifacts, and results are defined in [interface contracts](../../shared/interface-contracts.md). Use the canonical [acceptance and readiness criteria](../../shared/acceptance-and-readiness.md), [delivery plan](../../delivery-plan.md), and [decision record](../../decisions.md).
