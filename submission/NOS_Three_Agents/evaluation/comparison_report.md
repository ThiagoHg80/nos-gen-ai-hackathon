# Comparison report: agents A, B and C

Date: 2026-10-10. Workspace: `NOS_Three_Agents/`.

## 0. Live update (10 Oct 2026, about 18:00 Lisbon)

Sections 1 to 12 were written before any live run. Where they say that no
live result exists, this section supersedes them.

**What ran.** Live benchmark `bench-live-20261010T170036Z` on
`gemini-3.8-flash`, temperature at the model default. The configured
`gemini-3.6-flash` returned HTTP 429 (free-tier quota), so the model was
switched through `NOS_GEMINI_MODEL` and the freeze manifest was rewritten
with a note; no prompt or code changed. Requests used: 8 of 24.

| Agent | Trial | Status | What happened |
|---|---|---|---|
| A | 1 | CANDIDATE_INVALID | All masks correct; the trailing space of the last line (line 60) is missing |
| A | 2 | CANDIDATE_VALID | Strictly valid; identical to the reference rendering, 60 of 60 lines |
| A | 3 | CANDIDATE_INVALID | Same single deviation as trial 1 |
| B | 1 | PIPELINE_FAILED | HTTP 400 `INVALID_ARGUMENT` on the ledger request |
| C | 1 | PIPELINE_FAILED | HTTP 400 `INVALID_ARGUMENT` on the spans request |
| B, C | 2, 3 | NOT_RUN | Skipped: the same request would fail again |

One earlier single run of A on the same model was also valid.

**Agent A, measured (PROVISIONAL, reference not human-reviewed).**

| Measure | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|
| Reference MASK words hidden (of 46) | 46 | 46 | 46 |
| Reference KEEP words hidden (of 193) | 0 | 0 | 0 |
| Ambiguous words hidden (of 115) | 0 | 0 | 0 |
| Precision / recall | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| Unauthorised character changes | 1 deleted | 0 | 1 deleted |
| Valid if trailing whitespace is ignored | yes | yes | yes |
| Prompt / output / thinking tokens | 1,988 / 798 / 4,516 | 1,988 / 799 / 4,051 | 1,988 / 798 / 4,978 |
| Model latency | 61 s | 74 s | 54 s |

**How to read this.**

- The reference and A's prompt were written from the same masking policy
  by the same author. Full agreement shows that the model follows our
  policy on this document. It does not show agreement with the organisers'
  hidden reference.
- The three trials made identical masking decisions. That is three runs on
  one document, not proof of general reliability.
- A's only observed weakness is the one predicted for a model-written
  document: whitespace. Two of three trials dropped the final trailing
  space. Whether that matters depends on whether the hidden reference
  keeps trailing spaces, which is still unknown.
- **B and C are unmeasured, not worse.** Both failed before producing any
  output. The two failing requests are the only ones that send a
  `responseSchema`; A, which sends none, works. That points at the
  structured-output request format, but the cause is not diagnosed. Fixing
  it needs a code change and one or two requests to confirm.
- Cost is UNKNOWN: no verified price was retrieved.

Real error text, as saved (no secret in it):

```
{"error": {"code": 400, "message": "Request contains an invalid argument.", "status": "INVALID_ARGUMENT"}}
```

Results: `evaluation/benchmark_results.csv` and
`evaluation/benchmark_tables.md`. The raw artifacts of the live runs
(requests, raw responses, candidates, validation reports and the request
log) are kept on the machine that ran them and are not committed.

## 1. Summary

- Three agents are implemented and run end to end through one CLI.
- **No live Gemini result exists.** No API key is configured on this
  machine, so the live benchmark was refused before any request was sent.
  Live request count: **0 of 24**.
- Offline evidence: 98 tests pass, flake8 is clean, and a mock benchmark
  (9 runs) completes. Mock runs prove that the code works; they say
  nothing about Gemini's accuracy.
- There is therefore **no measured basis** for ranking A, B and C on
  accuracy, fidelity, latency or cost. Section 8 gives a recommendation
  based on eligibility and engineering properties only, and says what the
  first live benchmark must show.

## 2. Implementation status

Status values: IMPLEMENTED_OFFLINE, LIVE_TESTED, NOT_RUN, BLOCKED, FAILED.

| Item | Status | Evidence |
|---|---|---|
| Agent A - Gated Rewrite | IMPLEMENTED_OFFLINE | 8 agent tests; 3 mock benchmark runs valid |
| Agent B - Decision Ledger + LLM Rendering | IMPLEMENTED_OFFLINE | 9 agent tests; 3 mock runs valid; both stages run in one workflow |
| Agent C - Span Ledger + Deterministic Rendering | IMPLEMENTED_OFFLINE | 9 agent tests; 3 mock runs valid |
| Shared extraction, policy, validators, ledger checks | IMPLEMENTED_OFFLINE | 48 shared tests |
| Gemini REST adapter | IMPLEMENTED_OFFLINE | 16 adapter tests, one against a local stub HTTP server; field names checked against Google's API definition |
| Live trials, A, B and C (3 each) | BLOCKED | no API key; 9 `NOT_RUN` rows in `benchmark_results.csv` |
| Provisional reference annotations | IMPLEMENTED_OFFLINE | built and position-checked; not human-reviewed |
| Metrics and benchmark runner | IMPLEMENTED_OFFLINE | 8 evaluation tests; mock benchmark |
| Competition flake8 check | reproduced locally, passes | `flake8 .` with default rules |
| Competition hidden evaluation and prompt evaluation | could not run | scripts and reference are secret |

No item is LIVE_TESTED and none FAILED.

## 3. Provenance

| Material | Path | Identity |
|---|---|---|
| Challenge brief | `references/official/NOS - JunctionX Lisbon 2026.pdf` | downloaded HTTP 200, PDF, 125,289 bytes, 5 pages, SHA-256 `32d95aa8b2cd...6055b1` |
| Regulations v1.1 | `references/official/JunctionX Lisbon 2026 - Official Regulations.pdf` | downloaded HTTP 200, PDF, 227,500 bytes, 6 pages, SHA-256 `c7715ec22bb2...f014ae` |
| Official repository | `references/nos-gen-ai-hackathon/` | branch `main`, commit `c4995b0` (2025-05-07), clean; JunctionX branch at `3c90e7e` |
| Target document | `input/original/document_to_anonymize.pdf` | 68,002 bytes, 2 pages, SHA-256 `ea79a07011b6...672d77`, byte-identical to the checkout, same blob on both branches |
| Raw extraction | `input/raw_extraction.txt` | PyMuPDF 1.27.2.3 `page.get_text()`, pages concatenated |
| Canonical source | `input/canonical_source.txt` | identical to the raw extraction; SHA-256 `a5f6989f043b...deed74` |

The brief, the regulations and the target document are three different
files. Originals are unchanged. Full records are in
`references/evidence_manifest.json`; requirements with status and
applicability are in `references/evidence_table.md`.

### Frozen transformation contract

| Rule | Frozen value | Basis |
|---|---|---|
| Extraction | PyMuPDF default text, no cleanup | suggested by the brief; the tutorial's accent and punctuation cleanup is not applied |
| Normalisation | newline convention only | - |
| Newline | LF; a final newline is optional and not significant | provisional |
| Lines | 60 source lines, 0 blank, 60 retained | measured |
| Trailing space | kept: all 60 lines end with one space | provisional; also checked with trailing whitespace ignored |
| Blank line | empty or whitespace-only | provisional for whitespace-only |
| Word | run of non-whitespace containing a letter or digit | provisional |
| Mask | core becomes one `*`; opening and closing punctuation stay | provisional |
| Ambiguous values | recorded, left unmasked | provisional |
| Components | 355 whitespace tokens, 354 maskable | measured |

## 4. Per-trial results

### Live trials

| Agent | Trial | Status | Reason |
|---|---|---|---|
| A | 1, 2, 3 | NOT_RUN | BLOCKED: no API key |
| B | 1, 2, 3 | NOT_RUN | BLOCKED: no API key |
| C | 1, 2, 3 | NOT_RUN | BLOCKED: no API key |

Every metric for these rows is N/A. File:
`evaluation/benchmark_results.csv`.

Calls planned: 12. Calls submitted: 0. Tokens, latency and cost: none to
report. Cost would in any case be UNKNOWN: no verified price was
retrieved.

### Mock runs (code-path evidence only, NOT Gemini results)

Benchmark `bench-mock-20261010T151746Z`, 9 runs, all `CANDIDATE_VALID`.
The stand-in masks words after four field labels. Against the provisional
reference it scores precision 1.00 and recall 0.41 for all three agents,
identically, because all three use the same stand-in. Those numbers
describe the stand-in, not any agent's prompt. They show that the
pipeline from candidate to metrics runs. Tables:
`evaluation/mock_benchmark_tables.md`.

## 5. Aggregates

Live: sample size 0 per agent. Completed trials 0, pipeline failures 0,
structural pass rate N/A, conditional accuracy N/A, disagreement between
repeated outputs N/A.

Measured without the model (request sizes, in characters):

| Agent | Stage | System instruction | User content | Schema sent |
|---|---|---|---|---|
| A | rewrite | 4,146 | 2,737 | no |
| B | 1 ledger | 4,854 | 4,163 | yes |
| B | 2 render | 2,280 | 7,438 plus about 20 per decided word beyond the mock's 19 | no |
| C | spans | 4,848 | 4,163 | yes |

Token counts are UNKNOWN until the API reports them. B sends about 2.7
times A's input characters over two calls, before its real ledger is
added.

## 6. Error examples

Only one real error occurred, reproduced verbatim (it contains no secret):

```
BLOCKED: no API key in GEMINI_API_KEY / GOOGLE_API_KEY (environment or .env)
```

No API error, truncation, safety block or invalid model content was
observed, because no request was sent. The handling of those cases is
covered by tests with scripted responses, not by observation:

| Case | Behaviour under test |
|---|---|
| Truncated response (`MAX_TOKENS`) | run fails; partial text saved; never a valid status |
| Safety or `SPII` finish, blocked prompt, no candidates | run fails explicitly |
| Fenced or preambled document | candidate invalid; saved exactly as returned |
| Fenced or cut JSON ledger | parsed as returned, fails; B's stage 2 is not called |
| Unmatched quote, bad ID, contradictory overlap | rendering blocked; no partial output |
| Wrong number of asterisks | alignment UNALIGNABLE; accuracy N/A |
| Budget exhausted | nothing sent; run fails |

## 7. Trade-offs

### Engineering

| Property | A | B | C |
|---|---|---|---|
| Calls per run | 1 | 2 | 1 |
| Who writes the candidate | model | model | Python |
| Unmasked characters equal the source | checked after the fact | checked after the fact | by construction, given valid spans |
| Exposure to the 60 trailing spaces and 10 soft line breaks | yes | yes | none |
| Policy enforced mechanically | no | category and location checks on the ledger | category and location checks on spans |
| Scope change (mask AMBIGUOUS too) | new prompt | new prompt for stage 1 only if categories change; otherwise one policy switch, then a second call | one policy switch, no new call |
| Explanation of each mask | positions only | ledger with category and reason | ledger with category and reason |
| Failure behaviour | candidate rejected | either stage can fail; stage 2 skipped after a stage 1 failure | invalid spans stop the run |

B's validator computes the deterministic rendering internally to check
the model's rendering. The second call therefore reproduces something the
code already holds. Its only gain over C is that the candidate is a
literal model response.

A's policy cannot be enforced mechanically: nothing stops the model from
masking an AMBIGUOUS value. For B and C a MASK entry with an AMBIGUOUS
category is a validation error. This asymmetry will show up as
`ambiguous_hidden_n` in the results.

### Compliance

| Agent | Eligibility | Depends on |
|---|---|---|
| A | fits every reading found | nothing unverified; its two-part prompt would be filed as one text |
| B | UNVERIFIED | whether two prompts may be filed for "the exact prompt" |
| C | UNVERIFIED | whether code may produce `submission.txt` from a model response (inferred from the brief, not stated) |

These labels are independent of technical performance.

### What validation does not show

A structurally valid output can still leak personal data or mask too
much. A deterministic renderer guarantees fidelity for the spans it is
given, not that the spans are complete. Only the reference-based figures
address detection, and those are provisional.

## 8. Recommendation

Evidence is insufficient to recommend an agent on accuracy, fidelity,
latency or cost. On eligibility and engineering alone:

- **Baseline candidate: A.** It is the only agent whose eligibility rests
  on nothing unverified. Its risk is fidelity, which the first live trial
  will show directly (`structural_pass`, `pass_ignoring_trailing_ws`).
- **Candidate if post-processing is confirmed: C.** It removes the
  fidelity risk and makes the scope a switch. It should be preferred only
  after a mentor confirms row 9 of the evidence table.
- **B** is justified only if mentors require an unmodified model response
  and also accept two prompts.

Different criteria may have different winners once measured. Three trials
on one document would not establish general superiority either way. The
team decides; nothing has been selected or submitted.

## 9. Blockers

1. **API key.** Set `GEMINI_API_KEY` (or `.env`) and run
   `run_benchmark.py --mode live`. Twelve requests are planned.
2. **Model access.** `gemini-3.6-flash` with the team's key is unverified.
   The runner checks it with a metadata call before any inference.
3. **Reference review.** A second person must review the annotations
   before any accuracy figure is more than provisional.
4. **Organiser answers** (they change the policy, not the code):
   - Is special-category data masked, or identifiers only?
   - May code transform the model response before `submission.txt`?
   - May a multi-step pipeline file more than one prompt?
   - Is a word a whitespace-separated token, and does attached
     punctuation stay?
   - Are the 60 PDF layout lines kept, and do trailing spaces count?
   - Does the automatic score run on fork pull requests?

## 10. Proposed next steps (not done)

- Run the live benchmark unchanged and read the per-trial rows first.
- If A fails only on trailing whitespace, ask the organisers before
  changing the canonical source; do not tune prompts between trials.
- Human review of the reference; record it in `annotation_policy.md`.
- Add a broad-scope policy version once the scope question is answered.
- For the competition, port the chosen agent into the team's fork under
  `submission/` with real commits from each member.

## 11. Runtime, evaluation and submission artifacts

- Agent runtime: `agents/`, `shared/`, `run_agent.py`.
- Shared evaluation code: `evaluation/`, `run_benchmark.py`. Agents never
  see the reference; two tests guard this.
- Official submission artifacts: none produced. `submission/` in the
  reference checkout is untouched. No commit, push, pull request or CI
  run was made.

## 12. Deliverables

| Deliverable | Path | Exists | Status |
|---|---|---|---|
| Common CLI | `run_agent.py` | yes | IMPLEMENTED_OFFLINE |
| Benchmark runner | `run_benchmark.py` | yes | IMPLEMENTED_OFFLINE; live BLOCKED |
| Agent A | `agents/A_gated_rewrite/` | yes | IMPLEMENTED_OFFLINE |
| Agent B | `agents/B_decision_ledger/` | yes | IMPLEMENTED_OFFLINE |
| Agent C | `agents/C_span_ledger/` | yes | IMPLEMENTED_OFFLINE |
| Shared code | `shared/` | yes | IMPLEMENTED_OFFLINE |
| Tests | `tests/`, `agents/*/tests/`, `evaluation/tests/` | yes | 98 pass |
| Original materials and manifest | `references/` | yes | downloaded and verified |
| Evidence table | `references/evidence_table.md` | yes | complete for accessible sources |
| Target PDF, extraction, canonical source | `input/` | yes | frozen |
| Masking policy | `shared/policy/masking_policy_v1.json` | yes | frozen, provisional |
| Annotation policy and reference | `evaluation/annotation_policy.md`, `evaluation/reference_annotations.json`, `.csv` | yes | provisional, not reviewed |
| Freeze manifest | `evaluation/freeze_manifest.json` | yes | 38 files, holds |
| Live results | `evaluation/benchmark_results.csv`, `evaluation/benchmark_tables.md` | yes | NOT_RUN placeholders (BLOCKED) |
| Mock results | `evaluation/mock_benchmark_results.csv`, `evaluation/mock_benchmark_tables.md` | yes | MOCK only |
| Run artifacts | `runs/` | yes | mock runs only; no live run |
| Request budget log | `runs/_budget/live_requests.jsonl` | no | created by the first live request |
| Setup files | `README.md`, `requirements.txt`, `.env.example` | yes | complete |
