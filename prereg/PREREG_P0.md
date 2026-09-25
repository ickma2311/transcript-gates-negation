# PREREG P0 — frozen 2026-09-23 (revised after the novelty check returned PROCEED WITH CAUTION with four harness defects; sha256 at the end; not changed after the run started)

## Question
Under **one edit per utterance with strictly equal per-card WER**, do four transcript error types (negation word lost / function word lost / content word replaced by a near-homophone / bystander speech inserted) differ in their effect on the **action outcome** of an LLM tool call; and do two cheap gates (confirmation prompt, speaker labels) differ in their detection rate across error types?

## Materials (frozen in `seed_items.py`; 42 cards × 6 conditions = 252 trials; `inject.py 0`)
- 42 spoken-style commands, each with exactly one negation whose deletion flips exactly one boolean/enum argument; gold and flipped calls are fixed by construction, no human annotation needed.
- Conditions: clean / neg_drop / func_drop / content_sub / other_1w (**each of these four has exactly one word-level edit per card, so per-card WER is identical = 1/L**; content_sub changed to single-word replacements only) / other_intent / other_chatter (3–6-word bystander fragment inserted, WER ≈ 0.38, dose control only).
- Gates: none / confirm (system prompt: if a recognition error is possible, reply `CONFIRM:` instead of calling; **a reply containing both CONFIRM and a tool call is scored by the call**, because the action would execute) / spktag (**run on every condition**: `[speaker 1]`/`[speaker 2]` labels, only speaker 1 declared to be the user; this is an oracle-label upper bound, not real speaker verification).
- Models: Qwen2.5-3B-Instruct (fp16), Qwen2.5-7B-Instruct-AWQ; vLLM, temperature 0.

## Primary endpoints (per model × condition × gate)
- **WA**: wrong-action rate = (WRONG_ACTION + FLIPPED + EXTRA_CALL) / n
- **CF**: confirmation rate = CONFIRM / n (under the confirm gate); CF on the clean condition is the false-alarm cost
- **Primary hypothesis H1 (gate × type interaction at equal WER)**: under the confirm gate, CF on **other_1w** exceeds CF on neg_drop by ≥ 25pp ("a fluent error is invisible"); the other_intent − neg_drop difference is reported only as secondary (different dose).
- **H2 (same WER, different harm)**: under no gate, WA on neg_drop exceeds WA on func_drop by ≥ 40pp (both are a single deletion).
- **H3 (source labels only fix insertions)**: spktag reduces WA on other_intent by ≥ 30pp relative to none, and does not raise WA on clean by > 5pp; **also report the WA difference on neg_drop between spktag and none** (expected ≈ 0, the other half of "only fixes insertions").

## Decision rules (fixed, not changed before the run)
- **GO**: at least one of the two models satisfies H1 and H2, and on that model the confirm gate's CF on clean is ≤ 25%.
- **STOP**: on both models the confirm gate's CF is < 10% on every error condition (prompt-level gate entirely ineffective, no interaction measurable) **or** H2 fails on both models (WA difference < 20pp: negation loss is no more harmful than function-word loss, construction assumption fails).
- Otherwise: **INCONCLUSIVE**; state what is missing and enter lite mode with only the smallest discriminating experiment.
- Labelling discipline: this pilot is **EXPLORATORY** throughout; it only allocates follow-up compute.

## Budget
One Colab T4 session: ~5 min vLLM install + ~630 prompts per model (≤ 5 min each) → total < 30 min. Cost $0.

## Known limitations (raised by the novelty reviewer, written before the run)
- Negation deletion necessarily flips the gold by construction; H2 only gives a magnitude; **the main result is the H1 interaction**.
- Speaker labels are an oracle setting; real speaker verification comes after P1.
- The endpoint is the **proposed** tool call (mock execution), not real-world consequences.
- 42 cards are hand-written templates with narrow coverage; after a GO, expand to ≥ 120 cards with blind-checked gold before any confirmatory experiment.

## Frozen hashes (2026-09-23, after fixing the four defects raised by the novelty check, before the GPU run)
09d5fb2a89b8139ba83499fe6c45b5d4e76b09499611f99ef6d6f276de891f03  seed_items.py
5f5bf193bad18fe20f31037cc70bdd4572e070233e76748533f094d89097a563  inject.py
de89bcc35de7c0132d56d9ae583d7c3939c530f5e314f5f2a1fd0ffa3ca5e840  run_pilot.py

## Correction note (2026-09-24, added after the run; frozen text above unchanged)
The materials line says "6 conditions = 252 trials" but lists seven conditions (other_1w was added when content_sub was restricted to single words); the frozen `inject.py 0` produced **7 conditions × 42 = 294 trials**, as recorded in `results/p0/*/trials.jsonl`. The bystander fragments described as "3–6 words" range from **2 to 6 words** in the saved trials.
