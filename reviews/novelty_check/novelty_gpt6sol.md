## Novelty Check Report

### Proposed Method

**P0** compares controlled transcript edits on the same tool-call cards, holding word error rate (WER) equal for the single-word conditions, then tests confirmation and speaker-label prompts. **P1** tests whether the resulting error-type ranking carries over to qualifying Whisper transcripts from perturbed audio. Both score *proposed tool calls*; neither measures executed harm.

### Core Claims

1. **P0, same WER can yield different wrong-call rates** — Closest: [Beyond WER (2606.05909)](https://arxiv.org/abs/2606.05909) — What stays unknown or different: its paired acoustic study measures clinical outputs, not a matched-WER comparison of input error types on tool calls.

2. **P0, confirmation catches conspicuous insertions more often than fluent negation loss** — Closest: [Proactive for Uncertainty (2605.25404)](https://arxiv.org/abs/2605.25404) and **MFCL/BFCL Audio [UNVERIFIED]** — What stays unknown or different: the former uses ASR-internal error detectors; the latter accommodates clarifications in audio function calling, but I found no per-ASR-error-type comparison of confirmation benefit *and* false-confirmation cost. The ICML 2026 audio paper has [an official conference listing](https://icml.cc/Downloads/2026); its arXiv ID is **[UNVERIFIED]**.

3. **P0, speaker labels help source errors but not negation loss** — Closest: [MSI-Bench (2609.24812)](https://arxiv.org/abs/2609.24812) — What stays unknown or different: MSI-Bench *does* compare audio with speaker-labeled transcripts on speaker-authority cases; it does not test the proposed source-error versus negation-error gate interaction. The dossier understates this overlap.

4. **P1, the text-injection risk ranking transfers to ASR** — Closest: [From Text to Voice (2605.15104)](https://arxiv.org/abs/2605.15104) and **MFCL/BFCL Audio [UNVERIFIED]** — What stays unknown or different: both pair text and audio tool-call evaluations; I found no test of whether a *matched error-type ranking* from injected transcripts predicts the ranking from selected ASR outputs.

5. **P1, targeted acoustic errors can be produced at useful yield** — Closest: [Audio2Tool (2604.22821)](https://arxiv.org/abs/2604.22821) — What stays unknown or different: it tests acoustic noise and background-speaker intent, but does not report yield for aligned negation, function-word, and content-word errors.

**Direct-result check:** For **P0 and P1 separately**, I found no specific published paper reporting either exact result posed in question 1: matched-WER input-error types on an LLM tool-call endpoint, or confirmation/speaker gates evaluated per ASR error type with both benefit and false-confirmation cost. This is a search finding, not proof that no such work exists.

### Closest Prior Work

| Paper | Year | Venue | Overlap | Key Difference |
|---|---:|---|---|---|
| [MTVA-Bench (2609.20152)](https://arxiv.org/abs/2609.20152) | 2026 | arXiv preprint | Injects authored channel damage before tool calls | No matched-WER type × gate study. **Correction:** its 53 channel conditions comprise only **10 light ASR cases** and 43 VAD splits. |
| **MFCL/BFCL Audio [UNVERIFIED]** ([ICML listing](https://icml.cc/Downloads/2026); [accessible earlier MFCL draft](https://openreview.net/pdf?id=8yWECy22Zi)) | 2026 | ICML listing; earlier draft | Audio function calls, perturbations, clarification handling | Closest newly found benchmark; no exact proposed interaction established from the material I could access. The accepted full text was unavailable to verify here. |
| [MSI-Bench (2609.24812)](https://arxiv.org/abs/2609.24812) | 2026 | arXiv preprint | Speaker-scoped tool decisions; audio versus labeled-transcript comparison | No matched-WER error types or negation comparison. |
| [Audio2Tool (2604.22821)](https://arxiv.org/abs/2604.22821) | 2026 | arXiv preprint | Background speaker with a valid competing intent | No matched transcript-error comparison or gate test. |
| [From Text to Voice (2605.15104)](https://arxiv.org/abs/2605.15104) | 2026 | arXiv preprint | Paired text/audio calls and **output** error taxonomy | Does not rank controlled **input** ASR-error types. |
| [Beyond WER (2606.05909)](https://arxiv.org/abs/2606.05909) | 2026 | INTERSPEECH 2026 | Paired noise, negation errors, downstream safety | Clinical documentation endpoint; no matched-WER type contrast. |
| [Vehicle Voice Command Authorization (2609.19630)](https://arxiv.org/abs/2609.19630) | 2026 | arXiv preprint | Speaker metadata, confirmation class, false executes | Explicitly assumes accurate transcription. |

### Overall Novelty Assessment

- Score (P0): **7/10**   - Score (P1): **6/10**
- Recommendation (P0): **PROCEED WITH CAUTION**
- Recommendation (P1): **PROCEED WITH CAUTION**
- Key differentiator: **P0’s defensible claim is the error-type × gate interaction on wrong proposed calls at matched WER. P1’s is whether that ranking transfers through ASR, with selection yield reported. Both clear this novelty check.**
- Risk: **P1 is more exposed to concurrent work.** Audio2Tool and the ICML audio benchmark already study acoustic tool-call failures; MTVA-Bench can expand its channel cases, and MSI-Bench already tests a speaker-labeled transcript condition. The remaining P1 delta is narrow enough for those groups to add. This is a race, not a reason to abandon it.

### Suggested Positioning

Make the **gate × type interaction** P0’s lead result. Negation removal flips the intended argument **by construction**; a higher wrong-call rate than a harmless function-word deletion is informative about model behavior and magnitude, but weak as a standalone discovery. A transcript-only confirmation prompt also has no direct evidence that a fluent negation was deleted. Its practical detection limit is the useful question.

Fix the harness before using its thresholds. In the frozen `inject.py` run, **3 of 42 content substitutions have twice the claimed one-edit WER** because a replacement contains two words. The confirmation hypothesis compares a one-word negation drop with a **3–6-word** bystander intent, confounding type with dose. The speaker-tag run excludes negation drops, so it cannot establish “does nothing for negation.” Perfect supplied speaker labels measure an oracle-label setting. In `run_pilot.py`, a response containing both `CONFIRM:` and a tool call is scored as confirmation before its call is parsed. Audit these cases and the semantic validity of the hand-built flipped calls before preregistration.

For P1, report the **unselected ASR outputs and rejection rates** alongside the qualifying subset. Selecting on transcript alignment before seeing agent outputs avoids outcome leakage, but transfer on selected examples does not establish transfer for ordinary ASR traffic. Its small error-type ranking also needs uncertainty reported, not only a Spearman threshold.

### Papers you checked that turned out NOT to overlap (so we do not re-check them)

- [Small Edits, Big Consequences (2507.15868)](https://arxiv.org/abs/2507.15868): meaning-changing text edits in coding prompts; no speech-to-tool endpoint.
- [Blue Teaming Function-Calling Agents (2601.09292)](https://arxiv.org/abs/2601.09292): adversarial attacks and defenses for function-calling agents; no ASR error-type experiment.
- [Noise-LLM noisy slot filling (2310.06504)](https://arxiv.org/abs/2310.06504): input perturbations for slot filling; no executable tool-call or gate endpoint.
- [Measuring Transcription Noise (2502.13645)](https://arxiv.org/abs/2502.13645): downstream language-understanding tasks, rather than tool actions.

