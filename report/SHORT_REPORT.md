# Transcript-level gates cannot see a dropped negation: a pre-registered impossibility demonstration plus the measured behaviour of two Qwen models

**Scope statement.** 42 hand-constructed spoken-style commands plus 42 positive mirrors; two Qwen2.5 models (3B-Instruct fp16, 7B-Instruct-AWQ); text-level error injection (not real ASR); proposed (not executed) tool calls.
All numbers are **EXPLORATORY**. All four pilots were pre-registered and judged by their pre-registered rules. Version 1 of this note **failed** the pre-publication adversarial review (`KILL_ARGUMENT_round1.md`): it presented "the gates are blind" as a measured finding, whereas the adjudicator showed that, for transcript-only inputs, this is a property of the design. This version follows that adjudication: **state the impossibility first, then report behaviour.**

## One paragraph

In this constructed set, deleting the negation word leaves a transcript that is **verbatim identical to a legitimate positive command in 7 of 42 pairs** (with opposite gold calls); any gate that sees only the transcript and the tool schemas cannot recover the original intent on **those 7 pairs**. A further 11 pairs differ by a single "but"/"and" and the remaining 24 differ more; these 35 are reported only as behavioural observations.
The measured behaviour of both Qwen models is to act on the visible text (after negation deletion, 41/42 proposed calls disagree with the hidden original intent; positive mirrors are handled correctly in 39–42/42). The tested optional-boolean wrapper confirmed 97.6–100% of the positive mirrors in this constructed set.
What this note establishes is **possibility** (such collisions exist and the models act on them); how often real ASR produces them, and the deployment cost, are **unknown**.

## What this note can and cannot answer

- Can: on the 7 verbatim-identical pairs, does a transcript-level gate (text + schema) have any usable evidence? — No (impossibility, §2). What do the models do with such transcripts? — Follow them (§3). What does the one action-shape rule we tested cost on this constructed set? — Near-universal confirmation (§5).
- Cannot: what happens on real ASR output (no audio, n-best or confidence was in any gate's input); other model families; general conclusions such as "cheap gates fail"; the harm of entity substitution (the two scorers disagree; unresolved).

## 1  Design

- **Cards.** 42 commands, each containing exactly one negation whose removal flips exactly one optional boolean argument of the gold tool call; gold and the "transcript-faithful" call are fixed by construction. 23 tool schemas, 1–2 distractor tools per card.
- **Positive mirrors** (added in P0c). 42 natural phrasings of the same tool and argument where the user genuinely wants the boolean true; gold = the flipped call of the original card.
- **One-edit conditions** (per-card WER = 1/L, strictly equal): `neg_drop` negation deleted / `func_drop` a function word deleted / `content_sub` a content word replaced by a near-homophone / `other_1w` one bystander word appended / `other_1w_mid` the same word inserted inside the sentence. **Dose conditions** (WER ≈ 0.38): `other_intent` / `other_chatter` (multiword bystander fragments, 2–6 words in the saved trials).
- **Gates** (system prompts). `none`; `confirm` (names possible error types); `confirm_generic` (only "ask when unsure"); `spktag` (oracle speaker labels); `confirm_optbool` (rule: confirm before setting any optional boolean to true); and an offline deterministic version, `wrapper_optbool`. **Every gate's input is one transcript plus the schemas; no audio, n-best list or confidence.**
- **Scoring.** The pre-registered strict scorer (every gold argument must match) and a post-hoc lenient scorer (DEVIATION: function name plus all boolean/integer/enum arguments must match; free-text strings ignored). Both are reported.
- **Statistics.** WA = rate of proposed actions that disagree with the **hidden original intent** (WRONG_ACTION + FLIPPED + EXTRA_CALL); CF = confirmation rate; paired bootstrap 95% CIs over cards; temperature 0. Colab T4, $0.

## 2  Impossibility: after negation deletion, the transcript can be indistinguishable from a legitimate positive command

Comparing the 42 `neg_drop` transcripts with the 42 positive mirrors card by card:

| | Pairs |
|---|---|
| Transcript **verbatim identical**, opposite gold boolean (**the impossibility claim covers only these 7**) | **7 / 42** (me3, or3, cp2, df2, bf2, ri2, su2) |
| Differ by a single but/and (observable text; not covered by the impossibility claim) | 11 / 42 |
| Differ more | 24 / 42 |

Example, `me3`: both inputs read "book a one on one with priya on monday at nine and add a video link"; the gold `video_call` is false in one (the original said "don't") and true in the other.
For these 7 pairs, the raw outputs of both models under `none` and `confirm_optbool` are **byte-identical**. No gate that sees only these two inputs can decide differently on these 7 pairs — this is not a model failure; the information is absent from the input. For the other 35 pairs the textual differences are observable; for them this note reports measured behaviour only and makes no impossibility claim.

## 3  Model behaviour on the visible text (Table 1; lenient scoring; n = 42 per cell)

| Condition | WER | 3B WA | 7B WA |
|---|---|---|---|
| clean | 0 | 7.1 | 2.4 |
| clean_pos (positive mirrors) | 0 | 7.1 | 0.0 |
| **neg_drop** (disagreement with hidden intent) | 1/L | **97.6** | **97.6** |
| func_drop | 1/L | 14.3 | 4.8 |
| content_sub | 1/L | 19.0 (strict 95.2) | 9.5 (strict 92.9) |
| other_1w / other_1w_mid | 1/L | 21.4 / 14.3 | 9.5 / 11.9 |
| other_intent | ≈0.38 | 28.6 | 21.4 |

Composition of the 97.6% for `neg_drop`: 3B — FLIPPED 37, WRONG 3, EXTRA_CALL 1, CORRECT 1; 7B — FLIPPED 40, EXTRA_CALL 1, CORRECT 1. That is, **the models essentially execute the visible transcript faithfully**, and the visible transcript is the opposite of the original intent. On the 18 inputs that are identical or differ by one but/and, the number of pairs where the model gives the flipped call for `neg_drop` and the correct call for `clean_pos` is 17/18 (3B) and 18/18 (7B).
Pre-registered H2 (WA(neg_drop) − WA(func_drop) ≥ 40pp): +83.3pp [71.4, 92.9] and +92.9pp [85.7, 100]. This is a necessity of the construction (deleting the negation necessarily contradicts the hidden intent); it is reported only to show that WER is entirely insensitive to it.

## 4  Confirmation prompts and speaker labels (Table 2)

| Condition | 3B confirm | 3B generic | 7B confirm | 7B generic |
|---|---|---|---|---|
| clean (42 negated cards) | 0.0 | 0.0 | 0.0 | 0.0 |
| clean_pos (42 positive mirrors, P0d) | 0.0 | 0.0 | 7.1 | 0.0 |
| neg_drop | 0.0 | 0.0 | 9.5 | 2.4 |
| func_drop | 0.0 | 0.0 | 2.4 | 2.4 |
| content_sub | 0.0 | 0.0 | 0.0 | 0.0 |
| other_1w / other_1w_mid | 4.8 / 0.0 | 2.4 / 0.0 | 9.5 / 2.4 | 4.8 / 2.4 |
| other_intent / other_chatter | 31.0 / 16.7 | 28.6 / 14.3 | 21.4 / 23.8 | 16.7 / 16.7 |

Per §2, the low confirmation rate on the `neg_drop` row is **not evidence of a detection failure** — it is only meaningful next to the `clean_pos` row: the 7B `confirm` prompt confirms 7.1% of positive mirrors and 9.5% of `neg_drop` transcripts (aggregate rates over two 42-card sets whose texts mostly differ); on the 7 verbatim-identical pairs the raw outputs are identical, as the impossibility requires. For 3B both rows are 0%.
Pre-registered H1 (CF(other_1w) − CF(neg_drop) ≥ 25pp) does not hold: +4.8pp [0, 11.9] and +0.0pp [−11.9, 11.9]. The confirmation prompts ask more often on the longer bystander fragments (16.7–31.0%), but those fragments also have ~4× the WER; length, WER, position and content vary together, so no single cause can be isolated.
The four 7B confirmations on `neg_drop` all asked about the flipped argument (anecdotal, n = 4).
Oracle speaker labels: WA reduction on `other_intent` of +2.4pp [−11.9, 16.7] (3B) and +11.9pp [0, 23.8] (7B) (pre-registered 30pp not met); on clean +0.0 / +2.4pp; on clean_pos −2.4pp for 3B (4.8 vs 7.1) and +2.4pp for 7B (2.4 vs 0.0), both within noise.

## 5  An action-shape rule: it blocks the flips, at the cost of near-universal confirmation (Table 3, P0c)

| | 3B prompted | 3B wrapper | 7B prompted | 7B wrapper |
|---|---|---|---|---|
| Confirms on neg_drop (blocks the flip) | 0.0 | 97.6 | 2.4 | 97.6 |
| Confirms on clean_pos (legitimate request intercepted) | 0.0 | **97.6** | 0.0 | **100.0** |

The rule "confirm before setting any optional boolean to true": the prompted version is almost never executed; the deterministic version blocks 97.6% by construction, but because every positive mirror requires exactly that true value, it intercepts 97.6–100% of the legitimate positive requests **on this constructed set**.
This is a cost measurement for **this one rule on this set**, not a conclusion about "detection" nor a general conclusion about action-level rules; the pooled 51.2% comes from an artificial 1:1 mix and is not a deployment cost. Pre-registered decision: CLOSE.

## 6  What the data supports (wording narrowed per result-to-claim and the adversarial review)

1. On these 42 constructed pairs, the post-deletion transcript is verbatim identical to a legitimate positive command in 7 pairs (opposite gold); a transcript-level gate has no usable evidence on **those 7** (impossibility). The other 35 pairs are textually distinguishable and are reported as behaviour only.
2. Both Qwen models act on the visible text: `neg_drop` disagrees with the hidden intent in 41/42; positive mirrors are correct in 39–42/42. All percentages are conditional on this constructed set and carry no prevalence meaning.
3. The two tested confirmation prompts rarely ask on the constructed one-word errors (≤ 9.5%); their cost on the negated and positive cards is given by the two rows of Table 2; the pre-registered "bystander insertion − negation" confirmation gap is absent.
4. Oracle speaker labels did not reach the pre-registered 30pp reduction.
5. The tested optional-boolean wrapper blocks 97.6% of the flips on this set at the cost of intercepting 97.6–100% of the positive mirrors; the prompted version is almost never executed. The frequency of such collisions in real ASR, and the deployment cost, were not measured.

## 7  Not claimed

The harm of entity substitution (strict 93–95% vs lenient 9.5–19%, not blind-adjudicated); "cheap gates fail in general"; "a model ignores the labels"; treating 51.2% as a deployment cost; any conclusion about real ASR or executed actions.

## 8  Deviations and process

- Scorer: the strict scorer over-penalised free-text formatting (28.6% / 16.7% of clean calls mis-scored); a lenient scorer was added post hoc and both are reported (DEVIATION); the lenient scorer cannot measure entity substitution.
- The first P0c run was lost to a Colab client timeout; re-run with streamed output; frozen hashes unchanged. P0d ran only the three prompt gates on the positive mirrors (`PREREG_P0d.md`).
- Cards were hand-written by the author with AI assistance and not blind-checked; single model family; prompt-level gates only.
- Review chain (all GPT-6 Sol via the Codex CLI): novelty check PROCEED WITH CAUTION (7/10, 6/10) → research review PROCEED (6/10) → method review REVISE (5.5/10) → result-to-claim partial → **kill-argument round 1 FAIL (this version was rewritten accordingly) → round 2 WARN (0 unresolved, 4 partially answered, all wording; the three edits in `KILL_ARGUMENT_round2.md` were applied)**.

## 9  Reproducibility

`../code/`: `seed_items.py`, `inject.py`, `run_pilot.py`, `rescore.py`, `analyze.py`, `pair_check.py`; pre-registrations `PREREG_P0.md` / `P0b` / `P0c` / `P0d` (with SHA-256) in `../prereg/`; the exact jobs that ran, `job_bundle_p0_frozen.py` / `p0b` / `p0c` / `p0d`; raw outputs in `../results/`. `python code/analyze.py results/<run>` recomputes the strict-scoring tables from `results.jsonl`; for p0 and p0b it also prints the pre-registered contrasts with paired-bootstrap CIs and the decision, for p0c the optional-boolean rule evaluation, and for p0d the descriptive table only; to recompute the lenient tables, copy each `results_lenient.jsonl` over `results.jsonl` in a scratch copy first. `python code/pair_check.py results/p0c results/p0` recomputes the pair counts (7 / 11 / 24), the identical-output check, the 17/18 and 18/18 figures, and the FLIPPED breakdown.
