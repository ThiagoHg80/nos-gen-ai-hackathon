# Agent

One model call returns the whole document with personal data masked. The
answer is written exactly as returned, by default to `submission.txt`. The
model is Gemini, or any local OpenAI-compatible server for testing.

```
PDF -> raw_uncensored_document.txt -> prompt -> LLM -> answer file
```

The agent does not check, score or record its answers. That is the job of
`benchmark/`, which you can run on any answer file afterwards.

## Setup

Run everything from `submission/`.

```
pip install pymupdf langchain-core langchain-google-genai langchain-openai pytest
```

## Models

| `--provider` | Default `--model` | Needs |
|---|---|---|
| `gemini` (default) | `gemini-3.6-flash` | `GEMINI_API_KEY` in the environment or `submission/.env` |
| `local` | `local` | An OpenAI-compatible server at `--base-url` (default `http://localhost:8080/v1`) |

For example with llama.cpp:

```
llama-server -m model.gguf --port 8080
python -m agent --provider local --out local_answer.txt
```

`LLM_PROVIDER` and `LOCAL_LLM_URL` set the defaults of `--provider` and
`--base-url`. Temperature is never sent, so each model uses its own default
(Gemini 3 recommends keeping it).

## Prompt

The prompt is the instruction text sent as the system message. The
document is sent separately, as the user message between `<document>` tags.

By default the agent reads `submission/prompt.txt`. If that file is empty
it stops and says so. Other prompts are in `submission/prompts/`; pass one
with `--prompt`.

## Run

```
python -m agent --dry-run                  # show the prompt, no API call
python -m agent                            # call Gemini, write submission.txt
python -m agent --prompt prompts/prompt02.txt
python -m agent --pdf other.pdf --out answer.txt
```

`--pdf` defaults to `raw_data/document_to_anonymize.pdf`, `--out` to
`submission/submission.txt`. Every run first extracts the PDF to
`submission/raw_uncensored_document.txt`.

When the answer goes to `submission.txt` and you passed a different
`--prompt`, that prompt is also copied into `prompt.txt`, so the two files
always match.

Nothing is written when the model call fails after one retry or the
answer is cut off (its `finish_reason` is not `STOP`).

Exit codes: `0` answer written, `1` model failure, `2` not run (empty prompt
or no API key).

## Evaluate an answer

```
python -m benchmark.mask_syntax_validation raw_uncensored_document.txt submission.txt
python -m benchmark.mask_diff raw_uncensored_document.txt submission.txt
```

## Files

| File | Job |
|---|---|
| `__main__.py` | Arguments and the LangChain chain that links the steps |
| `extraction.py` | PDF to text (PyMuPDF), exact spaces and accents kept |
| `prompt.py` | Loads the prompt file, builds the system and user messages |
| `llm.py` | Chat model per provider, API key, reading the answer |
| `tests/` | Offline tests: model replaced by a stub, plus a fake local server |

## Tests

```
python -m pytest agent/tests benchmark/tests
```
