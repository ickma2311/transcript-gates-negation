### Point P_1: Constructed labels and rates
**Attack claim**: Every seed card changes one optional Boolean from false to true when its negator is removed, and every positive mirror requires true; the headline rates are therefore engineered.

**Verdict**: partially_answered  
**Evidence (or lack of)**: The construction is explicit in [seed_items.py:39](pilot/seed_items.py:39) and [inject.py:85](pilot/inject.py:85). The note says the gold calls are construction determined and calls the large negation-versus-function-word contrast inevitable ([SHORT_REPORT.md:20](report/SHORT_REPORT.md:20), [54](report/SHORT_REPORT.md:54)). That disclosure makes the design defensible for a counterexample, but gives the rates no prevalence meaning.  
**Severity if unresolved**: major  
**If unresolved, recommended fix**: Label every 42-card percentage as conditional on this constructed set wherever it appears in a headline or conclusion.

### Point P_2: Seven exact collisions
**Attack claim**: A transcript-only gate cannot distinguish the seven identical-input pairs by definition, so identical responses are not an empirical discovery about gate competence.

**Verdict**: answered_by_current_text  
**Evidence (or lack of)**: The note identifies exactly seven identical pairs, limits its explicit impossibility proof to them, and says this is missing input information rather than model failure ([SHORT_REPORT.md:29](report/SHORT_REPORT.md:29)–38). I reproduced the seven pairs from the code and checked that their saved P0c outputs match in both models under `none` and `confirm_optbool`. A constructed collision is a valid impossibility counterexample.  
**Severity if unresolved**: critical  
**If unresolved, recommended fix**: None for the exact-pair claim.

### Point P_3: The other 35 pairs remain distinguishable
**Attack claim**: The proof for seven identical pairs cannot establish impossibility for the other 35; even a `but`/`and` change is information a text gate can use.

**Verdict**: partially_answered  
**Evidence (or lack of)**: The table distinguishes seven exact pairs from 18 pairs that are identical *or* differ by one `but`/`and` ([SHORT_REPORT.md:31](report/SHORT_REPORT.md:31)–38). Reconstruction gives seven exact, 11 one-word-different, and 24 more-different pairs. Yet the one-sentence claim and conclusion say text gates lack usable evidence “on these inputs” ([SHORT_REPORT.md:9](report/SHORT_REPORT.md:9)–15, [85](report/SHORT_REPORT.md:85)); line 53 also calls the 18 “the same text.”  
**Severity if unresolved**: major  
**If unresolved, recommended fix**: Confine “impossible” and “no evidence” to the seven exact pairs, and describe the remaining 35 solely as measured cases with observable textual differences.

### Point P_4: “Wrong action” is not gate failure
**Attack claim**: The 41/42 wrong-action score compares responses to a hidden negated source, although the models usually follow the affirmative transcript they receive.

**Verdict**: answered_by_current_text  
**Evidence (or lack of)**: The note defines WA against **hidden original intent** ([SHORT_REPORT.md:24](report/SHORT_REPORT.md:24)–25), explains the 41/42 as predominantly faithful execution of visible text ([52](report/SHORT_REPORT.md:52)–54), and expressly says low `neg_drop` confirmation is not evidence of detection failure ([68](report/SHORT_REPORT.md:68)). One correction remains: line 86 says positive mirrors were correct 40–42/42, while the reported 3B `none` result is 39/42 ([RESULTS_P0d.md:7](pilot/RESULTS_P0d.md:7)).  
**Severity if unresolved**: major  
**If unresolved, recommended fix**: None for the interpretation; correct the 39/42 figure.

### Point P_5: Wrapper “tradeoff” follows from its rule
**Attack claim**: A wrapper that confirms any proposed true optional Boolean will confirm nearly every positive mirror, because true is what those mirrors were designed to request.

**Verdict**: partially_answered  
**Evidence (or lack of)**: The wrapper implements exactly that rule ([analyze.py:73](pilot/analyze.py:73)–88). The preregistration predicts a construction-driven near-100% positive-mirror cost ([PREREG_P0c.md:7](pilot/PREREG_P0c.md:7)–24), and the note confines the figures to this rule and rejects the artificial 1:1 mixture as a deployment cost ([SHORT_REPORT.md:80](report/SHORT_REPORT.md:80)–81). The opening “must block 97.6–100%” wording still sounds broader than the tested rule and sample ([11](report/SHORT_REPORT.md:11)).  
**Severity if unresolved**: major  
**If unresolved, recommended fix**: Replace the opening “must” claim with “this optional-Boolean wrapper confirmed 97.6–100% of positive mirrors in the constructed set.”

### Point P_6: No measured real-ASR incidence
**Attack claim**: Text deletion supplies no estimate of how often real ASR produces these collisions, leaving operational frequency and cost unmeasured.

**Verdict**: partially_answered  
**Evidence (or lack of)**: The note plainly identifies text-level injection, excludes real-ASR conclusions, and disclaims deployment cost ([SHORT_REPORT.md:3](report/SHORT_REPORT.md:3), [16](report/SHORT_REPORT.md:16), [81](report/SHORT_REPORT.md:81), [93](report/SHORT_REPORT.md:93)). Disclosure addresses the overclaim, but cannot supply an incidence estimate. That gap limits practical significance; it does not invalidate an explicitly conditional counterexample.  
**Severity if unresolved**: major  
**If unresolved, recommended fix**: State in the opening conclusion that the work establishes possibility, with real-ASR collision frequency and deployment cost unknown.

## Summary

Total rejection points: **6** — answered_by_current_text: **2** — partially_answered: **4** — still_unresolved: **0**

## Net assessment

**Major revision, rather than rejection on this memo alone, for a self-scoped exploratory note.** “Built into the stimuli” restates the mechanism of a valid impossibility demonstration for the seven exact collisions; it does not refute that demonstration. The note still reaches beyond those seven when it says text gates have no usable evidence across “these inputs,” and its opening wrapper claim is broader than its constructed-rule measurement supports. The 41/42 result is an observation about two models’ proposed calls relative to hidden intent, not an empirical gate failure. No real-ASR collision frequency is a stated limitation, not by itself a reason to suppress a conditional counterexample. What remains publishable is a narrow illustrative note; the files do not support a general empirical negative result or an operational tradeoff estimate.

## Top action items

1. Restrict every impossibility claim to the seven exact pairs; keep the other 35 as behavioral observations.
2. Qualify the wrapper figures as results for this rule on this constructed set, including in the opening summary.
3. Correct the positive-mirror count in [SHORT_REPORT.md:86](report/SHORT_REPORT.md:86) from 40–42/42 to 39–42/42.