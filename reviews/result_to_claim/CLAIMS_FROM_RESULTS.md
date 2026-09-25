verdict: partial
reviewer: gpt-6-sol (reasoning effort high, the lab's standard tier) · codex session 01a0d470-560c-7310-b263-495d37b01c56 · 2026-09-24
integrity_status: unavailable (no /experiment-audit was run) → this verdict is labelled provisional
evidence pre-check: 24/24 cited values verified (existence; `.aris/evidence_precheck.json`)
reviewer re-ran analyze.py and both scorers on all 5,964 saved outputs: every stored label matched; per-card WER equal across one-word conditions on all 42 cards.

# Verdict per claim and the wording adopted

| # | Original claim | Verdict | Wording adopted (reviewer's, verbatim) | Confidence |
|---|---|---|---|---|
| K1 | Same WER, different harm | **yes** (within these cards) | On 42 constructed commands at identical per-card word error rate, deleting the negation produced far more wrong proposed calls than deleting a function word in both tested Qwen models | high |
| K2 | Confirmation gate is blind to fluent one-word errors | partial | In these two Qwen models, the tested confirmation prompts rarely requested clarification for the constructed one-word errors, including negation deletion, and the pre-registered bystander-versus-negation confirmation gap was absent | high for the measurement / medium for the interpretation |
| K3 | The gate reacts only to multi-word incoherence | partial | The tested confirmation prompt asked more often on the longer bystander fragments than on the one-word edits; those fragments also had substantially higher WER (length, WER, position and content vary together, so "incoherence" cannot be isolated) | high / medium |
| K4 | Oracle speaker labels | partial | Oracle speaker tags did not meet the pre-registered 30-point wrong-action reduction on multi-word bystander intent: 2.4 points (3B) and 11.9 points (7B) (**do not say 3B "ignores" the labels**: its outputs changed, NO_CALL 6/42 → 4/42) | high |
| K5 | An action-shape rule cannot separate "wanted true" from "lost negation" | partial | On these paired cards, the prompted optional-boolean rule almost never blocked negation deletions; a deterministic version blocked 97.6% but also confirmed 97.6–100% of legitimate positive requests; the transcript-faithful call on a negation-dropped card is identical to the gold call of its positive mirror, which is why this call-only rule cannot tell the two intentions apart [corrected 2026-09-24: the reviewer's wording said "paired gold calls"; the gold calls of the pair are opposite, it is the proposed call that coincides]. **51.2% is a figure from an artificial 1:1 mix, not a deployment cost** | high |
| K6 | Scorers | partial | Report the pre-registered strict scorer alongside the post-hoc lenient scorer: strict scoring misclassified many clean calls because of free-text representations, while lenient scoring cannot measure entity-substitution harm reliably | high |
| Overall | "Same WER, blind gates, no fingerprint of negation" | **partial** | In an exploratory text-injection pilot using 42 constructed commands and two Qwen models, matched-WER negation deletion caused many more wrong proposed tool calls than function-word deletion. Two tested confirmation prompts rarely clarified one-word errors, and an optional-boolean call filter traded high negation blocking for near-universal confirmation of legitimate positive mirrors | medium |

# Not supported by the data; not written in the note
- Any general conclusion about "fluent semantic errors (including entities)" — entity-substitution harm is unresolved between the two scorers (strict 93–95%, lenient 9.5–19%).
- Any general "cheap gates are blind"; "3B ignores the labels"; "51.2% is the cost"; real ASR / executed consequences.

# One error found by the reviewer's recomputation (fixed)
The statement "all action-level DiDs ≤ 0" in IDEA_REPORT / RESULTS_P0b was wrong: 3B other_1w is +2.4pp [0.0, 7.1] under both confirm and confirm_generic. This does not affect the pre-registered conclusion (far below 25pp).

# Routing
partial → claims narrowed per the table; supplementary experiments: blind adjudication of content_sub only if the note mentions entity harm (it does not); no new experiments needed for a negative-result note.
