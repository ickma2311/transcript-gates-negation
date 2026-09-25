# Transcript-level gates cannot see a dropped negation: a pre-registered impossibility demonstration plus measured behaviour of two Qwen models

An exploratory, pre-registered pilot (four runs, 2026-09-23/24, free Colab T4, no paid API) on a cascaded voice-agent
question: when an ASR system drops a negation word, can a cheap gate that sees only the transcript and the tool schemas
catch it before the LLM proposes the wrong tool call?

**Scope, stated up front:** 42 hand-constructed spoken-style commands plus 42 positive mirrors, two Qwen2.5 models
(3B-Instruct fp16, 7B-Instruct-AWQ), text-level error injection (not real ASR), proposed (not executed) tool calls.
All numbers are EXPLORATORY. The first version of this note failed an adversarial pre-publication review (round 1,
`reviews/kill_argument_round1/`) for presenting the gate result as a measured detection failure; the current framing
follows that adjudication. Not affiliated with any vendor.

## The one-paragraph result

In this constructed set, deleting the negation makes the transcript **verbatim identical** to a legitimate positive
command in 7 of 42 pairs (opposite gold tool calls); 11 more differ by one "but"/"and" and 24 differ more. A gate that
sees only transcript + schema cannot recover the original intent on **those 7 pairs** — a property of the inputs, not of a
model; the other 35 are reported only as observed behaviour. Across all 42 cards, both Qwen models largely act on the visible text
(41/42 negation-dropped transcripts yield a proposed action that disagrees with the hidden original intent — 37/42 (3B) and 40/42
(7B) are exactly the transcript-faithful flipped call, the rest are other wrong actions or extra calls; 39–42/42 positive mirrors
yield the correct call). Two "confirm when unsure" system prompts confirm at ≤ 9.5% on one-word errors and at 0–7.1% on the
positive mirrors (aggregate rates over the two 42-card sets, whose texts mostly differ; on the 7 verbatim-identical pairs the
raw outputs are identical, so those pairs necessarily get the same decision). The tested deterministic rule (confirm before setting any
optional boolean to true) blocks 97.6% of the flips in this set but also confirmed 97.6–100% of the positive mirrors, which by
construction require that boolean. This establishes possibility only; how often real ASR produces such collisions, and the
deployment cost, are unknown.

## What the data supports (and only this)

1. On the 7 verbatim-identical pairs (opposite gold), transcript-only gates have no usable evidence of the deleted
   negation. Impossibility on those 7, not a measurement; the other 35 pairs have observable textual differences.
2. Both models follow the visible text: 41/42 negation-dropped transcripts disagree with the hidden original intent;
   positive mirrors are handled correctly 39–42/42. All percentages are conditional on this constructed set.
3. The tested confirmation prompts rarely ask on one-word errors (≤ 9.5%); their cost on positive mirrors is 0–7.1%;
   the pre-registered "bystander-insertion − negation" confirmation gap (≥ 25pp) did not appear (+4.8pp [0, 11.9],
   +0.0pp [−11.9, 11.9]). They ask more on longer bystander fragments (16.7–31.0%), whose WER is also ~4× higher.
4. Oracle speaker labels missed the pre-registered 30pp wrong-action reduction (+2.4pp [−11.9, 16.7]; +11.9pp [0, 23.8]).
5. The tested optional-boolean wrapper blocks the flips in this set at the cost of confirming 97.6–100% of the positive
   mirrors; the prompted version was almost never executed (0.0 / 2.4%). No real-ASR incidence or deployment cost is measured.

Also reported, as a construction-determined magnitude only: at identical per-card WER (one edit each), negation
deletion disagreed with the original intent in 97.6% of cases versus 14.3% / 4.8% for function-word deletion.

## What it does not support

Anything about real ASR output (no audio, n-best or confidence was available to any gate), other model families,
"cheap gates fail in general", entity-substitution harm (unresolved between the strict scorer, 93–95%, and the lenient
one, 9.5–19%), or executed actions.

## Layout

- `report/SHORT_REPORT.md` — the note (English, canonical). Chinese versions of the note, the pre-registrations, the result summaries and the result-to-claim ledger are under `zh/` (the note was first written in Chinese and translated; the failed version 1 exists only in Chinese, `zh/report/SHORT_REPORT_v1_failed_round1.md`)
- `prereg/` — four frozen pre-registrations (P0, P0b and P0c list code hashes; P0d refers to P0c's unchanged code hash), translated from the Chinese originals in `zh/prereg/` (hash lines identical)
- `code/` — cards, injector, runner (strict scorer), lenient rescorer (post-hoc deviation), analysis, the exact self-contained Colab jobs that ran
- `results/` — result summaries and all raw model outputs (`results.jsonl`, `results_lenient.jsonl`, `trials.jsonl`)
- `reviews/` — prompts and verbatim outputs of every external review (novelty check, research review, method review,
  result-to-claim, kill-argument rounds 1 and 2), all GPT-6 Sol via the Codex CLI

## Reproduce

`python code/analyze.py results/p0` (also `p0b`, `p0c`, `p0d`) reprints the strict-scoring tables from `results.jsonl`; for p0 and p0b it also prints the pre-registered contrasts with
paired-bootstrap CIs and the decision, for p0c the optional-boolean rule evaluation, and for p0d the descriptive table only; for the lenient tables, copy each `results_lenient.jsonl` over `results.jsonl` in a scratch copy first.
`python code/pair_check.py results/p0c results/p0` recomputes the pair counts and the FLIPPED breakdown. (`analyze.py` received a guard on 2026-09-24, after the release check, so that runs without the pre-registered cells print a descriptive table only; the experiment code is unchanged.) `python code/inject.py 0`
rebuilds the 378 trials.

## Deviations, honestly

- The pre-registered strict scorer mis-scored 28.6% / 16.7% of clean calls on free-text formatting; a lenient scorer was
  added post hoc and both are reported. The lenient one cannot measure entity-substitution harm.
- The first P0c run was lost to a Colab client timeout; re-run with streamed output, frozen hashes unchanged.
- Cards were written by the author with AI assistance and not blind-checked; single model family; prompt-level gates only.

## Disclosure

Experiments, analysis and writing were done with AI assistance (Claude Code as executor; GPT-6 Sol as independent
reviewer at every gate). Every experiment statistic here was mechanically checked to exist in the result files and re-derived by a
reviewer from the raw outputs; review scores and verdicts come from the review records in `reviews/`, and the $0 cost is a
statement about the free Colab tier, not a measured quantity. License: MIT.

Note: review transcripts under `reviews/` are verbatim except that absolute local paths were rewritten to repository-relative ones.
