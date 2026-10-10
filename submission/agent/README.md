# Agent

One model call returns the whole document with personal data masked. The
answer is written exactly as returned, by default to `submission.txt`. The
model is Gemini, or any local OpenAI-compatible server for testing.

```
PDF -> raw_uncensored_document.txt -> prompt -> LLM -> answer file
```

The agent does not check, score or record its answers. The benchmark folder
currently contains synthetic data, not executable evaluation modules.
Use the optional preflight and the project evaluation tools separately.

## Setup

Run everything from `submission/`.

```
python -m pip install PyMuPDF==1.27.2.3 langchain-core==1.6.9 langchain-google-genai==4.4.1 langchain-openai==1.7.0 pytest==9.1.1
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
it stops and says so. The prompts directory is not present in the current
checkout. Pass an existing reviewed file
with `--prompt`.

## Run

```
python -m agent --dry-run                  # show the prompt, no API call
python -m agent                            # call Gemini, write submission.txt
python -m agent --prompt "path/to/reviewed_prompt.txt" --out candidate_review.txt
python -m agent --pdf other.pdf --out answer.txt
```

`--pdf` defaults to `raw_data/document_to_anonymize.pdf`, `--out` to
`submission/submission.txt`. Every run first extracts the PDF to
`submission/raw_uncensored_document.txt`.

When the answer goes to `submission.txt` and you passed a different
`--prompt`, that prompt is also copied into `prompt.txt`, so the two files
always match.

No new answer file is written when the model call fails or the
answer is cut off (its `finish_reason` is not `STOP`). PDF extraction happens
before the model call and may already have written raw text.

Exit codes: `0` answer written, `1` model failure, `2` not run (empty prompt
or no API key).

## Evaluate an answer

```
python -B security_preflight.py --document candidate_review.txt
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
python -m pytest agent/tests NOS_Three_Agents -ra -o addopts="-p no:cacheprovider"
```

The locally verified interpreter is Python 3.12.7. Use one virtual environment
and the same interpreter for pip and execution. The full project setup,
optional privacy requirements, recorded checks and competition delivery
instructions are in [the project README](../NOS_Three_Agents/README.md).
Replace example prompt paths with actual reviewed files. The preflight is
optional and does not establish anonymity or validate document formatting.
