# Research review brief (idea-discovery Phase 4) — idea "asr_toolcall"

You are a senior ML/speech reviewer (NeurIPS / Interspeech level). Start from the assumption that this plan is broken somewhere and find where. Executor notes are not evidence beyond the files they cite; verify the artifacts yourself. You may read anything under `` and run the CPU-only code there (`python inject.py 0`, `python run_pilot.py --backend mock ...`, `python acoustic_p1.py --selftest`, `python analyze.py <dir>`). Do NOT propose adding modules, gates, frameworks or flags; an objection is recorded as a named risk or answered by a cheaper discriminating experiment. The core hypothesis is not up for rewriting. If, after genuinely trying to break it, the plan holds, say so plainly.

## Files
- `idea-stage/IDEA_REPORT.md` — literature landscape (51 verified arXiv IDs), ranked ideas (from gpt-6-sol brainstorm), novelty verdict (gpt-6-sol: P0 7/10 PROCEED WITH CAUTION, P1 6/10 PROCEED WITH CAUTION).
- `idea-stage/novelty_gpt6sol.md` — the full novelty report, including four harness defects it found (all fixed since; see PREREG).
- `pilot/PREREG_P0.md` — frozen pre-registration for pilot P0 (hypotheses H1–H3, GO/STOP rules, hashes).
- `pilot/seed_items.py`, `pilot/inject.py`, `pilot/run_pilot.py`, `pilot/analyze.py` — the frozen harness. `pilot/trials.jsonl` = 42 cards × 7 conditions.
- `pilot/acoustic_p1.py` — the P1 (acoustic transfer) pipeline: Kokoro TTS → word-span masking / bystander mixing → Whisper-large-v3 → alignment-based selection.
- `pilot/job_bundle.py` — the self-contained Colab job. **No GPU run has happened yet**; all numbers so far are from mock/CPU smoke tests.

## The idea in one paragraph
At identical per-utterance WER (exactly one word-level edit), compare how four transcript error types — negation drop, function-word drop, content-word near-homophone substitution, single-word insertion from a bystander speaker — change an LLM agent's proposed tool call (endpoint: wrong/extra action vs correct vs confirmation request), and whether two cheap prompt-level gates (confirm-when-uncertain; oracle speaker tags) catch different error types. Pre-registered lead result: the gate × error-type interaction (H1: confirmation catches conspicuous one-word bystander insertions ≥25pp more often than fluent negation drops, with ≤25% false confirmations on clean; H3: speaker tags cut bystander wrong actions ≥30pp but leave negation drops unchanged). P1 then asks whether the text-injection ranking of error types survives real ASR (TTS + masking/mixing + Whisper, selection by transcript alignment only, rejection rates reported).

## Known weaknesses (be harder than these)
- Negation drop flips the gold by construction; its wrong-action rate is a magnitude, not a discovery.
- 42 hand-built cards (executor-written, not blind-checked); Qwen2.5-3B / 7B-AWQ only; prompt-level gates only; oracle speaker labels.
- Endpoint is the proposed call (mock execution), not real harm.
- Concurrent work: MTVA-Bench 2609.20152 (09-17), MSI-Bench 2609.24812 (09-21), Audio2Tool 2604.22821, and **MFCL-Audio (ICML 2026, Salesforce; 6.2K tasks; Text-Audio pipelined vs True-Audio suites; perturbations: accent, speaking rate, disfluency, background noise; a clarification protocol)** — found by the novelty reviewer; we have not confirmed whether MFCL-Audio compares error types at matched WER or scores confirmation cost per error type. Please check it.

## Questions (answer each, with file:line or a runnable counter-example where you can)
1. Is there a flaw in the matched-WER logic — does "one edit each" really make the four types comparable, or is there a confound (position of the edit, argument-bearing vs not, sentence-final insertion being trivially detectable) that would make H1 true for an uninteresting reason? If the sentence-final insertion is the problem, name the cheapest fix that does not add machinery.
2. Is the confirm gate as prompted a fair "cheap gate", or is it strawman-easy to fail / to game? What single control would convince you?
3. Are the GO/STOP thresholds in PREREG_P0.md sensible for n = 42 cards, or under-/over-powered? Give the number of cards you would want and why.
4. What is the strongest case FOR this idea — what result would make it the paper people cite?
5. What is the cheapest discriminating next experiment after P0 (one sentence, with a decision rule)?
6. Verdict line: `VERDICT: PROCEED` or `VERDICT: ABANDON` (with the named reason), plus a score /10 for "worth one more week of a single researcher's time on free compute".

Say plainly when something is correct. Do not manufacture findings.
