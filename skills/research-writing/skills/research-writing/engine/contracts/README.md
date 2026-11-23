# Shared contracts (strict mode)

Schema files used by the strict-mode scripts: reviewer sprint contracts, Material Passport
ports, revision patches and audit artifacts.

## Research-family workflow profiles

- `research_workflow/research_workflow_profile.schema.json`
  (`research-workflow-profile/1.0`) is the closed, manuscript-blind declaration
  of stage applicability and vocabulary. Omitted task families resolve to
  `unresolved_fit`, never to applicable. The profile embeds a SHA-256 over its
  JSON Canonical Form with `content_sha256` replaced by 64 zeroes; persisted
  profile files must themselves be exact canonical bytes.
- `research_workflow/research_workflow_profile_selection_receipt.schema.json`
  (`research-workflow-profile-selection-receipt/1.0`) records an append-only
  user selection/confirmation/fallback chain. A correction appends a new
  binding and one visible `profile_context_changed` stale mark per supplied
  prior-profile stage output. It never rewrites or removes an artifact. Newly
  introduced authority requirements remain attached to each mark with an
  explicit `authority_sensitive_reuse_gate: unmet`, so a later consumer can
  block that reuse until the applicable check passes.
- `../research_workflow_profiles/field_general.json` is the mandatory shipped
  fallback: every task family is unresolved except the field-general integrity
  gates, alternatives are unresolved, the live-branch budget is 3, and an empty
  authority list means “unknown; ask the user,” never “not required.” It ships
  with explicit English and zh-TW display names.

The standard-library runtime is `@/engine/scripts/research_workflow_profile.py`. Its
`select` command treats an omitted `--profile` as a visibly recorded automatic
fallback; an explicit profile requires `--selected-by`. `correct` consumes an
explicit prior-profile binding and stage-output inventory, then emits the new
receipt to stdout only. No command reads manuscript content, infers a family,
changes the default workflow, or writes scholar-owned artifacts. The human
usability protocol and every outcome claim remain `NOT_RUN`.

## PDF read-integrity and optional content advisory (follow-up)

- `pdf/pdf_read_preflight.schema.json` accepts the unchanged legacy structural sidecar
  or the all-or-nothing opt-in content extension. In that extension, `verdict` is
  explicitly `verdict_scope: STRUCTURE_ONLY`; `OCR_RECOMMENDED` never rewrites that
  structural value into a content claim. The schema binds the legacy shape to tool
  version 1.0.0 and the extension shape to 1.1.0.
- `pdf/pdf_content_classifier_worker.schema.json` closes the stdout of the fixed
  isolated worker to two classifications, three unavailable reasons, finite bounded
  confidence, and bounded non-negative page indexes. Runtime additionally binds every
  page to the structural page count.
- `pdf/pdf_content_classifier_diagnostic.schema.json` is the separate POSIX-only,
  local mode-`0600` operator artifact. Platforms without `fchmod` reject its CLI
  option before path creation. Its explicitly untrusted detail is capped and never
  copied into or referenced by the sidecar. File-writing CLI invocations use
  conservative NFC/casefold keys, path resolution, and existing-inode checks to reject
  aliases before worker launch; the stdout-only legacy path adds no such precondition.
  POSIX sidecar output pre-binds the parent dirfd/inode, then uses a private `0700`
  fixed-name staging directory and anchored dirfd-relative publication. Open-inode
  checks reject staging entry swaps; atomic final-entry replacement does not follow
  post-check links. Non-POSIX output fails closed; stdout classification remains
  available. The diagnostic parent is likewise dirfd-bound before the worker. These are
  instantaneous inode postconditions, not a general same-UID sandbox; callers control
  the output parent. A failed diagnostic unlinks only the no-follow leaf still matching
  its created fd inode, preserving the primary error and any attacker replacement while
  keeping its exclusive path retryable.

Runtime: `@/engine/scripts/pdf_read_preflight.py` and
`@/engine/scripts/pdf_content_classifier_worker.py`.

## Claim-standing candidate ledger (Track A)

- `claim_standing/query_plan.schema.json` (`claim-standing-query-plan/1.0`)
  binds one exact high-impact checkpoint claim, at most three accepted queries,
  at most four discovery-index identities, filters, authorized content class,
  frozen caps, and retrieval-only consent through a closed consentable-plan
  projection (version 1.1 below adds the stance-authorizable consent).
- `claim_standing/retrieval_input.schema.json`
  (`claim-standing-retrieval-input/1.0`) carries already-retained,
  adapter-neutral attempts, closed retry-authorization receipts, raw hits,
  explicit version relations, and caller-supplied relevance success/failure
  evidence bound to exact claim/candidate inputs and canonical prompt bytes.
- `claim_standing/candidate_ledger.schema.json`
  (`claim-standing-candidate-ledger/1.0`) preserves every attempt and raw-hit
terminal state while recording deterministic work-family selection.
- `claim_standing/query_plan_v1_1.schema.json`
  (`claim-standing-query-plan/1.1`) is identical to 1.0 except that the consent
  decision may be `retrieval_plus_stance`, in which case a top-level
  `stance_plan` names the exact stance provider/model surface, the consent
  binds its hash, and the authorized content classes extend by exactly
  `claim_and_selected_evidence_to_stance_provider`. A 1.0 plan stays valid
  under its own schema; the runtime validator accepts both versions and
  enforces the stance bindings only on 1.1.
- `claim_standing/transmission_ledger.schema.json`
  (`claim-standing-transmission-ledger/1.0`) accounts every event that left the
  session during one probe: retrieval-query events derived one-to-one from the
  retained attempts and stance-classification events copied verbatim from the
  stance runner's transmission records, each carrying recipient, purpose, exact
  content classes, byte count, local hash, time, consent receipt, retention
  disclosure, and result state. `@/engine/scripts/check_claim_standing_transmissions.py`
  is the normative builder/validator: an event outside the plan's authorized
  content classes or consented recipient roster fails closed (design §9
  gate 14), and validation is exact replay.
- `claim_standing/stance_record.schema.json`
  (`claim-standing-stance-record/1.0`) is the stance-classification output for
  one probe run: full §7 probe-identity hashes, one row per selected work
  family under the closed §5.1 vocabulary and cross-field rules (a performed
  row requires at least one `EVR-CS-` evidence-row reference; metadata-only
  coverage can never be performed), the all-selected distribution whose seven
  buckets must sum to `selected_total`, a mandatory
  `STANCE CLASSIFICATION UNMEASURED` banner, and no scalar
  credibility/confidence/trust field anywhere (test-pinned).

Provider retention disclosure is also closed: `known` requires a non-empty
reference and `unknown` requires null.

The schema-level `\\S` checks are portable first screens. The runtime applies a
single NFKC visible-semantic-text predicate to the claim/query, disclosure,
identity, available-abstract, successful-assessment, and failure-detail
surfaces; it rejects surrogates and text made only of Unicode control/format,
separator, combining, whitespace, or punctuation characters. Failed malformed
assessment raw output remains exact evidence and may itself be whitespace- or
format-only. DOI text is stable identity only when strict NFKC/prefix-trimmed
`10.<4-9 digits>/<suffix>` validation succeeds.

The pure local finalizer is
`@/engine/scripts/build_claim_standing_candidate_ledger.py`; the authoritative boundary
is `@/references/claim_standing_candidate_ledger_protocol.md`. This slice
has no discovery adapter, network/model call, stance classification, rendering,
evidence-row extension, pipeline hook, or held-out dispatch. It is an offline
substrate only, remains unmeasured, and does not close.
Its CLI never creates an output for a `session_only` plan. `build --output`
requires the existing, hash-bound `explicit_local_export` consent state; there
is no command-line override. Authorized output must exactly match the
hash-bound absolute `authorized_output_path`, is exclusive/no-follow where the host
supports it, mode `0600` from creation, file- and directory-fsynced, and
truthfully carries the consented persistence/export/path state at the ledger root
and in each work family's sharing scope. Its separate rights basis remains
`not_assessed`; local persistence consent is not a rights claim.

## Sprint contracts

Sprint contract templates for reviewer hard-gate orchestration.

Schema: `@/engine/contracts/sprint_contract.schema.json` (Schema 13).
Validator: `@/engine/scripts/check_sprint_contract.py`.
Protocol: `@/roles/review/panel/strict/sprint_contract_protocol.md`.

### Shipped templates

**(reviewer family)**:

- `reviewer/full.json` — panel 5, 5 dimensions, 4 failure conditions
- `reviewer/methodology_focus.json` — panel 2, 2 dimensions, 3 failure conditions

**Draft / paper suite (generator-evaluator family)**:

- `writer/full.json` — single-agent writer, 7 dimensions (D1 section_completeness / D2 citation_density / D3 argument_blueprint_fidelity / D4 total_word_count / D5 per_section_word_count / D6 acknowledged_limitations / D7 register_consistency), 5 failure conditions (F1 / F4 / F2 / F3 / F0). No `scoring_plan` field.
- `evaluator/full.json` — single-agent evaluator, 5 dimensions (D1 originality / D2 methodological_rigor / D3 evidence_sufficiency / D4 argument_coherence / D5 writing_quality), 7 failure conditions (F1 / F2 / F3 / F6 / F4 / F5 / F0). Carries full `scoring_plan` + `disagreement_handling`.

Both writer + evaluator templates ship under Schema 13.1 (allOf branches 11/12 require `pre_commitment_artifacts` for `writer_full` and `disagreement_handling` for `evaluator_full`; branches 5/6 pin `failure_conditions[].action` to mode-specific enums; branches 8/9 pin F0 contains to the mode's accept variant). Orchestration lives in `@/roles/draft/paper/strict/generator_evaluator_protocol.md` + the writer/evaluator agent files.

### Reserved reviewer modes without shipped templates

`reviewer_guided` is in the schema enum but ships without a template (guided mode operates without a sprint contract). `reviewer_re_review` left the Schema 13 enum: re-review is governed by the dedicated contract family under `re_review/` (four schemas + `@/engine/scripts/check_re_review_synthesis.py`), not by a Schema 13 template — a contract claiming `mode: reviewer_re_review` no longer validates.

### How to add a new template

1. Add the file under `@/engine/contracts/<domain>/<mode>.json`.
2. Run `python @/engine/scripts/check_sprint_contract.py <path> --ars-version vX.Y.Z`; expect
   zero errors and zero soft warnings.
3. If `expression` strings use new phrasing, update `sprint_contract_protocol.md`
   and the synthesizer prompt's recognised-pattern list in the same PR.

## Passport contracts

Schemas for Material Passport input ports.

- `passport/literature_corpus_entry.schema.json` — Schema 9 `literature_corpus[]`
  entries produced by user-written adapters.
- `passport/bibliographic_integrity_signal.schema.json` — v1.0
  additive signal carrier, v1.1 authoritative retraction-status rows, and the
  v1.2 title/abstract tortured-phrase advisory profile,
  including resolver disagreement/reinstatement, judgment context, freshness,
  and opt-in finalizer policy eligibility. The separate
  `retraction_status_cache_v1` namespace and pure resolver live in
  `@/engine/scripts/retraction_status.py`.
- `passport/rejection_log.schema.json` — adapter output companion logging
  entries that could not be included in the corpus.
- `passport/reset_ledger_entry.schema.json` — `reset_boundary[]` ledger entries
  for the opt-in passport reset boundary protocol.
- `passport/standing_constraint_entry.schema.json` — `standing_constraints[]`
  entries: a run-wide constraint the user stated, in their words.
- `passport/excluded_source_entry.schema.json` — `excluded_sources[]`
  entries: a reference an integrity gate judged `NOT_FOUND`, kept off later writer
  dispatches.
- `passport/version_records.schema.json` — optional
  `phase2_investigation/version_records.yaml` sidecar for academic citation version
  families (preprint -> proceedings -> journal extension). This is deliberately a
  sidecar: `literature_corpus_entry.schema.json` stays adapter-owned and unmodified.
- `passport/human_read_log.schema.json` — the user-owned
  `USER_ATTESTED_READ` ledger
  (`<passport-stem>_human_read_log.yaml`, written by `@/engine/scripts/ars_mark_read.py`),
  including required scope on new marks and legacy-compatible scope absence.
  Declaration-only: it is not verified reading or comprehension. Missing/unknown
  scope remains `coverage_unknown` and never promotes to `ok`.
- `passport/user_attested_read_resolution.schema.json` — the closed output
  of `@/engine/scripts/human_read_attestation_resolver.py`; only `state: covered` is
  `ok_eligible`, while absence, rescind, partial/unknown coverage, unresolved
  anchors, and invalid ledgers remain explicitly non-promoting. This output is a
  `transient_routing_decision`, not a persisted audit receipt: it carries no
  input digest and must be recomputed from the current ledger and exact anchor
  on each finalizer pass. Its closed `finalizer_disposition` keeps absent or
  rescinded marks as unacknowledged LOW-WARN, partial/unknown active marks as
  acknowledged-partial, anchor failures on the locator-precedence route, and
  invalid ledgers on a blocking route.

## Shared evidence rows

`@/engine/contracts/evidence/claim_registry.schema.json` is the closed E1
population contract: exact raw-draft hash plus exact UTF-8 byte span and equal
text for every registered claim. `claim_registry_coverage_report.schema.json`
is the deterministic, replay-bound gap report emitted by
`@/engine/scripts/claim_registry_coverage.py`; it binds exact raw draft and serialized
registry hashes and joins only those exact spans. It covers citation-bearing
and quantitative candidate sentences only. Its finite grammar includes common
Markdown/numeric/author-year/Pandoc/inline-reference citations plus
unit-bearing numbers, p-values, `N=...`, and common effect-size/ratio notation;
unrecognized scholarly syntax remains possible. The report always records
`semantic_extraction_coverage: not_machine_detectable`; it cannot certify that
every substantive claim was extracted into E1. Consumers replay the report
against both inputs; absence, stale bindings, or validation failure are
unresolved execution states, never a zero-gap result.

## Review-panel provenance

`reviewer/review_panel_provenance_input.schema.json` records actual seat-level
observations; `reviewer/review_panel_provenance.schema.json` is the closed,
replay-derived artifact built by `@/engine/scripts/review_panel_provenance.py`. Both are
closed to `reviewer_full`, bind the exact raw-byte digest of
`reviewer/full.json`, and require the ordered `EIC`, `R1`, `R2`, `R3`, `DA`
roster. Actual execution observations remain nullable and are never filled from
those seat labels. The artifact keeps role separation, within-panel invocation
context separation, peer-output blinding, model-family diversity, provider
diversity, and accountable-human diversity as six separate `true` / `false` /
`unknown` axes. `fresh_context_scope: within_panel_attempt_only` makes explicit
that no cross-attempt history is checked. Missing facts remain unknown,
same-family or family-unknown execution carries a fixed correlated-error
disclosure, and no persona-derived binary independence field is admitted.

`reviewer/review_panel_provenance_carrier.schema.json` is the exact closed
Schema 6 valid/invalid union. The valid branch is accepted only after the
runtime hashes the referenced artifact's exact raw bytes, validates and replays
it, and compares the normalized-manifest digest, execution-topology digest,
fresh-context scope, and six axes. The invalid branch admits only
`absent|unreachable|digest_mismatch|schema_invalid|replay_invalid`, forces all
axes to `unknown`, and carries no path or digest. `reviewer_full` must emit one
branch; the other closed modes must omit the field. Use
`@/engine/scripts/review_panel_provenance.py validate-schema6` for mode-scoped presence
and replay validation.

`@/engine/contracts/evidence/evidence_row.schema.json` defines the closed
`evidence-row/1.0` carrier for evidence shown at human-adjudication checkpoints.
V1 has one consumer discriminator, `surface: phase_e_claim_verification`: the
Stage 2.5/4.5 Phase E Claim Verification Report persists
one row per `(claim_id, ref_slug, anchor)` at Integrity Report
`phases.E_claims.evidence_rows[]`. The array is additive: a positively identified
earlier report may omit it and, only with `--allow-legacy-absence`, renders
exactly `LEGACY — EVIDENCE ROWS UNAVAILABLE`; missing shape alone is not legacy
proof and never means that evidence was checked. The opt-in Stage 4→5
`claim_audit_results[]` contract is a separate lifecycle and is unchanged.

The one evidence-state vocabulary is:

- `verified_exact_match` — a once-decoded writer `quote` anchor matched the
  exact session-held source string;
- `agent_extracted` — a `page`/`section` passage selected by the auditing agent,
  also exact-substring checked, but labeled non-authoritative because passage
  selection is agent judgment;
- `unconfirmed_anchor` — session source was present but the writer's decoded
  quote did not match it;
- `not_checked`, `source_missing`, `access_failed`, `retrieval_failed`, and
  `anchorless` — explicit empty states. V1 maps `paragraph` to `not_checked` and
  `none`/a missing marker to `anchorless`.

These states describe excerpt provenance/availability only. They never compute
or change the independent Phase E `verdict`, issue severity/count, or PASS/FAIL
decision. Viewing a row is not reading the source: the runtime never reads or
writes `human_read_log`, never invokes the user's read-scope declaration, and never affects
LOW-WARN/read-scope promotion.

`@/engine/scripts/evidence_rows.py` is the standard-library-only normative runtime:

```python
strict_percent_decode(value)
build(row, session_source_or_none, *, extracted_text=None,
      failure_state=None, cached_row=None)
validate(row, session_source_or_none=None)
paginate(rows, page=1, page_size=25)
render_markdown(rows, page=1, page_size=25, *, session_sources=None)
render_html(rows, page=1, page_size=25, *, session_sources=None)
```

The decoder is strict UTF-8 and runs exactly once (`+` is not a space;
`%2520` becomes the literal `%20`). Positive excerpts must be an exact
contiguous substring of the explicitly supplied session source. Quote anchors
and excerpts are each capped at 25 words by whitespace split and 1000 Unicode
code points. `source_content_sha256` hashes the exact session source encoded as
UTF-8 with no Unicode, whitespace, or newline normalization;
`source_artifact_sha256` hashes optional raw artifact bytes and never substitutes
for the content hash. UTF-8 byte offsets bind an excerpt to the content hash.
`row_sha256` covers canonical JSON for the complete row except the digest field
itself. It is an unkeyed integrity checksum, not a signature or independent
proof of provenance. Source-bound trust is established by replaying the row
against explicitly supplied session source text. Direct Python
`validate(row)` without its optional source argument checks only closed shape,
cross-fields, and self-contained integrity; it does not prove source provenance.

Cache keys bind schema/surface, claim and citation identity, source-content
hash, decoded anchor, resulting state, and (for `page`/`section`) the candidate
excerpt hash. A key match is replay-validated against the current session
source before reuse. Hits preserve the original excerpt and `captured_at`, then
set `cache.status: hit` and recompute `row_sha256`. Claim/source/content/candidate
drift is a miss. A corrupt candidate is ignored and rebuilt from current explicit
inputs; it is never returned as a hit. Current explicit failure states win without
reading cached evidence; failure/empty states are never cached.

Renderers are pure functions over persisted rows plus the explicit in-memory
`session_sources` mapping supplied by their caller. Every source-bound row must
have a matching `ref_slug → exact source text` entry and is replay-validated
before anything is displayed; missing or drifting text fails closed. Empty-state
rows need no source map. For V1 rows, the CLI's `--source-dir` builds the mapping from the
files named by `source_file_name(ref_slug)` that source-bound rows name in one
folder, read as exact UTF-8 bytes, and opens no other file. The renderer
does not accept or follow a source pointer,
URL, DOI, retrieval client, model, cache, or read ledger. Integrity validation
checks the stored encoded/decoded-anchor relationship; display does not decode or
alter the stored anchor again. Markdown and HTML external strings are rendered
inert, including percent-decoded markup, table delimiters, bare URLs/email,
newlines, all Unicode `Cc`/`Cf` controls, and U+2028/U+2029. A render page contains
at most 25 rows, preserves document order, reports total/page bounds and
deterministic previous/next/explicit-page navigation, and never silently
truncates. There is intentionally no `--all`; any number of persisted rows
remains accessible by page.

For any Integrity Report wrapper with `evidence_rows` present, the adapter
requires integer `E_claims.checked` and `E_claims.verified`; it checks that unique
evidence `claim_id` count equals `checked`, unique `VERIFIED` claim count equals
`verified`, and every row sharing a claim ID carries the same claim object and
claim-level verdict. Thus `checked > 0` with an empty present array fails. Raw
single-row and row-array inputs remain valid standalone runtime inputs. Only an
absent `evidence_rows` field is legacy-compatible. Exact omission
of a selected `(claim_id, ref_slug, anchor)` tuple cannot be proved from this
wrapper alone because the E1 selected-tuple registry is not machine-carried here;
the current producer must enforce that completeness before handoff.

Rows containing an excerpt or decoded quote anchor default to
`session_only`/`not_assessed`. Only an explicit user declaration may set the
paired `user_confirmed_shareable`/`user_declared_authorized` values. The length
limit is data minimization, not a licence, copyright exception, or publication
right; exported reports must retain the row handling label/caveat or strip the
external text.

Validate persisted rows or render exactly one page. On both CLI commands, any
source-bound row requires replay from an explicit `ref_slug → source text` JSON
map, or from a folder of per-source text files (V1 rows only):

```bash
python @/engine/scripts/evidence_rows.py validate evidence-rows.json \
  --source-map session-sources.json

python @/engine/scripts/evidence_rows.py render evidence-rows.json \
  --format markdown --page 1 --page-size 25 \
  --source-dir paper_evidence_sources/stage-2.5
```

Exactly one of `--source-map` and `--source-dir` is required whenever either CLI
command receives a document with a source-bound state. The command opens the
JSON map, or only the folder's files that source-bound rows name, and no other
file. Missing
`evidence_rows` is a render failure by default. A positively identified earlier
Integrity Report renders the exact fixed legacy label with exit 0 only when the
caller adds `--allow-legacy-absence`; `validate` always rejects the absence.
Current producers may never use the compatibility flag.

`@/engine/contracts/evidence/evidence_row_v1_1.schema.json` is the separately
versioned extension for `surface: authority_profile_content_coverage`.
It replaces Phase E claim/verdict fields with exact authority-requirement,
structured-expectation, packet-artifact, and document-locator bindings. Its
states are `agent_extracted`, `checked_no_match`, `not_checked`,
`source_missing`, `access_failed`, and `retrieval_failed`; they describe only
the provenance or absence of one bounded advisory passage. The shared 25-word,
1,000-code-point, strict once-decode, exact UTF-8 replay, inert rendering,
rights, and human-read-ledger boundaries still apply. V1.1 performs no cache
lookup. `@/engine/scripts/evidence_rows.py` exposes `build_advisory(...)` for this
surface, while the existing `evidence-row/1.0` builder and rendered bytes remain
unchanged. Its CLI refuses V1.1 rows with exit 2 and names
`@/engine/scripts/build_content_coverage_advisory.py` instead. The versioned surfaces cannot be mixed in one page.

`@/engine/contracts/evidence/evidence_row_v1_2.schema.json` is the separate closed
version for `surface: cross_document_consistency`. It binds one complete
ordered bilateral or trilateral advisory observation to the exact accepted
manuscript and optional completed-preregistration bytes. It is finalized only by
`@/engine/scripts/build_cross_document_consistency_advisory.py`; the existing 1.0/1.1
schemas and `@/engine/scripts/evidence_rows.py` identities and behavior remain unchanged.

`@/engine/contracts/evidence/evidence_row_v1_3.schema.json` is the separate closed `evidence-row/1.3` carrier for the `claim_standing_advisory` surface (design §5.2): one row per (probe claim, selected work-family candidate) binding the bounded inspected-evidence excerpt to its exact source hash/span, reusing the family's excerpt/cache/content-handling blocks verbatim (test-pinned). The row is provenance-only — it never carries a stance or verdict, an exact excerpt match never determines stance, and abstract-level coverage is declared as such and never rendered as verified full text.

## Non-ranking revision authority

The current reviewer-to-author revision family lives under `revision/`:

- `revision_roadmap.schema.json` — immutable reviewer-owned
  `revision-roadmap/1.0`, exact draft/manifest bindings, source-trace order,
  independent severity/obligation/cost/consequence, and proposed target scopes;
- `claim_surface_manifest.schema.json` — exact registered Claim Intent surfaces,
  raw UTF-8 spans, hashes, blocks, current rungs, and byte-identical equality
  between every protected surface and its referenced ClaimIntent `claim_text`;
- `author_adjudication_input.schema.json` and
  `author_adjudication.schema.json` — explicit session-author choices and the
  deterministic raw-hash-bound sidecar; and
- `integrity_correction_list.schema.json` plus the integrity authorization
  input/output schemas — proposal-only issues and explicit author approval of
  the complete exact patch SHA-256; and
- `revision_evidence_bundle.schema.json` plus the integrity receipt schema
  — a continuous local chain from exact integrity PASS through current
  review-write/no-op/integrity rounds to the final draft; and
- `claim_strength_drift_findings.schema.json`,
  `claim_strength_drift_disposition_input.schema.json`, and
  `claim_strength_drift_disposition.schema.json` — the E6 semantic finding set,
  transient exact raw-event artifact paths plus choices, and deterministic
  hash-bound disposition sidecar. Build and replay validation safely reopen
  every explicitly named regular non-symlink event file and recompute its raw
  SHA-256; a digest assertion alone is insufficient. The sidecar retains no
  event path or raw message. This byte binding does not authenticate source,
  content meaning, or actor identity.

`@/engine/scripts/revision_roadmap.py` builds, validates, renders, and bundle-replays this
family without a model, network, API, directory scan, or ambient clock. It opens
only explicitly named local artifacts through containment, symlink, and
read-once guards. Bundle validation reruns the pure current patch engine for
every write round and requires byte-exact replay output to equal the named post
draft; rewritten artifact/report hashes cannot substitute for authorized bytes.

The current patch schema accepts only format 1.1 and separates
`review_roadmap` from `integrity_correction` authority. Registered claim
replacements and declined-overlap collateral authority are exact and
single-use. An integrity issue list grants no write by itself: apply requires a
separate author sidecar whose explicit input already carries the exact proposed
patch digest. Apply report 1.3 records the replayed witness and explicitly leaves
unregistered semantic drift to E6 review. Once E6 reports a drift row, it has no
ordinary advisory default: `@/engine/scripts/claim_strength_drift_disposition.py` requires
one explicit `restore`, `authorize_with_reason`, or `pause` choice per finding;
only an all-authorized sidecar derives `authorized_to_continue`. The sidecar
proves finding coverage and artifact binding, not semantic-detection completeness
or scientific warrant. Patch 1.0 lives only under
`patch/legacy/v1_0/` with its archived loader.

The current `re_review/` family is version 1.1, uses
`obligation_class`, hard-requires original/revised drafts, roadmap, author
sidecar, and bundle, and copies
author fields exactly into Schema 11. Earlier versions are not included; mixed chains are invalid.


## Human-subjects correspondence contract

`human_subjects/committee_correspondence.schema.json` defines the standalone
`review revision-coach` committee-correspondence variant. It binds every
confirmed source comment to one concern record while preserving the entire UTF-8
letter byte-for-byte, including non-comment material. The contract carries
multi-label actions, explicit authority/provenance, optional profile enrichment,
fixed unresolved placeholders, the administrative boundary, and no model
priority or severity.

Validate a bundle with:

```bash
python @/engine/scripts/check_committee_correspondence.py \
  committee_correspondence/<source-sha12>/concern_tracker.json
```

The checker recomputes file/segment hashes, contiguous byte coverage, exact
comment-to-concern accounting, source order, full-permutation working views, and
response-skeleton coverage.

## Human-subjects authority context

The `human_subjects/` authority family keeps selection explicit and separates three
closed artifacts:

- `irb_context_record.schema.json` — the author-confirmed facts plus exact,
  axis-qualified profile and overlay pins;
- `authority_profile_registry.schema.json` — curator-owned, versioned, bounded
  profiles and row-local source anchors;
- `resolved_authority_context.schema.json` — a pointer-only, deterministic
  three-valued applicability trace and downstream gate.

V1 has exactly two axes: `review_ethics` and `data_protection`. Institutional and
funder rules are additive overlays, never a third axis; display precedence cannot
remove, merge, or satisfy a requirement. The shipped registry demonstrates the
same contract with bounded US 45 CFR 46, Taiwan Human Subjects Research Act, and
GDPR research subsets. It is not a completeness, compliance, pathway, exemption,
or authorization claim.

Resolve an explicit context offline, lint the registry alone, or replay-check a
serialized result before consuming it:

```bash
python @/engine/scripts/resolve_human_subjects_authority.py \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --output resolved-authority-context.json

python @/engine/scripts/resolve_human_subjects_authority.py \
  --registry @/engine/human_subjects_authority_registry.json \
  --check-registry

python @/engine/scripts/resolve_human_subjects_authority.py \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --check-resolved resolved-authority-context.json
```

The resolver is standard-library-only, opens only named files, evaluates a closed
Strong-Kleene predicate AST, never infers a jurisdiction, and rejects duplicate
JSON keys and non-finite numbers. Protocol:
`@/references/human_subjects_authority_protocol.md`.

## Human-subjects submission-packet manifest

Two closed contracts define the deterministic packet layer:

- `@/engine/contracts/human_subjects/submission_packet_inventory.schema.json` — an author-declared
  list of exact packet-relative files, byte digests, evidence bindings, responsible
  holder roles, declared structure metadata, waiver/exception claims, and
  caller-supplied authorization status; and
- `@/engine/contracts/human_subjects/submission_packet_manifest.schema.json` — the pointer-only,
  replay-bound result with five structural status tokens, exact requirement and
  evidence pointers, independent readiness/authorization fields, and the
  fixed non-authorization boundary.

The checker consumes a authority result only after exact replay against its
named context and registry. It filters to `submission_packet` consumer rows and
uses only `evidence_expected` ids, artifact types, and holders. It never evaluates
or copies `structured_expectations`, descriptions, or attachment prose; exact
whole-row bytes are canonical-hashed only for replay integrity. It never infers a
jurisdiction, grants a waiver, verifies institutional acceptance, or updates the
caller-supplied authorization value. An evidence row is packet-owned only when
both its exact obligated actor and exact expected holder occur in the declared
packet-responsibility roles. Declared version, date, signature, and certificate
metadata is syntax/internal-consistency only unless a separately versioned,
source-backed mechanical expectation exists.
Once the authority and capability gates permit packet observation, every
inventoried path retains a `DOCUMENTED` or `CONFLICTING` row for
declared-vs-attached visibility, including extra files not consumed by the
selected profiles. A closed gate leaves observations empty and does not open the
packet root. Observation status alone does not change readiness; only an
applicable packet-owned evidence entry can create a listed packet gap.
The runtime rejects more than 512 copied consumer scopes, more than 4,096 entry
or exclusion rows, and any final canonical manifest larger than 8 MiB, ensuring
that every successful build can be replayed by the same CLI.

Build, replay-validate, or render a manifest offline with:

```bash
python @/engine/scripts/build_submission_packet_manifest.py build \
  --inventory inventory.json \
  --packet-root packet \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --resolved resolved-authority-context.json \
  --output submission-packet-manifest.json

python @/engine/scripts/build_submission_packet_manifest.py validate \
  --manifest submission-packet-manifest.json \
  --inventory inventory.json \
  --packet-root packet \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --resolved resolved-authority-context.json

python @/engine/scripts/build_submission_packet_manifest.py render \
  --manifest submission-packet-manifest.json \
  --inventory inventory.json \
  --packet-root packet \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --resolved resolved-authority-context.json
```

The authority triplet is all-or-none. An intentionally absent triplet produces an
unresolved manifest without a default profile; a partial or mismatched triplet is
a contract error. `render` requires the same inputs and exact replay, so a
self-consistent but forged manifest digest is insufficient.

Protocol: `@/references/submission_packet_manifest_protocol.md`.

## Review-pathway rule trace

Two closed Draft 2020-12 contracts define the determination-adjacent trace:

- `@/engine/contracts/human_subjects/review_pathway_trace_request.schema.json`
  binds caller-owned candidate question labels to an exact, complete partition
  of every selected-profile `pathway_trace` requirement; and
- `@/engine/contracts/human_subjects/review_pathway_rule_trace.schema.json`
  carries matched, unmatched, and unresolved predicate work, profile-local
  alternatives, exact fact occurrences, responsible authority roles, exact
  requirement/anchor pointers, the fixed institutional result, and the
  footer.

The standard-library-only builder first replays the exact context,
registry, and resolved artifact. It never invents a candidate name, profile,
predicate, authority anchor, determination, probability, rank, or timeline. All
selected profiles on both axes are accounted for, but candidates and
alternatives stay profile-local. An unknown requirement fact remains unresolved;
a missing profile halts without candidate rows at `JURISDICTION_UNRESOLVED`.

Build, replay, render, and lint only explicitly named artifacts:

```bash
python @/engine/scripts/build_review_pathway_rule_trace.py build \
  --request pathway-trace-request.json \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --resolved resolved-authority-context.json \
  --output pathway-rule-trace.json

python @/engine/scripts/build_review_pathway_rule_trace.py validate \
  --request pathway-trace-request.json \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --resolved resolved-authority-context.json \
  --trace pathway-rule-trace.json

python @/engine/scripts/build_review_pathway_rule_trace.py render \
  --request pathway-trace-request.json \
  --context context.json \
  --registry @/engine/human_subjects_authority_registry.json \
  --resolved resolved-authority-context.json \
  --trace pathway-rule-trace.json \
  --output pathway-rule-trace.md

python @/engine/scripts/check_review_pathway_output.py \
  --trace-json pathway-rule-trace.json \
  --rendered pathway-rule-trace.md
```

The banned-output lint is surface-scoped to those named generated files and
permits a pathway term only in the exact candidate grammar. Successful replay or
lint never changes a readiness, authorization, acceptance, verdict, checkpoint,
or workflow gate. Protocol:
`@/references/review_pathway_rule_trace_protocol.md`.

## Authority-profile content-coverage advisory

`@/engine/contracts/human_subjects/content_coverage_advisory.schema.json` defines
the closed final `content-coverage-advisory/1.0` carrier. It consumes a
manifest only after exact replay against the named inventory, packet root,
context, authority registry, and resolved context. It then binds explicit
evaluator judgments to exact `structured_expectations[]` pointers and exact
session-held artifact strings through `evidence-row/1.1` rows. The standard
library finalizer is `@/engine/scripts/build_content_coverage_advisory.py`.

The output layer is always `LLM-ADVISORY`, and its independent field is
`advisory_coverage_status`. The finalizer copies deterministic packet status,
readiness, caller-supplied authorization, institutional-acceptance boundary,
authority/evidence pointers, and digests without changing them. A structural
gap, external dependency, or waiver/exception boundary cannot be converted into
a semantic missing-element finding. Applicability-false requirements remain
excluded, and every profiled structured expectation is either explicitly
checked or explicitly `not_checked`; missing session content never becomes an
implicit negative result.
An open authority/capability gate with an explicitly unprovided overlay
selection preserves each selected base requirement as
`APPLICABILITY_UNRESOLVED` without inspecting content; a fully closed gate has
no exact requirement to report and is rejected.

The final carrier is deliberately marked `evaluation_status: UNMEASURED`.
UNMEASURED is not a scored measurement row, and this feature makes no accuracy,
coverage-improvement, or efficacy claim. The finalizer and renderer open only
named inputs, perform no directory scan or retrieval, and invoke no model/API;
the draft judgments and positive-row capture timestamps are caller-supplied
advisory observations. Rendering first replays the deterministic manifest and
every source-bound evidence row, so a self-consistent digest alone is
insufficient. The carrier retains all rows, while one render call exposes only
one explicit page of at most 25 evidence rows with deterministic navigation;
there is no render-all mode.

Protocol:
`@/references/authority_content_coverage_advisory_protocol.md`. Spec:

## Tortured-phrase screening contracts

The family is local, hash-bound, and advisory-only:

- `audit/tortured_phrase_snapshot.schema.json` defines the closed canonical
  `literal` / `all` / `any` / `near` AST and rule-level `exclude_if` grammar;
- `audit/tortured_phrase_snapshot_manifest.schema.json` binds the exact raw
  snapshot bytes, source/version/as-of metadata, preprocessing disclosure,
  zero unsupported rules, and rights; and
- `audit/tortured_phrase_advisory.schema.json` defines the replay-bound
  own-draft `HEURISTIC-ADVISORY` / `UNMEASURED` transcript.

`@/engine/scripts/tortured_phrase_screening.py` accepts only explicitly named local
snapshot/manifest and input paths. A snapshot is either user supplied or a
repository-authored synthetic fixture. this skill includes no native PPS importer,
fetch option, or redistributed PPS list content, and this path invokes no
model, external API, human/model judge, ambient clock, file time, or network
time. Snapshot SHA-256 covers the exact UTF-8 file bytes; required timestamps
are explicit arguments.

The same runtime can return a new passport copy carrying
`bibliographic-integrity-signal/1.2` rows for each cited title and abstract
surface. A missing abstract is an explicit `not_checked` / `unresolved`
`ABSTRACT_MISSING` row; a present whitespace-only abstract uses
`ABSTRACT_EMPTY`. Consumers remain read-only and the enricher refuses
in-place output. A detected row is only a phrase-list match requiring review;
a zero match is not a clean certificate. No result establishes origin,
paper-mill production, contextual validity, or accuracy, and no result creates
a marker, terminal gate, replacement text, or automatic rewrite. All corpus
rows render in the one canonical `Bibliographic Integrity Advisories` section.


## Cross-document consistency advisory

The family is a standalone replay-bound advisory:

- `passport/preregistration_artifact.schema.json` defines the persistent
  `preregistration-artifact/1.0` handoff sidecar;
- `audit/cross_document_source_manifest.schema.json` binds exactly the accepted
  manuscript plus the exact sidecar projection;
- `audit/cross_document_consistency_advisory_draft.schema.json` accepts the
  closed caller-supplied semantic observations;
- `evidence/evidence_row_v1_2.schema.json` binds their exact bilateral or
  trilateral evidence; and
- `audit/cross_document_consistency_advisory.schema.json` defines the canonical
  final `LLM-ADVISORY` / `UNMEASURED` carrier.

Only `@/engine/scripts/build_cross_document_consistency_advisory.py` may build or update
the preregistration sidecar. The non-shell research architect supplies only the
explicit caller status and companion handle. Academic-paper intake and every
pipeline handoff validate and carry the same sidecar and, when provided, the
same companion bytes unchanged. The repository template is guidance, not
evidence.

Finalization replays the sidecar, exact two-artifact manifest, accepted draft,
optional preregistration companion, and every quote or checked scope before
consuming observations. Methods absence requires an exact named counterpart
scope. An undisclosed preregistration deviation requires a third exact manuscript
disclosure-scope witness. Missing or unavailable inputs cannot become a
no-listed result.

At the one mandatory Stage-5 entry checkpoint, runs first and second
against the same accepted-draft artifact ID/SHA-256. Their carriers and failure
semantics stay separate. failure writes no output and produces only bounded
`ADVISORY_UNAVAILABLE:<CODE>`; neither advisory changes Stage 4.5 or Stage-5
routing. Any manuscript revision stales both and requires both to rerun.

The final carrier has no score, pass/fail, gate, readiness, authorization,
rewrite, ClaimIntent, consent/protocol duplicate, or clean-document meaning.
Protocol: `@/references/cross_document_consistency_advisory_protocol.md`.
