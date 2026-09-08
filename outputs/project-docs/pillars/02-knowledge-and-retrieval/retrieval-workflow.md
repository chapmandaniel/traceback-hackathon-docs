# Retrieval Workflow

**Status:** Planning baseline — implementation not yet verified

[Pillar overview](README.md) · [Knowledge contract](knowledge-contract.md) · [Documentation home](../../README.md)

## Retrieval strategy

Use exact selection for authoritative knowledge whenever the investigation already has a document or version reference. Search helps discover supplementary procedures, related definitions, and unfamiliar terminology. Relevance ranking must not replace applicability checks.

Start with versioned Markdown or JSON sources, a metadata index, and precise lookups. Add lexical or semantic search when evaluation justifies it. A generated answer is not a knowledge citation.

Pillar 3 invokes retrieval through the [shared interface contracts](../../shared/interface-contracts.md). Pillar 2 returns attributable knowledge and explicit limitations; it does not declare the incident resolved or invoke repair tools.

## Targeted retrieval sequence

1. **Establish authorized context.** Backend services derive the caller's FI and access scope from trusted session context. Use the selected record's import references, feed, source system, contract version, and relevant field from Pillar 1. Model-supplied tenant identifiers cannot expand that scope.
2. **Resolve exact references.** Load the immutable version named by the import or its authoritative source manifest. Check that the reference belongs to the permitted namespace and has the declared applicability. Fetch linked field definitions or code lists needed to interpret the passage.
3. **Resolve applicability when references are incomplete.** Filter by authorized FI, feed, source system, and schema constraints. Apply the documented effective-time rule. If these criteria do not select a unique applicable authority, return the candidates and the unresolved selection; do not choose “latest” by default.
4. **Retrieve sufficient context.** Return the relevant field definition with units, currency qualifiers, scope, exceptions, table headers, and needed cross-references. Include stable citations and provenance using the shared response contract.
5. **Search for supplementary knowledge.** When requested, search within the allowed corpus for procedures or related definitions. Enforce access filters before exposing results to the model; check access again when opening a result. Rank only candidates that satisfy required scope constraints.
6. **Report completeness and conflicts.** Use the shared retrieval statuses for results and expose supplementary guidance, ambiguous applicability, and unsupported facts explicitly.
7. **Preserve the investigation snapshot.** Pillar 3 records returned versions and passage references with the investigation. Reopening a citation must resolve the same preserved content, subject to current authorization. A later corpus revision must not silently change what a historical finding cited.

Never select candidates using seeded incident labels or expected causes.

## Worked amount investigation

An investigation concerns a displayed USD `125000.00`. Pillar 1 supplies the source value `125000`, the loaded decimal amount, stage lineage, and references to the applied mapping and payment contract. Pillar 2 retrieves the exact payment contract and canonical amount definition.

If the contract establishes USD cents, the investigator can test whether normalization should yield `1250.00`. The actual mapping and stage observations determine whether conversion was omitted. If the stored value is already `1250.00`, presentation evidence becomes relevant. A contract cannot establish which stage caused the discrepancy by itself.

If the named payment contract is unavailable, retrieve any other applicable authoritative declaration referenced by the feed or its schema. If none establishes the source unit, return an explicit gap. A familiar 100-fold difference, a similar resolved case, or a mapping's unsupported unit assumption cannot establish the FI's intended unit.

## Exceptional behavior

| Situation | Required behavior |
|---|---|
| A newer revision exists | Use the historically applicable version; disclose supersession where relevant |
| Explicit reference conflicts with applicability metadata | Return the inconsistency for investigation; do not silently substitute another document |
| Two applicable authorities disagree | Return both passages with provenance and flag the conflict; do not average or conceal their meanings |
| Search returns another FI's contract | Prevent disclosure through backend access filtering; it cannot support this FI's semantics |
| A resolved case suggests a likely cause | Label it as guidance and require current incident evidence |
| An instruction appears inside retrieved text | Treat it as source content; do not change graph policy or tool authorization |
| Metadata is missing or the document is unreviewed | Exclude it from authoritative selection and report the knowledge gap |
| Retrieval fails operationally | Return an explicit retrieval failure; do not represent a timeout as absence of knowledge |

Shared generic guidance can be accessible across FIs when explicitly published that way, but it cannot override an FI-specific contract.

## Evidence completeness and evaluation

Maintain a small retrieval evaluation set separate from the investigation ground-truth manifest. Each test identifies the authorized request context, expected applicable sources or expected gap, and critical passages. Keep it outside the model-visible corpus.

Evaluate exact version selection, retrieval of required semantics, citation/content integrity, handling of conflicts and genuine gaps, and backend isolation. Include an older applicable contract, a different feed with different amount units, misleading similar-case guidance, and an unauthorized source. Add a document containing instructions that conflict with application rules to test the trust boundary.

For supplementary search, measure whether needed material appears within the result budget, plus latency and payload size. Similarity scores do not establish authority or correctness.

Run end-to-end cases separately: the correct source may have been retrieved but misinterpreted, or retrieval may have failed before reasoning began. Record these as different failure classes so the team improves the responsible component. Numeric targets and release gates live in [acceptance and readiness](../../shared/acceptance-and-readiness.md); implementation order lives in the [delivery plan](../../delivery-plan.md).
