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

This directory contains data, not runnable benchmark modules or a tests/
directory in the current checkout. Setup and the implemented evaluation
commands are documented in [the project README](../NOS_Three_Agents/README.md).
