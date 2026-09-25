# PREREG P0c — benefit and cost of the rule "confirm before setting an optional boolean argument to true" (route (b), chosen by the author on 2026-09-24)

## Motivation
P0/P0b: prompt-level confirmation is blind to fluent semantic errors; yet the 7B model's four confirmations on neg_drop all asked about the flipped optional boolean.
Question: how many negation losses can a rule that needs no error detection and looks only at the **shape of the action** — "ask before setting any optional boolean argument to true" — block, and at what cost?

## Key design: positive-mirror cards
The gold boolean of all 42 existing cards is false (negation → false); on them the rule wins by construction at zero cost, a construction artefact.
Therefore add **42 positive-mirror cards** (`seed_items.POS_UTTERANCES`; same tool, same argument, the user **genuinely** wants that true; gold = the original card's flipped call).
The rule's cost = the fraction of positive cards on which a legitimate request is turned into a confirmation.

## Two implementations, both reported
- **prompted** (`confirm_optbool` gate): the rule is stated in the system prompt and executed by the LLM itself.
- **wrapper** (`analyze.optbool_wrapper`): a deterministic post-filter on the none-gate outputs; any optional boolean set to true → CONFIRM. Computed offline, no compute.

## Endpoints
- blocked(neg_drop) = CONFIRM rate on the neg_drop condition (the rule blocked the flip).
- Cost = CONFIRM rate on the 84 pooled cards, clean (42 negated) + clean_pos (42 positive); also reported separately.
- CF and WA on the other conditions (func_drop / content_sub / other_1w / other_1w_mid / other_intent) reported alongside.

## Decision (fixed before the run)
- **Worth a ≥ 120-card confirmatory experiment**: on at least one model the prompted version has blocked(neg_drop) ≥ 60% **and** pooled clean CF over the 84 cards ≤ 30%.
- **Close route (b)**: neither model satisfies this. The wrapper is reference only — by construction its block rate on negation loss should be near 100% and its cost near 50% (every positive card fires); if the prompted version's cost is not clearly below the wrapper's, the LLM is not using the transcript to discriminate and the rule amounts to confirming everything.
- Stated expectation: I expect the prompted version to approach the wrapper (cost ≈ 50%), i.e. **close**; the point of running is to measure this, not to hope it holds.

## Materials and compute
42 negated cards × 8 conditions + 42 positive cards × 1 condition = 378 trials × 2 gates (none, confirm_optbool) × 2 models; one Colab T4 session, $0. Label EXPLORATORY.

## Frozen hashes
b2b92cb262b56b996c02f730b351be6d74d07c9ec365a45cbce3e2bf32a52a27  seed_items.py
d42c28b9f919bd26ba158f27a6cbc614031e22dfa37e14955f0e1d3dfb1de40d  inject.py
f140a71cd1cb9bc122c2d3ad7b0eb096970b9d461c68ddc75c7e62dc134e111a  run_pilot.py
860942f97cb9e7fc5b7c8e173363d1e25f0b2573cff4a80056048e70662b5a5b  analyze.py
