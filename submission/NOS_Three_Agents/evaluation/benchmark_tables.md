# Benchmark tables - bench-live-20261010T170036Z

- Mode: LIVE. LIVE Gemini run.
- Reference status: PROVISIONAL (AI-drafted, not human-reviewed). Every accuracy figure below is PROVISIONAL.
- Planned trials: 9; statuses: {'CANDIDATE_INVALID': 2, 'PIPELINE_FAILED': 2, 'CANDIDATE_VALID': 1, 'NOT_RUN': 4}.
- N/A marks an undefined value; UNKNOWN marks usage the backend did not report. Neither is zero.

## Per-trial results

| agent | trial | status | structural_pass | pass_ignoring_trailing_ws | alignment_status | tp | fp | fn | precision | recall | f1 | exact_agreement | over_masking_rate | under_masking_rate | ambiguous_hidden_n | char_inserted | char_deleted | char_substituted | exact_reference_match | calls_submitted | prompt_tokens | output_tokens | model_latency_s | pipeline_latency_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 1 | CANDIDATE_INVALID | no | yes | ALIGNED | 46 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0 | 0 | 1 | 0 | no | 1 | 1988 | 798 | 61.1475 | 61.1546 |
| B | 1 | PIPELINE_FAILED | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 1 | UNKNOWN | UNKNOWN | 3.9289 | 3.9329 |
| C | 1 | PIPELINE_FAILED | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 1 | UNKNOWN | UNKNOWN | 2.3521 | 2.3554 |
| A | 2 | CANDIDATE_VALID | yes | yes | ALIGNED | 46 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0 | 0 | 0 | 0 | yes | 1 | 1988 | 799 | 74.165 | 74.1713 |
| B | 2 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| C | 2 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| A | 3 | CANDIDATE_INVALID | no | yes | ALIGNED | 46 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0 | 0 | 1 | 0 | no | 1 | 1988 | 798 | 53.5057 | 53.5124 |
| B | 3 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| C | 3 | NOT_RUN | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Aggregates per agent

| agent | trials_planned | trials_run | pipeline_failures | candidates_produced | valid_candidates | overall_valid_output_rate | evaluable_outputs | mean_precision_evaluable | mean_recall_evaluable | mean_f1_evaluable | mean_exact_agreement_evaluable | mean_over_masking_evaluable | mean_under_masking_evaluable | calls_submitted_total | http_attempts_total | prompt_tokens_total | output_tokens_total | mean_model_latency_s | mean_pipeline_latency_s | repeat_pairs_compared | max_words_differing_between_repeats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 3 | 3 | 0 | 3 | 1 | 0.3333 | 3 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 3 | 3 | 5964 | 2395 | 62.9394 | 62.9461 | 3 | 0 |
| B | 3 | 1 | 1 | 0 | 0 | 0.0000 | 0 | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 | UNKNOWN | UNKNOWN | 3.9289 | 3.9329 | 0 | N/A |
| C | 3 | 1 | 1 | 0 | 0 | 0.0000 | 0 | N/A | N/A | N/A | N/A | N/A | N/A | 1 | 1 | UNKNOWN | UNKNOWN | 2.3521 | 2.3554 | 0 | N/A |
