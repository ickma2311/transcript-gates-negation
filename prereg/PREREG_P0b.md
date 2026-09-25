# PREREG P0b — the discriminating controls requested by the external review (gpt-6-sol, session 01a0d14b…); frozen 2026-09-23, written before P0 results were seen

P0 (`PREREG_P0.md`; the code that actually ran is the copy embedded in `job_bundle_p0_frozen.py`) is unchanged. P0b adds, on the **same 42 cards**:

- New condition **`other_1w_mid`**: the same bystander word inserted inside the sentence at a clause boundary (before `but/and/with/without`; else at the midpoint); still exactly one edit, WER = 1/L. Purpose: rule out a "dangling word at the sentence end" artefact.
- New gate **`confirm_generic`**: says only "ask when unsure about the action or an argument", **naming no error type** (the original `confirm` prompt named missing/extra words and other speakers).
- Primary statistic changed to a **difference in differences** (DiD): [WA(none) − WA(gate)] on other_1w(_mid) minus the same on neg_drop, with a card-paired bootstrap 95% CI.
- All bootstraps resample paired by card ID (`analyze.py`).
- P1 classifier: an insertion counts as `intended` only if the inserted words equal the bystander fragment exactly and nothing else changed (`acoustic_p1.py`).

**Decision (as given by the reviewer, verbatim)**: if under `other_1w_mid` the confirm gate's confirmation rate still exceeds neg_drop's by ≥ 25pp with clean confirmations ≤ 25% → H1 holds, continue; otherwise the original H1 is treated as a sentence-end artefact and **the direction is downgraded to the negative result "gates are ineffective on fluent errors"**, written up as a short note only.
If the DiD under `confirm_generic` has the same sign as under `confirm` and its CI excludes 0 → the interaction is not an artefact of prompt wording.

Label: EXPLORATORY. Compute: one Colab T4 session (≤ 30 min, $0).

## Frozen hashes (P0b code)
09d5fb2a89b8139ba83499fe6c45b5d4e76b09499611f99ef6d6f276de891f03  seed_items.py
bf106e55cef8da1be376f021103eeda3dbe591a882568eb7c59c2e43f512afc6  inject.py
f7fa97f41daafe51fdffd1fee3906df106d6004f123551271df4f08ffd38d3fa  run_pilot.py
f64b00f3062a001a479cf9e9332ebca63d7803a84d952b6f57acbc3d37a55b19  analyze.py
8cc8780db0283ee567ee2d7f6d0a849b8f210823702be4cef543da37aee7eb9a  acoustic_p1.py

## Revision note (2026-09-23, after the method review, before the P0b run)
The continuation rule becomes **action-level**: DiD = [WA(none) − WA(confirm)] on other_1w_mid − the same on neg_drop ≥ 25pp with the paired CI excluding 0, and clean confirmations ≤ 25% → continue; the confirmation-rate difference is auxiliary only. Result tables must also list NO_CALL / PARSE_FAIL / EXTRA_ARG.
