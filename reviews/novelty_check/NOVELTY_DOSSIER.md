# Novelty dossier — two candidate ideas (novelty-check Phase C)

You are the cross-model novelty reviewer. Read this whole file, then (1) search the web/arXiv yourself for anything closer than what is listed, (2) judge under the VERDICT LIMITS at the end, (3) answer in the exact report format requested. You may also read `idea-stage/IDEA_REPORT.md` (section "Literature Landscape") and `pilot/` (the frozen pilot harness) for context. Cite papers only with arXiv IDs you have actually seen on arxiv.org during this session or that appear below; mark anything else `[UNVERIFIED]`. Never invent an ID.

## Idea P0 — "Same WER, different harm: an error-type × gate matrix for LLM tool calls"

**Method.** Take spoken-style commands that each contain exactly one negation whose removal flips exactly one boolean/enum argument of the gold tool call (42 hand-built cards over 23 tool schemas; gold and the "transcript-faithful wrong call" are both determined by construction). For every card create transcripts with **exactly one word-level edit** so that per-card WER = 1/L is identical across types: (a) negation drop, (b) function-word drop (control: "a word went missing"), (c) content/entity near-homophone substitution, (d) single-word insertion from a bystander speaker; plus two higher-dose conditions (3–6-word bystander fragment with a valid intent / with idle chatter). Run a frozen open-weight LLM agent (Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct-AWQ; vLLM, temperature 0) under three system prompts ("gates"): none; **confirm** ("if a recognition error could change the action, reply CONFIRM: <question> instead of calling"); **speaker-tag** (transcript annotated `[speaker 1]/[speaker 2]`, only speaker 1 is the enrolled user). Score every output as CORRECT / EXTRA_ARG / FLIPPED / WRONG_ACTION / EXTRA_CALL / CONFIRM / NO_CALL, so a gate cannot look good by refusing everything.

**Core claims (falsifiable).**
- C1 (same WER, different harm): at identical per-card WER, negation drop yields a much higher wrong-action rate than function-word drop (pre-registered ≥40pp).
- C2 (fluent-error blind spot): a prompt-level confirmation gate catches other-speaker insertions (transcript looks incoherent) far more often than negation drops (transcript is fluent) — pre-registered ≥25pp gap in CONFIRM rate — while false confirmations on clean transcripts stay ≤25%.
- C3 (source tags only fix source errors): speaker tags cut wrong actions under bystander insertion but do nothing for negation drops.
- The contribution is the **type × gate interaction at matched WER on the action endpoint**, not "speech hurts" (already known) nor "negation is severe" (already known in clinical/QA settings).

## Idea P1 — "Does the text-injection ranking survive real ASR?"

**Method.** TTS the same cards (target voice) and bystander fragments (different voice); create matched acoustic perturbations: mask the negation word span vs. a function-word span vs. a content-word span with equal-duration noise at equal SNR (word spans from Whisper word timestamps on clean audio), and mix the bystander fragment at fixed SNR after/overlapping the command. Transcribe with Whisper-large-v3. **Select items by transcript alignment alone** (intended edit occurred, WER within a pre-registered band) before any agent output is seen; report rejection counts. Then compare the wrong-action ranking of error types between text injection and qualifying ASR outputs (Spearman ≥0.8 = transfers).

**Core claims.** C4: text-level injection is a valid proxy for the action-level risk ordering of real ASR errors. C5 (feasibility): the yield of matched acoustic errors per type is high enough (≥30/80) to make such a benchmark practical.

## Candidate prior work already found (all IDs verified to exist via arXiv API on 2026-09-23)

Benchmarks on speech→tool calls: 2510.07978 (VoiceAgentBench), 2604.22821 (Audio2Tool; Tier 8 "intent blending" with a background speaker carrying a valid intent; Qwen3-Omni-30B 92.4%→41.7%; no error-type decomposition, no matched-WER, no mitigation), 2605.15104 (From Text to Voice; When2Call + Confetti to audio with DEMAND noise; output-error taxonomy: argument-value 39.5–57.2%, decision 25.8–37.4%), 2603.13686 (τ-Voice), 2604.04847 (Full-Duplex-Bench-v3), **2609.20152 (MTVA-Bench, 2026-09-17: text-level "channel layer" that drops/doubles/substitutes an authored span; only 53/490 scenarios carry channel damage; authors: "cannot support general claims", "the corpus needs many more scenarios with authored recognition damage")**, **2609.24812 (MSI-Bench, 2026-09-21: multi-speaker audio scenes with expected tool calls; "models often respond when no one has addressed them"; no matched control, no mitigation)**, 2609.13076 (MP-Bench; no tool calls), 2605.13841, 2607.27453, 2609.21967, 2608.26432.

WER is insufficient / error type matters: **2606.05909 (Beyond WER: paired acoustic stress test for clinical scribes; same dialogues under clean vs noise, downstream frozen; ambient noise +0.71pp WER yet unsafe outputs nearly doubled; MUSAN overlapping speech 5 dB: WER +38pp, unsafe +78pp; NegErr metric; endpoint = clinical document, not action; no matched-WER type contrast)**, 2507.16456 (AER, Interspeech'25; no error-type breakdown), 2608.30348 (ODR; echo → Whisper transcribes the far-end speaker in 62.1% of clips), 2502.13645 (task models "affected differently by the types of errors"; SLU classification tasks), 2601.15339, 2608.22872, 2605.17443, 2603.25727 (WildASR: ASR "hallucinate plausible but unspoken content ... concrete safety risks for downstream agent behavior"), 2106.02016.

Mitigations: 2309.04842 (n-best to LLM), 2512.17247, **2605.25404 (Proactive for Uncertainty: small detectors on ASR latents diagnose perception / comprehension / deletion errors, LLM asks targeted clarification; +17% downstream; no tool-call endpoint, no per-type benefit/cost of confirming)**, 2504.18851 (When2Call), 2605.18882, 2511.08798, 2606.06976, 2606.19559, 2510.05307 (confirmation frequency HCI), **2609.19630 (Vehicle Voice Command Authorization, 2026-09-17: speaker role/authentication passed as text metadata; REQUIRE_CONFIRMATION class; False Execute 1.2–13.7%; explicitly assumes an accurate transcription; lists transcription-error handling as future work)**, 2607.28165 (concurrent audio injection; CADV source-separation defence), 2608.05495 (PromptShield Home), 2604.14604, 2403.14438 / 2411.00023 / 2604.08412 / 2507.05609 / 2605.15044 (device-directed speech, side-talk rejection, speaker verification).

Possibly relevant, found only by web search and not yet read by us: 2507.15868 ("Small Edits, Big Consequences" — one-token edits / negation flips in text LLM robustness), 2601.09292 ("Blue Teaming Function-Calling Agents"), 2310.06504 (input perturbation framework for noisy slot filling).

## Questions to answer
1. For P0 and for P1 separately: is there a **specific published paper** that already reports (i) an error-type comparison at matched WER on an LLM *action/tool-call* endpoint, or (ii) confirmation / speaker-source gates evaluated **per ASR error type** with both benefit and false-confirmation cost? Name it or say none found.
2. What is the closest prior work for each idea and what exactly is the delta, in one sentence a reviewer could verify?
3. Which of the two is more at risk from concurrent work (MTVA-Bench, MSI-Bench, Audio2Tool authors) and why?
4. Anything in our harness design that would make the finding trivially true or trivially false (e.g., negation drop flips the gold by construction — is measuring its wrong-action rate informative at all, or is only the gate × type interaction informative)? Say so plainly.

## Report format (use exactly)
```
## Novelty Check Report
### Proposed Method
### Core Claims
1. [Claim] — Closest: [paper] — What stays unknown or different: [delta]
...
### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
### Overall Novelty Assessment
- Score (P0): X/10   - Score (P1): X/10
- Recommendation (P0): PROCEED / PROCEED WITH CAUTION / ABANDON
- Recommendation (P1): PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator:
- Risk:
### Suggested Positioning
### Papers you checked that turned out NOT to overlap (so we do not re-check them)
```

=== NOVELTY VERDICT LIMITS (these bound how you judge, never how widely you search) ===
Search exhaustively; judge calibrated. Two failures waste months equally:
passing an idea a published paper already contains, and killing a viable idea
because the territory has neighbors.
1. Proximity is information, not a verdict. Someone working nearby goes in the
   report; it is not by itself a reason to reject.
2. ABANDON has exactly one qualification: a specific published paper already
   contains this result — name that paper. No named paper, no ABANDON.
3. Crowded-but-deltaed is PROCEED: state the delta in one sentence a reviewer
   could verify. Thin or contested delta is PROCEED WITH CAUTION — say what
   would make it carry, not why it should die. CAUTION is not a safe middle:
   if you cannot name the specific thing that makes the delta thin, the
   verdict is PROCEED.
4. Concurrent or competing work is not a veto. That is a race — report it and
   let the user decide whether to run it.
5. A direct attack on a central problem is legitimate novelty when nobody has
   executed it well. "This area is hot" does not mean "this area is taken."
6. This check is an early gate, never the last one — more triage, pilots, or
   external review still stand between any idea and a paper, whatever order
   this run uses. A wrongly passed idea dies cheaply at one of them; a wrongly
   killed idea is never seen again. When torn between two verdicts, choose the
   more permissive one.
Say plainly when an idea clears the check. Do not manufacture overlap.
