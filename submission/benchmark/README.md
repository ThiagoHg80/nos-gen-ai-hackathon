# NOS — Synthetic Anonymization Benchmark (50 documents)

- `input/`: 50 original UTF-8 `.txt` documents (40 pt-PT, 10 English).
- `ground_truth/`: corresponding reference documents with one `*` per whitespace-delimited sensitive token; whitespace-only lines removed.
- `annotations.json`: sensitive source spans with Python character offsets `[start,end)` and category labels.
- All personal identifiers are fictional/test values; names and institution names may resemble real entities by coincidence.

## Policy used for the reference
Names of individuals (including staff and relatives), individual names repeated in shorter form, contact addresses, telephone numbers, personal email addresses, tax identifiers, social media handles and IBANs are masked. Institutional names, generic city mentions, political party names without a personal identifier, occupations, medical diagnoses, ordinary processing dates, monetary amounts, case references and quoted instructions are preserved. Explicit membership-person links are broken by masking the person's name, not the party. This is a **benchmark-specific policy**, not a verified interpretation of the NOS hidden reference.

Ground truths were generated deterministically from sensitive placeholders, not by asking an LLM to censor arbitrary prose. **Manually review the originals and ground truths before using them as authoritative labels**, especially contextual references and ambiguous identifiers. Token masking counts whitespace-delimited components. All documents are 50–500 words.

## Validation
`annotations.json` spans refer to the *original* text; ground truths have empty/whitespace-only lines removed. Compare output with ground truth only after verifying the agent's formatting contract.

Check one answer file (run from `submission/`):

```
python -m benchmark.mask_syntax_validation benchmark/input/doc_001.txt answer.txt
python -m benchmark.mask_diff benchmark/input/doc_001.txt answer.txt
```

## Scorer
`scorer.py` runs a model + prompt over `input/` and compares each
answer with `ground_truth/`, word by word (word ids from
`mask_diff.py`). Run from `submission/`:

```
python -m benchmark.scorer --prompt prompts/prompt01.txt            # Gemini
python -m benchmark.scorer --provider local --prompt prompts/prompt01.txt
python -m benchmark.scorer --docs doc_001 doc_041 --limit 1
```

`--provider`, `--model`, `--base-url` and `--timeout` work as in
`python -m agent`.
Each call writes `runs/<time>_<model>_<prompt>/`:

- `doc_XXX.json`, one per document: model, prompt path and SHA-256,
  seconds, token usage, error (if the call failed), `syntax` (from
  `mask_syntax_validation.py`), `counts` (tp/fp/fn/tn), `metrics`
  (precision, recall, f1, accuracy, specificity, fpr, fnr), and the word
  id and text of every false positive and false negative.
- `doc_XXX.txt`, the model's answer exactly as returned (none when the
  call failed). Check it by hand with `mask_syntax_validation.py` or
  `mask_diff.py` against `input/doc_XXX.txt`.
- `summary.json`: counts added over all documents, and metrics from those
  totals.

A positive is a word the ground truth masks. A word the answer breaks
the rules at is counted as not masked and listed under `unaligned`.

A masked word keeps its punctuation (`República,` -> `*,`), and all 50
ground truths pass `mask_syntax_validation.py`. An answer that writes a
bare `*` instead still counts as masked in `mask_diff.py`, so detection is
scored separately, but it fails the syntax check.
