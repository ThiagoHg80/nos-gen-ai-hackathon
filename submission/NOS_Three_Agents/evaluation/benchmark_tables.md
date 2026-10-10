# Benchmark tables - bench-live-20261010T151834Z

- Mode: LIVE. BLOCKED before any request was sent: BLOCKED: no API key in GEMINI_API_KEY / GOOGLE_API_KEY (environment or .env) No Gemini call was made; every row is a NOT_RUN placeholder, not a result.
- Reference status: PROVISIONAL (AI-drafted, not human-reviewed). Every accuracy figure below is PROVISIONAL.
- Planned trials: 9; statuses: {'NOT_RUN': 9}.
- N/A marks an undefined value; UNKNOWN marks usage the backend did not report. Neither is zero.

## Per-trial results

| agent | trial | status | structural_pass | pass_ignoring_trailing_ws | alignment_status | tp | fp | fn | precision | recall | f1 | exact_agreement | over_masking_rate | under_masking_rate | ambiguous_hidden_n | char_inserted | char_deleted | char_substituted | exact_reference_match | calls_submitted | prompt_tokens | output_tokens | model_latency_s | pipeline_latency_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 1 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| B | 1 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| C | 1 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| A | 2 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| B | 2 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| C | 2 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| A | 3 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| B | 3 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| C | 3 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Aggregates per agent

| agent | trials_planned | trials_run | pipeline_failures | candidates_produced | valid_candidates | overall_valid_output_rate | evaluable_outputs | mean_precision_evaluable | mean_recall_evaluable | mean_f1_evaluable | mean_exact_agreement_evaluable | mean_over_masking_evaluable | mean_under_masking_evaluable | calls_submitted_total | http_attempts_total | prompt_tokens_total | output_tokens_total | mean_model_latency_s | mean_pipeline_latency_s | repeat_pairs_compared | max_words_differing_between_repeats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 3 | 0 | 0 | 0 | 0 | N/A | 0 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 0 | N/A |
| B | 3 | 0 | 0 | 0 | 0 | N/A | 0 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 0 | N/A |
| C | 3 | 0 | 0 | 0 | 0 | N/A | 0 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 0 | N/A |
