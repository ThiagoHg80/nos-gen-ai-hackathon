# Benchmark tables - bench-mock-20261010T151746Z

- Mode: MOCK. MOCK run: these rows exercise the code path only and are NOT Gemini results.
- Reference status: PROVISIONAL (AI-drafted, not human-reviewed). Every accuracy figure below is PROVISIONAL.
- Planned trials: 9; statuses: {'CANDIDATE_VALID': 9}.
- N/A marks an undefined value; UNKNOWN marks usage the backend did not report. Neither is zero.

## Per-trial results

| agent | trial | status | structural_pass | pass_ignoring_trailing_ws | alignment_status | tp | fp | fn | precision | recall | f1 | exact_agreement | over_masking_rate | under_masking_rate | ambiguous_hidden_n | char_inserted | char_deleted | char_substituted | exact_reference_match | calls_submitted | prompt_tokens | output_tokens | model_latency_s | pipeline_latency_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 1 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 1 | UNKNOWN | UNKNOWN | 0.0003 | 0.0059 |
| B | 1 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 2 | UNKNOWN | UNKNOWN | 0.0005 | 0.0114 |
| C | 1 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 1 | UNKNOWN | UNKNOWN | 0.0002 | 0.0091 |
| A | 2 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 1 | UNKNOWN | UNKNOWN | 0.0003 | 0.006 |
| B | 2 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 2 | UNKNOWN | UNKNOWN | 0.0005 | 0.0114 |
| C | 2 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 1 | UNKNOWN | UNKNOWN | 0.0002 | 0.0092 |
| A | 3 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 1 | UNKNOWN | UNKNOWN | 0.0003 | 0.0052 |
| B | 3 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 2 | UNKNOWN | UNKNOWN | 0.0005 | 0.0108 |
| C | 3 | CANDIDATE_VALID | yes | yes | ALIGNED | 19 | 0 | 27 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 0 | 0 | 0 | 0 | no | 1 | UNKNOWN | UNKNOWN | 0.0002 | 0.009 |

## Aggregates per agent

| agent | trials_planned | trials_run | pipeline_failures | candidates_produced | valid_candidates | overall_valid_output_rate | evaluable_outputs | mean_precision_evaluable | mean_recall_evaluable | mean_f1_evaluable | mean_exact_agreement_evaluable | mean_over_masking_evaluable | mean_under_masking_evaluable | calls_submitted_total | http_attempts_total | prompt_tokens_total | output_tokens_total | mean_model_latency_s | mean_pipeline_latency_s | repeat_pairs_compared | max_words_differing_between_repeats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 3 | 3 | 0 | 3 | 3 | 1.0000 | 3 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 3 | 3 | UNKNOWN | UNKNOWN | 0.0003 | 0.0057 | 3 | 0 |
| B | 3 | 3 | 0 | 3 | 3 | 1.0000 | 3 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 6 | 6 | UNKNOWN | UNKNOWN | 0.0005 | 0.0112 | 3 | 0 |
| C | 3 | 3 | 0 | 3 | 3 | 1.0000 | 3 | 1.0000 | 0.4130 | 0.5846 | 0.8870 | 0.0000 | 0.5870 | 3 | 3 | UNKNOWN | UNKNOWN | 0.0002 | 0.0091 | 3 | 0 |
