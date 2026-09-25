I reran `analyze.py` on the raw results and reapplied both scorers to all 5,964 saved model outputs. Every stored outcome label matched the CPU rescoring. All 42 cards per pilot also had equal per-card WER across the one-word conditions. The judgments below concern **proposed tool calls from constructed text**, not real ASR or executed actions.

### K1 — Same WER, different harm

1. **claim_supported:** yes, within these cards.
2. **what_results_support:** Under no gate, lenient wrong-action rates were 97.6% for negation deletion in both models, versus 14.3% (3B) and 4.8% (7B) for function-word deletion. The cited paired differences and intervals match.
3. **what_results_dont_support:** A general ranking of ASR error types. The negation cards were constructed so deletion changes the intended boolean.
4. **missing_evidence:** Independently checked, diverse cards and real ASR outputs.
5. **suggested_claim_revision:** “On 42 constructed commands at identical per-card word error rate, deleting the negation produced far more wrong proposed calls than deleting a function word in both tested Qwen models.”
6. **next_experiments_needed:** none for an exploratory note.
7. **confidence:** high.

### K2 — Confirmation on fluent one-word errors

1. **claim_supported:** partial.
2. **what_results_support:** The cited confirmation rates match. The preregistered ≥25 percentage-point gap between one-word bystander insertion and negation deletion did not appear. The sentence-internal and generic-prompt controls also had low confirmation rates.
3. **what_results_dont_support:** “Blind” as a general capability claim. The tests cover two prompt wordings and these cards. Clean confirmation of 0% also fits a gate that rarely asks at all.
4. **missing_evidence:** Other models, prompt designs, and real ASR transcripts before generalizing.
5. **suggested_claim_revision:** “In these two Qwen models, the tested confirmation prompts rarely requested clarification for the constructed one-word errors, including negation deletion, and the preregistered bystander-versus-negation confirmation gap was absent.”
6. **next_experiments_needed:** none for the negative-result note.
7. **confidence:** high for the measured pattern; medium for its interpretation.

### K3 — Multi-word insertions

1. **claim_supported:** partial.
2. **what_results_support:** The cited 16.7–31.0% confirmation rates for the multi-word bystander conditions match and exceed most one-word rates.
3. **what_results_dont_support:** “Only” multi-word *incoherence* caused the response. Length, WER, position, and content change together; some one-word cases were confirmed.
4. **missing_evidence:** Matched-dose controls to isolate incoherence.
5. **suggested_claim_revision:** “The tested confirmation prompt asked more often on the longer bystander fragments than on the one-word edits; those fragments also had substantially higher WER.”
6. **next_experiments_needed:** none unless the report seeks a causal explanation.
7. **confidence:** high for rates; medium for interpretation.

### K4 — Oracle speaker tags

1. **claim_supported:** partial.
2. **what_results_support:** The cited wrong-action reductions and paired intervals match; neither model reached the preregistered 30-point target.
3. **what_results_dont_support:** “The 3B model ignores the labels.” Its outputs changed, and 3B also produced `NO_CALL` on 6/42 untagged versus 4/42 tagged `other_intent` cases. The experiment does not establish practical speaker verification performance.
4. **missing_evidence:** Case-level attribution of label use and real speaker labels, if pursuing a speaker-gate claim.
5. **suggested_claim_revision:** “Oracle speaker tags did not meet the preregistered 30-point wrong-action reduction on multi-word bystander intent: the measured reductions were 2.4 points (3B) and 11.9 points (7B).”
6. **next_experiments_needed:** none for this note.
7. **confidence:** high.

### K5 — Optional-boolean action rule

1. **claim_supported:** partial.
2. **what_results_support:** All cited rates match, and both implementations fail the preregistered decision rule. The 42 positive mirrors have the same **gold tool calls** as the corresponding negation-deletion cases, so a rule seeing only that exact call cannot distinguish those paired intentions.
3. **what_results_dont_support:** A universal claim that every action-level gate must fail, or that Qwen never follows such rules. Only one prompted wording and one deterministic boolean filter were tested. The 51.2% pooled confirmation cost comes from an artificially balanced set of 42 negative and 42 positive requests; it is not a deployment rate.
4. **missing_evidence:** A representative prevalence of legitimate `true` requests for a real-world cost estimate.
5. **suggested_claim_revision:** “On these paired cards, the prompted optional-boolean rule almost never blocked negation deletions. A deterministic version blocked 97.6% but also confirmed 97.6–100% of legitimate positive requests; the paired gold calls show why this call-only rule cannot tell those intentions apart.”
6. **next_experiments_needed:** none for closing this tested rule.
7. **confidence:** high.

### K6 — Scoring and anecdote

1. **claim_supported:** partial.
2. **what_results_support:** The cited strict clean wrong-action rates match. Of those strict `WRONG_ACTION` cases, lenient rescoring changed 9/12 (3B) and 6/7 (7B) to correct; the four 7B negation confirmations are a small case observation.
3. **what_results_dont_support:** Either scorer as a validated measure of semantic harm from entity substitutions. Strict scoring can overcount formatting differences; lenient scoring deliberately ignores free-text arguments.
4. **missing_evidence:** A small blinded semantic adjudication of free-text arguments, especially `content_sub`.
5. **suggested_claim_revision:** “We report the preregistered strict scorer alongside a post-hoc lenient scorer: strict scoring misclassified many clean calls because of free-text representations, while lenient scoring cannot measure entity-substitution harm reliably.”
6. **next_experiments_needed:** Blinded review of the `content_sub` calls if entity harm remains in the report’s main claim.
7. **confidence:** high.

### Overall narrative

1. **claim_supported:** partial.
2. **what_results_support:** Within 42 constructed cards and two Qwen models, matched-WER negation deletion sharply increased wrong proposed calls, while the tested confirmation prompts seldom asked about one-word errors. The tested optional-boolean rule failed its preregistered trade-off.
3. **what_results_dont_support:** A general result about “fluent semantic errors (negation, entity),” “cheap gates,” or actual speech-to-tool systems. Entity harm is unresolved between the two scorers; speaker tags and real ASR have not been established; the action-only indistinguishability applies to the paired calls and tested rule.
4. **missing_evidence:** Semantic adjudication for entity substitutions and real ASR, broader cards, and other model families for any general claim.
5. **suggested_claim_revision:** “In an exploratory text-injection pilot using 42 constructed commands and two Qwen models, matched-WER negation deletion caused many more wrong proposed tool calls than function-word deletion. Two tested confirmation prompts rarely clarified one-word errors, and an optional-boolean call filter traded high negation blocking for near-universal confirmation of legitimate positive mirrors.”
6. **next_experiments_needed:** Blinded `content_sub` adjudication if the report mentions entity harm; otherwise none for a narrowly framed negative-result note.
7. **confidence:** medium.

**Recomputed-number discrepancies:** The individual cited rates and intervals matched. One aggregate statement did not: K2 says action-level DiDs were “all ≤ 0,” but the lenient DiD for 3B `other_1w` is **+2.4 points [0.0, 7.1]** under both `confirm` and `confirm_generic`. This does not revive the preregistered interaction.

**VERDICT: partial**