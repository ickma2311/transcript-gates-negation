# Kill Argument Report — round 1 — asr_toolcall SHORT_REPORT.md

**Date**: 2026-09-24 · **Reviewer model**: gpt-6-sol, reasoning effort xhigh (the lab's strong tier for adversarial review), two fresh codex threads
**Attack thread**: codex-session:01a0d51f-04b5-7563-b3b8-29133608d11f · **Adjudicator thread**: codex-session:01a0d521-a266-7ad0-9934-107125b5ff0f
**Verdict**: **FAIL** (`reason_code: unresolved_critical`) — counts: {'answered_by_current_text': 0, 'partially_answered': 4, 'still_unresolved': 2}

## Net assessment
**The current note would not survive a senior read of this attack.** Its caveats acknowledge constructed data and a construction-determined contrast, but do not carry through to the gate claim. An honest, potentially publishable exploratory framing remains: **verbatim-identical transcript-and-schema pairs can have opposite original-intent gold answers, so a transcript-only gate cannot recover a deleted negation from those inputs; the models’ measured outputs then show how they act on the visible text.** Table 1 can report that behavior, and P0c can report the specific optional-boolean filter’s cost. Neither establishes general failure to detect an observable warning or a useful detector tradeoff.

## Attack memo (verbatim)
> I would reject this note because its central gate test asks the model to detect an error for which the test often supplies no evidence. The confirmation prompts receive only one transcript and the tool schemas, with no audio, ASR alternatives, or confidence information (`pilot/run_pilot.py:10-17,31-38`). Negation is deleted while the original negative call remains the gold answer (`pilot/inject.py:37-38,81-84`).
> 
> P0c makes the problem concrete: seven `neg_drop` transcripts are verbatim identical to legitimate `clean_pos` transcripts with the same tools but opposite gold calls. For `me3`, both inputs say “add a video link”; the gold `video_call` value is false in one trial and true in the other (`pilot/colab_out_p0c/Qwen2.5-3B-Instruct/trials.jsonl:90,348`). A text-only gate cannot distinguish those trials. The raw outputs are identical for all seven pairs under both P0c gates and both models.
> 
> The reported 41/42 wrong actions per model after negation deletion (`report/SHORT_REPORT.md`, Table 1) therefore measure agreement with the visible transcript, not failure to detect an observable warning sign. Table 2’s zero false-confirmation rate uses only the original negative cards as clean controls (`report/SHORT_REPORT.md:19,49`). This design cannot establish a useful detection-versus-confirmation tradeoff.

## Adjudication (verbatim)
### Point P_1: The gate lacks evidence of deletion
**Attack claim**: The confirmation gates see one transcript and tool schemas, so they cannot inspect audio, ASR alternatives, or confidence for evidence that a negation was lost.  
**Verdict**: partially_answered  
**Evidence (or lack of)**: [run_pilot.py:10](pilot/run_pilot.py:10) and [run_pilot.py:31](pilot/run_pilot.py:31) confirm the input limit. The note calls this “text-layer injection” and disclaims real-ASR conclusions at [SHORT_REPORT.md:3](report/SHORT_REPORT.md:3), but never states its consequence: a deleted negation may leave no detectable cue. That qualification does not sustain a claim about failure to detect an observable error.  
**Severity if unresolved**: critical  
**If unresolved, recommended fix**: State explicitly that these gates are being tested on transcript-only inputs that can contain no evidence of the deletion.

### Point P_2: The gold answer preserves hidden speech
**Attack claim**: `neg_drop` deletes the negative word while scoring against the original negative intent, making a transcript-faithful positive call wrong by construction.  
**Verdict**: partially_answered  
**Evidence (or lack of)**: [inject.py:37](pilot/inject.py:37) deletes the word; [inject.py:81](pilot/inject.py:81) retains the original gold call. The note acknowledges at [SHORT_REPORT.md:42](report/SHORT_REPORT.md:42) that the large contrast is construction-determined. Yet its headline and finding at [SHORT_REPORT.md:9](report/SHORT_REPORT.md:9) still present it as a measured difference in harmful error susceptibility. That position is not sustainable without foregrounding the hidden-gold construction.  
**Severity if unresolved**: critical  
**If unresolved, recommended fix**: Recast Table 1 as the rate at which calls disagree with the unobserved original intent after a stipulated deletion.

### Point P_3: Identical inputs have opposite gold calls
**Attack claim**: Seven `neg_drop` and `clean_pos` pairs give a text-only gate the same transcript and schemas but opposite gold boolean values; no such gate can distinguish them.  
**Verdict**: still_unresolved  
**Evidence (or lack of)**: The `me3` rows at [trials.jsonl:90](pilot/colab_out_p0c/Qwen2.5-3B-Instruct/trials.jsonl:90) and [trials.jsonl:348](pilot/colab_out_p0c/Qwen2.5-3B-Instruct/trials.jsonl:348) have identical visible inputs and opposite `video_call` gold values. I verified seven exact input pairs and identical raw outputs under both P0c gates in both models; `me3` outputs appear at [3B results.jsonl:179](pilot/colab_out_p0c/Qwen2.5-3B-Instruct/results.jsonl:179) and [3B results.jsonl:695](pilot/colab_out_p0c/Qwen2.5-3B-Instruct/results.jsonl:695). The note mentions only *call-only* indistinguishability and says paired gold calls are identical at [SHORT_REPORT.md:88](report/SHORT_REPORT.md:88); that does not answer these opposite-gold transcript pairs.  
**Severity if unresolved**: critical  
**If unresolved, recommended fix**: Present the seven pairs as an explicit transcript-only impossibility result, with the two distinct gold calls and matched outputs.

### Point P_4: The 41/42 figure is misinterpretable
**Attack claim**: The 41/42 wrong-action count per model largely records agreement with the positive meaning of the visible transcript, not failure to heed an observable warning.  
**Verdict**: partially_answered  
**Evidence (or lack of)**: Table 1 reports 97.6% at [SHORT_REPORT.md:35](report/SHORT_REPORT.md:35), and [SHORT_REPORT.md:43](report/SHORT_REPORT.md:43) calls the contrast construction-determined. But [SHORT_REPORT.md:84](report/SHORT_REPORT.md:84) continues to describe the count as “wrong proposed calls” without saying that following the supplied transcript is often the only evidence-based action available. The admission is real, but incomplete.  
**Severity if unresolved**: critical  
**If unresolved, recommended fix**: Put “41/42 disagreed with hidden original intent while generally following the visible transcript” beside the Table 1 number.

### Point P_5: Table 2’s clean controls are too narrow
**Attack claim**: Table 2’s zero false-confirmation rate covers only the original clean negative cards, leaving legitimate positive requests untested for those confirmation prompts.  
**Verdict**: partially_answered  
**Evidence (or lack of)**: [SHORT_REPORT.md:49](report/SHORT_REPORT.md:49) reports 0% for `clean`. P0c does add `clean_pos` at [SHORT_REPORT.md:23](report/SHORT_REPORT.md:23), but its gates are `none` and `confirm_optbool`, as specified at [PREREG_P0c.md:27](pilot/PREREG_P0c.md:27). Those positive cards do not establish the false-confirmation cost of Table 2’s `confirm` or `confirm_generic` prompts.  
**Severity if unresolved**: major  
**If unresolved, recommended fix**: Label Table 2’s 0% as the clean-negative rate only, and remove any broader cost inference unless those prompts are run on positive controls.

### Point P_6: No detector tradeoff is established
**Attack claim**: Low confirmation on deleted-negation trials and zero confirmation on negative clean controls cannot establish a useful detection-versus-confirmation tradeoff when the error can be invisible.  
**Verdict**: still_unresolved  
**Evidence (or lack of)**: [SHORT_REPORT.md:75](report/SHORT_REPORT.md:75)–[78](report/SHORT_REPORT.md:78) do measure a narrower result: a deterministic optional-boolean filter blocks most `neg_drop` calls while confirming nearly all legitimate positive requests. That is a valid cost measurement for that filter, and the note limits its pooled rate at [SHORT_REPORT.md:80](report/SHORT_REPORT.md:80). It does not establish a detector tradeoff for the confirmation prompts or overcome identical-input pairs.  
**Severity if unresolved**: major  
**If unresolved, recommended fix**: Separate the optional-boolean filter’s measured cost from any claim about error detection, and say the transcript-only detector tradeoff remains unidentified.

## Summary

Total rejection points: **6** — answered_by_current_text: **0** — partially_answered: **4** — still_unresolved: **2**

## Net assessment

**The current note would not survive a senior read of this attack.** Its caveats acknowledge constructed data and a construction-determined contrast, but do not carry through to the gate claim. An honest, potentially publishable exploratory framing remains: **verbatim-identical transcript-and-schema pairs can have opposite original-intent gold answers, so a transcript-only gate cannot recover a deleted negation from those inputs; the models’ measured outputs then show how they act on the visible text.** Table 1 can report that behavior, and P0c can report the specific optional-boolean filter’s cost. Neither establishes general failure to detect an observable warning or a useful detector tradeoff.

## Top action items

1. Make the seven opposite-gold, identical-input pairs the central result; correct the statement at [SHORT_REPORT.md:88](report/SHORT_REPORT.md:88).
2. Rewrite the headline, Table 1 interpretation, and gate conclusion around hidden-original-intent disagreement versus visible-transcript behavior.
3. Restrict Table 2’s 0% cost claim to clean negative cards, or run its two prompts on the existing 42 positive mirrors before discussing their confirmation cost.

## Executor verification
The attack's factual basis was recomputed by the executor: 7 verbatim-identical neg_drop/clean_pos transcript pairs (me3, or3, cp2, df2, bf2, ri2, su2), 11 more differing only by "but"/"and"; raw outputs identical for all 7 pairs under both P0c gates in both models.

## Disposition
FAIL → the note is NOT published in this form. Reframe per the adjudicator (transcript-only impossibility + visible-text behaviour), run the two confirmation prompts on the 42 positive mirrors (P0d) to measure their cost, then a fresh round-2 kill-argument.
