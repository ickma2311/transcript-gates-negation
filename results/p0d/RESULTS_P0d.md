# RESULTS P0d — 2026-09-24 (EXPLORATORY; Colab T4 957 s; PREREG_P0d; 42 positive-mirror cards × 4 gates × 2 models)

Cost of the confirmation prompts and speaker labels on **legitimate positive requests** (lenient scoring; strict scoring in parentheses):

| Model | Gate | CF | WA | OK |
|---|---|---|---|---|
| Qwen2.5-3B-Instruct | none | 0.0 (0.0) | 7.1 (26.2) | 92.9 (69.0) |
| Qwen2.5-3B-Instruct | confirm | 0.0 (0.0) | 7.1 (23.8) | 92.9 (71.4) |
| Qwen2.5-3B-Instruct | confirm_generic | 0.0 (0.0) | 4.8 (21.4) | 95.2 (73.8) |
| Qwen2.5-3B-Instruct | spktag | 0.0 (0.0) | 4.8 (23.8) | 95.2 (71.4) |
| Qwen2.5-7B-Instruct-AWQ | none | 0.0 (0.0) | 0.0 (21.4) | 100.0 (73.8) |
| Qwen2.5-7B-Instruct-AWQ | confirm | 7.1 (7.1) | 0.0 (14.3) | 92.9 (73.8) |
| Qwen2.5-7B-Instruct-AWQ | confirm_generic | 0.0 (0.0) | 0.0 (21.4) | 100.0 (73.8) |
| Qwen2.5-7B-Instruct-AWQ | spktag | 0.0 (0.0) | 2.4 (16.7) | 97.6 (76.2) |

Reading: the 7B confirm prompt confirms 7.1% of positive cards and 9.5% of neg_drop transcripts (aggregate rates over two 42-card sets whose texts mostly differ; on the 7 verbatim-identical pairs the raw outputs are identical, as the impossibility in §2 of the note requires). For 3B both prompts are 0% on the positive cards.
