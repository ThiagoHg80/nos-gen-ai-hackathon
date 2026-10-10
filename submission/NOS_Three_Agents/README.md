# NOS Three Agents — technical guide

Detailed setup, commands, limits and artifacts. The project story, the
results and the team are in the [main README](../../README.md).

Three independent, runnable anonymization agents for the NOS track of
JunctionX Lisbon 2026, with a shared extraction step, masking policy, API
adapter, validators and a bounded benchmark.

| Agent | What the model does | What Python does |
|---|---|---|
| A - Gated Rewrite | One call returns the whole masked document | Validates it; never modifies it |
| B - Decision Ledger + LLM Rendering | Call 1 returns decisions; call 2 renders the document | Validates the ledger, then the rendering; never modifies it |
| C - Span Ledger + Deterministic Rendering | One call returns sensitive spans | Verifies every span and renders the document itself |

**Current status (10 Oct 2026, evening):** all three are implemented and
tested offline. Agent A has run live on `gemini-3.8-flash`. Agents B and C
fail on their first live request with HTTP 400 and are not measured yet.
See `evaluation/comparison_report.md`, section 0.

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

Requests used so far: 8 of 24.

Live runs so far used `gemini-3.8-flash`, because the default
`gemini-3.6-flash` hit the key's free-tier quota (HTTP 429). The freeze
manifest records that switch, so set the same model in the shell before a
live run, otherwise the freeze check blocks it:

```powershell
$env:NOS_GEMINI_MODEL = "gemini-3.8-flash"
```

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

- Live results exist for agent A only: three benchmark trials on one
  document. B and C are blocked by an HTTP 400 on their structured-output
  request. Mock tests prove code behaviour only.
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
- The plain-text request used by agent A works live. The structured-output
  request used by B and C was checked only against Google's public API
  definition and is rejected by `gemini-3.8-flash`; the cause is not
  diagnosed yet.
- Structural validation cannot show that all personal data was masked.
- Agent C's and agent B's competition eligibility is unverified; see the
  report.
