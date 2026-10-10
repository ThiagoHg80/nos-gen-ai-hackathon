# Agent

One Gemini call returns the whole document with personal data masked. The
answer is written exactly as returned, by default to `submission.txt`.

```
PDF -> raw_uncensored_document.txt -> prompt -> Gemini -> answer file
```

The agent does not check, score or record its answers. That is the job of
`benchmark/`, which you can run on any answer file afterwards.

## Setup

Run everything from `submission/`.

```
pip install pymupdf langchain-core pytest
```

Put the API key in `submission/.env` or in the environment:

```
export GEMINI_API_KEY="<your-key>"
```

The model is `gemini-3.6-flash`. Override it with `NOS_GEMINI_MODEL`.

## Prompt

The prompt is the instruction text sent as the system message. The
document is sent separately, as the user message between `<document>` tags.

By default the agent reads `submission/prompt.txt`. If that file is empty
it stops and says so. To start from the example:

```
cp benchmark/prompt_examples/system_prompt.txt prompt.txt
```

Or pass any prompt file with `--prompt`.

## Run

```
python -m agent --dry-run                  # show the prompt, no API call
python -m agent                            # call Gemini, write submission.txt
python -m agent --prompt benchmark/prompt_examples/system_prompt.txt
python -m agent --pdf other.pdf --out answer.txt
```

`--pdf` defaults to `raw_data/document_to_anonymize.pdf`, `--out` to
`submission/submission.txt`. Every run first extracts the PDF to
`submission/raw_uncensored_document.txt`.

When the answer goes to `submission.txt` and you passed a different
`--prompt`, that prompt is also copied into `prompt.txt`, so the two files
always match.

Nothing is written when the API returns an error after one retry, the
prompt is blocked, or the answer is cut off (`finishReason` is not `STOP`).

Exit codes: `0` answer written, `1` API failure, `2` not run (empty prompt
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
| `gemini.py` | API key, Gemini REST call, reading the answer |
| `tests/` | Offline tests, Gemini replaced by a stub |

## Tests

```
python -m pytest agent/tests benchmark/tests
```
