# RESULT-TO-CLAIM EVALUATION — ideas/asr_toolcall (three exploratory pilots)

You are the cross-model judge. Claude (the executor) collected the results and proposes the claims below for a short negative-result / diagnostic report. Your job: judge what the data actually supports. Do NOT inflate. A result on 42 hand-built cards and two Qwen models does not support a general claim; say exactly how narrow the supportable statement is.

You may (and should) read and re-run the artifacts yourself, CPU only:
- Pre-registrations: `pilot/PREREG_P0.md`, `pilot/PREREG_P0b.md`, `pilot/PREREG_P0c.md` (frozen hashes inside)
- Result summaries: `pilot/RESULTS_P0.md`, `pilot/RESULTS_P0b.md`, `pilot/RESULTS_P0c.md`
- Raw model outputs: `pilot/colab_out/<model>/results.jsonl` (P0), `pilot/colab_out_p0b/`, `pilot/colab_out_p0c/` (fields: item_id, condition, gate, outcome, raw). `results_lenient.jsonl` = post-hoc lenient rescoring.
- Code: `pilot/seed_items.py` (42 cards + 42 positive mirrors), `pilot/inject.py`, `pilot/run_pilot.py` (strict scorer), `pilot/rescore.py` (lenient scorer, DEVIATION), `pilot/analyze.py` (`python analyze.py <dir>` prints tables, paired-bootstrap CIs, and the P0c rule evaluation; for lenient numbers copy each `results_lenient.jsonl` to a dir as `results.jsonl` next to `trials.jsonl`).
- Context: `idea-stage/IDEA_REPORT.md` (landscape + reviews), `refine-logs/refine_review_gpt6sol.md`.

## Setup (all three pilots)
Cards: 42 spoken-style commands, each with exactly one negation whose removal flips exactly one optional boolean of the gold tool call; 23 tool schemas; gold and "transcript-faithful flipped call" fixed by construction. Conditions with exactly one word-level edit (per-card WER = 1/L identical across types): neg_drop, func_drop, content_sub (near-homophone), other_1w (one bystander word appended), other_1w_mid (same word inside the sentence at a clause boundary); higher-dose conditions: other_intent / other_chatter (3–6-word bystander fragment, WER ≈ 0.38). Gates (system prompts): none, confirm (names error types), confirm_generic (does not), spktag (oracle [speaker 1]/[speaker 2] labels), confirm_optbool (rule: confirm before setting any optional boolean to true). P0c adds 42 positive-mirror cards (clean_pos) where the optional boolean is genuinely wanted, and a deterministic post-filter "wrapper_optbool" computed offline on none-gate outputs. Models: Qwen2.5-3B-Instruct (fp16) and Qwen2.5-7B-Instruct-AWQ, vLLM, temperature 0. Metrics: WA = wrong-action rate (WRONG_ACTION+FLIPPED+EXTRA_CALL), CF = confirmation rate. Scoring: strict (pre-registered; over-penalises free-text argument formatting) and lenient (post hoc DEVIATION: function name + all boolean/int/enum args must match, free strings ignored; under-counts content_sub harm). Both are reported.

## Intended claims (for the short report) with the cited numbers
Evidence pre-check (deterministic, `.aris/evidence_precheck.json`): all 24 cited values below were found in their source files (status = verified for every id). "verified" only means the number exists; you judge whether it supports the claim.

- **K1 (same WER, different harm).** At identical per-card WER, negation drop yields wrong actions 97.6% (both models, lenient) vs function-word drop 14.3% (3B) / 4.8% (7B); paired-bootstrap difference +83.3pp [71.4, 92.9] and +92.9pp [85.7, 100]. Caveat we already state: the flip is by construction, so this is a magnitude, not a discovery.
- **K2 (prompt-level confirmation is blind to fluent one-word errors).** Under the confirm gate, CF on neg_drop is 0.0% (3B) / 9.5% (7B); on other_1w 4.8 / 9.5; on other_1w_mid 0.0 / 2.4; on content_sub 0 / 0; on func_drop 0 / 2.4; false confirmations on clean = 0.0% both models. Pre-registered H1 (CF gap other_1w − neg_drop ≥ 25pp): +4.8pp [0, 11.9] and +0.0pp [−11.9, 11.9] → refuted. The non-leading prompt (confirm_generic) gives the same pattern. Action-level DiD all ≤ 0 (7B other_1w_mid: −9.5pp [−19.0, −2.4]).
- **K3 (the gate reacts only to multi-word incoherence).** CF on other_intent 31.0 / 21.4%, other_chatter 16.7 / 23.8%, at WER ≈ 0.38 — i.e., only where WER is not matched.
- **K4 (oracle speaker tags).** WA reduction on other_intent under spktag: +2.4pp [−11.9, 16.7] (3B) and +11.9pp [0, 23.8] (7B); pre-registered H3 (≥ 30pp) refuted; the 3B model ignores the labels.
- **K5 (an action-shape rule cannot separate "wanted true" from "lost negation").** Prompted rule confirm_optbool: blocked(neg_drop) 0.0 / 2.4%, CF on clean_pos 0 / 0% — the rule is not executed at all. Deterministic wrapper: blocked 97.6 / 97.6% but CF on clean_pos 97.6 / 100% and pooled-84 CF 51.2%. Pre-registered decision rule (blocked ≥ 60% and pooled CF ≤ 30%) → CLOSE.
- **K6 (methodological).** Strict scorer marked 28.6 / 16.7% of clean calls wrong, almost all free-text formatting ("four o'clock" vs "4 o'clock"); we report both scorers and label the lenient one a deviation. Also: 7B's four neg_drop confirmations all asked about the flipped parameter (n = 4, anecdotal).
- **Overall narrative we want to make:** "At matched WER, harm concentrates in fluent semantic errors (negation, entity), and cheap transcript- or action-shape-level gates cannot see them: a lost negation has no fingerprint at the action level." Scope: two Qwen models, 42 constructed cards, text-level injection, proposed (not executed) calls, EXPLORATORY.

## Known caveats (be harder than these)
Constructed cards by the executor (no blind check); n = 42 per cell; single model family; prompt-level gates only; text-level injection not real ASR; content_sub harm under-counted by the lenient scorer; the "matched WER" one-word bystander condition may not represent consequential bystander errors (the refine reviewer predicted this and P0 confirmed it); scorer changed post hoc; the K5 prompted-rule non-compliance might be a prompt-wording artefact (only one wording tested).

## Please return, in this exact structure
For EACH of K1–K6 and for the Overall narrative:
1. claim_supported: yes | partial | no
2. what_results_support
3. what_results_dont_support
4. missing_evidence
5. suggested_claim_revision (the sentence we should actually write)
6. next_experiments_needed (only if cheap and decision-relevant; "none" is a fine answer for a negative-result note)
7. confidence: high | medium | low
Then: a list of any number you recomputed that does NOT match what is cited above (say "all matched" if so), and a one-line final verdict: `VERDICT: yes | partial | no` for the Overall narrative.
Be honest. Do not manufacture findings; say plainly when a claim is fine.
