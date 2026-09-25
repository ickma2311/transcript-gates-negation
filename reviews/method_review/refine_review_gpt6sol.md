## Method review

**Verdict: REVISE — overall 5.5/10.** The matched-WER construction and the paired DiD design are sound directions. The proposal is specific enough to run as an exploratory study, but the current design does not yet make the interaction matrix a convincing dominant paper contribution. I found no LLM outcome results in the inspected pilot materials.

| Criterion | Score | Judgment |
|---|---:|---|
| Problem Fidelity | 7/10 | It retains the frozen action-endpoint question. A single inserted bystander word may rarely change an action, however, so the matched-WER source condition may not represent the consequential bystander error in the anchor. |
| Method Specificity | 6/10 | Conditions, prompts, outcomes, and paired DiD are implemented. The confirmatory B2 comparison is less settled, and the plan alternates between **confirmation-rate differences** and **wrong-action DiD** as the main interaction. |
| Contribution Quality | 5/10 | A type × gate matrix *could* be the contribution. It is not established by a high confirmation rate alone: the gate must prevent wrong proposed actions at a measured confirmation cost. Oracle speaker labels support an upper-bound result, not a practical low-cost gate claim. |
| Feasibility | 5/10 | The pilot is compact. B2’s card creation, independent checking, multiple model families, and full cell matrix make the stated `<5 GPU-h` and two-week schedule optimistic. B1 needs at least 30 qualifying clips per type from only 42 cards. |
| Validation Focus | 5/10 | B0/B0b and B2 address the central claim. B1 measures rank transfer over only five types and uses selected Whisper outputs from synthetic audio; it does not, as written, verify that the **gate interaction** survives ASR. |
| Venue Readiness | 4/10 | There is a plausible compact paper if the action-level interaction survives the controls and broader cards. At present it is a preregistered proposal with narrow constructed data, rather than an Interspeech or ACL Findings result. |

**Drift Warning: Yes.** The [anchor](refine-logs/FINAL_PROPOSAL.md:5) asks which gate prevents which *wrong action* and at what cost, without reversal on ASR output. The [claim map](refine-logs/EXPERIMENT_PLAN.md:7) puts action-level DiD first, but [P0b’s continuation rule](pilot/PREREG_P0b.md:12) still hinges on a confirmation-rate gap. Also, P1’s bystander audio is appended at the end, while the in-sentence insertion is the key control against a sentence-end artifact. These are limits on what a positive result would prove.

**Simplification opportunities:** Delete B3 from the two-week paper plan. Keep the multiword insertion doses and detailed failure cases as brief descriptive material only if they explain the main matrix. Drop the hard Spearman ≥0.8 claim as a headline result; five selected type-level ranks are too coarse to carry a second contribution.

**Prioritized actions**

1. **Let B0/B0b decide the next tests.** Report baseline wrong-action rates, wrong-action DiD with paired CIs, confirmation rates, and clean-card cost together. If the one-word bystander condition seldom causes wrong actions, say the action-level interaction is uninformative even if confirmation rises.
2. **Make the outcome accounting exhaustive before interpreting DiD.** In the [scorer](pilot/run_pilot.py:82), a nonempty response with no parsed call and no `CONFIRM:` becomes `NO_CALL`; it reduces measured wrong actions without counting as a confirmation. Report that outcome, parse failures, and `EXTRA_ARG` alongside WA so abstention or parsing behavior cannot masquerade as gate benefit.
3. **Use B2 for a genuinely confirmatory matrix.** Freeze its cards, checked gold actions, model families, primary gate comparison, and action-level estimand before model runs. Compare the generic prompt’s benefit at its observed clean confirmation cost; matching prompt effects cannot be inferred from the sign of DiD alone.
4. **Keep B1’s claim within its evidence.** Report qualification yields and exclusions, and compare ranks on common cards where possible. Call the result transfer to *Whisper transcripts of synthetic audio*. If its end-appended bystander condition does not test the surviving B0b contrast, do not use B1 to claim that contrast holds acoustically.