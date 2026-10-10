# NOS Three Agents

Three independent, runnable anonymization agents for the NOS track of
JunctionX Lisbon 2026, with a shared extraction step, masking policy, API
adapter, validators and a bounded benchmark.

| Agent | What the model does | What Python does |
|---|---|---|
| A - Gated Rewrite | One call returns the whole masked document | Validates it; never modifies it |
| B - Decision Ledger + LLM Rendering | Call 1 returns decisions; call 2 renders the document | Validates the ledger, then the rendering; never modifies it |
| C - Span Ledger + Deterministic Rendering | One call returns sensitive spans | Verifies every span and renders the document itself |

**Current status:** all three are implemented and tested offline. No live
Gemini call has been made, because no API key is configured on this
machine. See `evaluation/comparison_report.md`.

Nothing here is a competition submission yet. The workspace does not
write `submission/submission.txt` or `submission/prompt.txt`.

**In the team fork** this folder lives at `submission/NOS_Three_Agents/`.
Two things are deliberately not committed and are re-created by
`references/fetch_references.py`: the organisers' brief and regulations
PDFs (`references/official/`) and the read-only checkout of the upstream
repository (`references/nos-gen-ai-hackathon/`). Their hashes are recorded
in `references/evidence_manifest.json`. The folder's `.gitattributes`
disables end-of-line conversion, because the canonical source and the
frozen hashes depend on exact bytes.

## Setup

Windows PowerShell, Python 3.11, from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run every command below with `.\.venv\Scripts\python.exe -I -X utf8`.
`-I` keeps Python from importing code from the current directory, which
matters because the folder holds downloaded files.

## Reproduce the inputs

```powershell
$py = ".\.venv\Scripts\python.exe"
git clone https://github.com/nosportugal/nos-gen-ai-hackathon.git references/nos-gen-ai-hackathon   # only if missing
& $py -I -X utf8 references/fetch_references.py     # brief, regulations, target PDF + manifest
& $py -I -X utf8 prepare_source.py                  # raw extraction, canonical source, manifest
& $py -I -X utf8 evaluation/build_reference.py      # provisional reference annotations
```

`prepare_source.py` and `fetch_references.py` never overwrite an existing
original. `prepare_source.py` refuses to change a frozen derived file
unless `--force` is given.

## Run one agent

```powershell
& $py -I -X utf8 run_agent.py --agent A --mode mock
& $py -I -X utf8 run_agent.py --agent B --mode mock
& $py -I -X utf8 run_agent.py --agent C --mode mock
& $py -I -X utf8 run_agent.py --agent A --mode live     # needs a key; uses the budget
```

Mock mode needs no credentials and no network. A local stand-in produces
the "model" output, every artifact is labelled `MOCK`, and nothing it
prints is a Gemini result.

Exit codes: 0 valid candidate, 1 invalid candidate or pipeline failure,
2 blocked before running.

## Tests and lint

```powershell
& $py -I -X utf8 -m pytest          # 98 offline tests, synthetic text only
& $py -I -X utf8 -m flake8 .        # default rules, as in the competition CI
```

## Benchmark

```powershell
& $py -I -X utf8 run_benchmark.py --freeze --note "why"   # write the freeze manifest
& $py -I -X utf8 run_benchmark.py --mode mock             # code-path check
& $py -I -X utf8 run_benchmark.py --mode live             # 3 trials x (A 1 + B 2 + C 1) = 12 requests
```

A live benchmark is refused before any request when the freeze manifest
does not match the files, the key is missing, the model cannot be reached,
or the remaining budget cannot cover the planned trials. Trials run in the
order A, B, C within each trial number. Prompts and settings are never
changed between trials and every trial is kept.

If an agent's trial fails with a configuration-level error (`BAD_REQUEST`,
`ACCESS_DENIED`, `MODEL_NOT_FOUND`, `BUDGET_EXHAUSTED`), that failure is
kept and the agent's remaining trials are recorded as `NOT_RUN`, because
an identical request would fail the same way.

Re-score saved runs without calling the model:

```powershell
& $py -I -X utf8 evaluation/evaluate_runs.py --index runs/_benchmarks/<id>.json
```

## Credentials and model

- Key: environment variable `GEMINI_API_KEY` (or `GOOGLE_API_KEY`), or a
  `.env` file in this folder. See `.env.example`. The key is sent in a
  request header, never in a URL, never printed and never written to an
  artifact. Error text is sanitised before it is saved.
- Model and settings: `shared/model_config.json`. Default
  `gemini-3.6-flash`, temperature not sent (model default), 16,384 output
  tokens, 120 s timeout. `NOS_GEMINI_MODEL` overrides the model; doing so
  invalidates the freeze manifest on purpose.
- The adapter calls the REST `generateContent` endpoint with the standard
  library. There is no SDK and therefore no hidden retry.

## Resource limits

| Limit | Value | Where |
|---|---|---|
| Live inference requests, whole task | 24, failures and retries included | `runs/_budget/live_requests.jsonl` |
| Retry | 1 per stage, transient transport/service errors only | `shared/gemini_client.py` |
| Retry of invalid model content | never | - |
| Network timeout | 120 s per request | `shared/model_config.json` |
| Output cap | 16,384 tokens; truncation is detected and fails the run | same |
| Input size | checked before each request; no chunking | `check_input_size` |

Requests used so far: 0.

## Inputs and artifacts

| Path | Content |
|---|---|
| `references/official/` | Challenge brief and regulations, as downloaded |
| `references/nos-gen-ai-hackathon/` | Read-only checkout of the official repository |
| `references/evidence_manifest.json` | Source, size, SHA-256, pages, commit of each reference |
| `references/evidence_table.md` | Requirements with status and applicability |
| `input/original/document_to_anonymize.pdf` | The target document, unchanged |
| `input/raw_extraction.txt`, `input/canonical_source.txt` | Extracted text; see `input/source_manifest.json` |
| `shared/policy/masking_policy_v1.json` | Frozen provisional masking policy |
| `evaluation/reference_annotations.json` / `.csv` | Provisional reference, one row per word |
| `evaluation/freeze_manifest.json` | Hashes frozen before measured trials |
| `runs/<agent>/<run_id>/` | Immutable artifacts of one run |
| `runs/_benchmarks/<id>.json` | Which runs belong to a benchmark |
| `evaluation/benchmark_results.csv` | Live results (currently `NOT_RUN` placeholders) |
| `evaluation/mock_benchmark_results.csv` | Mock results, code-path evidence only |
| `evaluation/comparison_report.md` | Findings, trade-offs, blockers |

Each run directory holds the exact request, the raw API response of every
stage, the raw text, parsed ledgers or spans, `candidate.txt` when one
exists, `validation.json` and `result.json`. Files are made read-only and
a run directory is never reused.

Every agent returns the same result contract: `agent_id`, `run_id`,
`hashes` (source, policy, model config, freeze manifest, agent files),
`status`, `failure_reason`, `artifacts`, `validation`, `usage`, `timings`,
`stages`, `competition_eligibility`.

`status` is `CANDIDATE_VALID`, `CANDIDATE_INVALID` or `PIPELINE_FAILED`.
A failed run never gets a valid status, and its response is still saved.

## What is runtime, what is evaluation, what is a submission artifact

- **Agent runtime:** `agents/`, `shared/`, `run_agent.py`.
- **Shared evaluation code:** `evaluation/`, `run_benchmark.py`. Agents
  never import it and never see the reference; a test enforces this.
- **Competition submission artifacts:** none are produced here. For the
  competition, `submission/submission.txt` would be a run's
  `candidate.txt` and `submission/prompt.txt` the prompt that produced it.

## Known limitations

- No live result exists yet. Mock tests prove code behaviour only.
- The reference annotations are an AI-written draft that no human has
  reviewed. Every accuracy figure computed against them is provisional.
- The masking scope, the word rule and the whitespace baseline are
  provisional team rules; the organisers define none of them. In
  particular the hidden reference may mask health and other
  special-category data, which policy v1.0 records as AMBIGUOUS and leaves
  unmasked.
- The canonical source keeps the space PyMuPDF emits at the end of every
  line of this PDF. Whether the hidden reference keeps it is unknown, so
  each candidate is also checked with trailing whitespace ignored.
- `gemini-3.6-flash` access with the team's key is unverified. The REST
  field names were checked against Google's public API definition, not
  against a live call.
- Structural validation cannot show that all personal data was masked.
- Agent C's and agent B's competition eligibility is unverified; see the
  report.


## Optional multilingual privacy validation

Install only when needed, from this folder:

```powershell
& $py -m pip install -r requirements-privacy.txt
& $py -I -X utf8 -m pytest tests/test_censorship.py -v
```

One shared xx_ent_wiki_sm pipeline handles English, Portuguese and Spanish.
The model download is approximately 11 MB; the other packages add further
installation size. Agent outputs are not changed. Tests use synthetic text
and skip when optional dependencies or the model are absent.
Domain rules and models are loaded locally without downloads during checks.

To explicitly check an existing document, select its path:

```powershell
$env:NOS_PRIVACY_DOCUMENT = "..\submission.txt"
& $py -I -X utf8 -m pytest tests/test_censorship.py -v
Remove-Item Env:NOS_PRIVACY_DOCUMENT
```

An explicitly selected missing or empty document fails. Findings report
entity types and offsets, not sensitive source text. No findings do not prove
anonymity; false positives and negatives require human review. This heuristic
does not check formatting or establish competition eligibility.

Package references:
[Presidio](https://github.com/microsoft/presidio),
[spaCy and multilingual model](https://spacy.io/models/xx),
[Great Expectations](https://docs.greatexpectations.io/),
[pandas](https://pandas.pydata.org/).
Project-wide working rules and delivery checks are in
[AGENTS.md](../AGENTS.md) and
[COMPETITION_COMPLIANCE.md](../COMPETITION_COMPLIANCE.md).
