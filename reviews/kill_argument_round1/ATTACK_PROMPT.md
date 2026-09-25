You are simulating a hostile senior reviewer (Interspeech / ACL Findings / a careful area chair) for a short empirical negative-result note. This is a kill-argument adversarial check: your task is NOT a balanced review but the **single strongest argument for rejecting or not publishing this note**.

## Files to read (fresh, zero-context pass; do not look for prior reviews)
- The note: `report/SHORT_REPORT.md` (Chinese; answer in English)
- Raw data and code it relies on: `pilot/` — `seed_items.py` (cards), `inject.py`, `run_pilot.py` (strict scorer), `rescore.py` (lenient scorer), `analyze.py` (`python analyze.py colab_out` etc. reproduces the tables; for lenient numbers copy each `results_lenient.jsonl` next to its `trials.jsonl` as `results.jsonl`), `PREREG_P0.md` / `PREREG_P0b.md` / `PREREG_P0c.md`, `RESULTS_P0*.md`, raw outputs in `colab_out/`, `colab_out_p0b/`, `colab_out_p0c/`.
You may run the CPU-only Python there. Verify numbers yourself where you accuse.

## Your task
Write the worst-case rejection memo in approximately 200 words (do NOT exceed 250). One coherent argument, not a list. Pick the most damaging line of attack among: claim-vs-evidence gap; construction artefacts that make the headline trivially true or uninformative; scorer / statistics problems that change interpretation; scope overclaim in the title or one-sentence summary; whether the note contributes anything a reader could act on; contamination of "negative result" by design flaws (i.e., the gates failed because the test was unfair, not because gates fail). Cite file:line or table cells when accusing. Dispassionate, uncompromising, no hedging, do not acknowledge mitigations. Output just the memo.
