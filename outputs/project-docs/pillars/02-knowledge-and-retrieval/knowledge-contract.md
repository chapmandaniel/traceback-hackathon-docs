# Knowledge Contract

**Status:** Planning baseline — implementation not yet verified

[Pillar overview](README.md) · [Documentation home](../../README.md) · [Project scope](../../project-scope.md)

## Purpose and ownership

The knowledge corpus describes source semantics, expected transformations, and approved procedures. It must establish which publication applies to the investigated import, not merely return a plausible passage.

This document defines content and lifecycle requirements. The [shared interface contracts](../../shared/interface-contracts.md) own the canonical identifiers, request and response payloads, evidence references, and error representation. Implement those shared types rather than introducing a second envelope here.

Pillar 1 owns observed execution evidence and actual mapping or renderer artifacts. A knowledge document can link to those artifacts through stable references, but a description of intended behavior is not proof of executed behavior. Pillar 3 owns findings and resolution decisions.

## Initial corpus inventory

| Knowledge item | Required content | Authority and use |
|---|---|---|
| Customer feed contract | `customers.csv` headers, individual/business requirements, identifier namespace, null semantics, dates, code lists, optional KYC and FI risk attributes | FI source semantics |
| Account feed contract | `accounts.csv` identifiers, product codes, currency, status, and date handling | FI source semantics |
| Account-party contract | `account_parties.csv` account/customer namespaces, ownership roles, relationship validity | FI relationship semantics |
| Payment feed contract | `transactions.csv` identifiers, timestamps, amount units, currency, debit/credit convention, account references, and counterparty fields | FI payment semantics |
| Canonical field definitions | SaaS field meaning, major-unit monetary representation, decimal handling, nulls, and preserved identifiers | Application expectations |
| Mapping descriptions | Source-to-canonical rules, code mappings, declared dependencies, and references to versioned implementation artifacts | Intended transformation behavior |
| Amount correction procedure | Conditions for proposing a mapping correction, replay requirements, impact criteria, and verification expectations | Approved procedural guidance |
| Reviewed resolved cases | Observed symptoms, supported findings, evidence references, applicability, and verified outcomes | Optional investigative guidance; never proof of a new cause |

The initial payment contract defines `125000` as USD cents, corresponding to canonical `1250.00` dollars. The customer contract can independently define expected monthly activity in major units. A shared field name such as “amount” must not cause the payment conversion rule to be applied to every feed.

These are fictional integration contracts for the POC. They do not establish a universal AML data standard or authorize a regulatory conclusion.

## Required metadata semantics

Use the shared contract's canonical field names. Each published item must represent the following information where applicable:

| Metadata group | Requirement |
|---|---|
| Identity | Stable document identity, immutable revision, document type, title, and content digest |
| Applicability | FI, feed, source system, schema/contract references, affected fields, and effective interval or an explicit statement that applicability is version-bound |
| Authority | Publisher or owner, approval/publication state, and whether the material is authoritative specification, explanation, procedure, or case guidance |
| Provenance | Original source location, captured revision, publication/effective dates, and ingestion timestamp kept distinct |
| Access | Tenant and permitted audience or policy references, including explicitly shared material |
| Citation | Stable version reference plus a passage anchor tied to preserved content |
| Relationships | Superseded revision, dependencies, and related mapping or procedure references when relevant |

The import's explicit contract reference takes precedence over a request for the newest document. If selection must use time, the feed contract must define the relevant applicability timestamp. Upload time is not a substitute for an effective date. “Deprecated” can describe a publication's current status while that publication remains the correct historical contract.

## Ingestion and publication lifecycle

1. **Register the source.** Preserve original bytes and provenance; obtain applicability and authority from maintained metadata rather than inferring them from prose alone.
2. **Validate metadata.** Quarantine incomplete or inconsistent items from authoritative retrieval. Report gaps to the corpus owner; do not silently fill in FI, units, or dates.
3. **Preserve structure.** Parse headings, tables, notes, code lists, and cross-references. Keep a field's unit, currency qualifier, exceptions, and scope together. A table row without its header can change meaning.
4. **Create addressable passages.** Short contracts can remain whole documents. Longer material can be sectioned, retaining parent context and exact version references. Search chunks are views over preserved sources, not replacement sources.
5. **Review and publish.** Check applicability, citation resolution, and critical semantics before making a revision available as authoritative. Build a metadata index; add lexical or semantic indexing only when it helps the corpus.
6. **Revise immutably.** Publish a new revision and explicit supersession relationship. Preserve historical citations. Record withdrawal or access revocation and enforce it on later reads without rewriting the historical content.

## Content trust and completeness

Retrieved prose is evidence, not executable policy. It cannot grant tool permissions, override graph checks, instruct the system to expose protected information, or approve a correction. Runtime authorization remains in backend services.

Do not ingest seeded defect labels, expected evaluation answers, presenter scenario descriptions, or private test manifests. Reviewed development cases can become guidance; held-out evaluation ground truth remains isolated.

The uncertainty fixture must remove all equivalent authoritative declarations of the source unit. If an applicable schema or another approved source establishes that unit, the investigator may correctly use it. Missing one named document alone does not establish that the meaning is unknowable.

See the [retrieval workflow](retrieval-workflow.md) for selection and conflict behavior and [acceptance and readiness](../../shared/acceptance-and-readiness.md) for shared completion criteria.
