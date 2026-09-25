# PREREG P0d — cost of the confirmation prompts on the positive-mirror cards (the gap raised as P5 in kill-argument round 1; 2026-09-24, fixed before the run)

Question: Table 2's "0% false confirmations on clean" was measured only on the 42 negated cards; the confirmation and wrong-action rates of `confirm` / `confirm_generic` / `spktag` on the 42 **positive** cards (where the user genuinely wants that true) are unknown.
Materials: the same 42 `clean_pos` cards (frozen in P0c); gates none / confirm / confirm_generic / spktag; both models; one Colab T4 session.
Endpoints: CF(clean_pos) and WA(clean_pos) per gate; reported next to P0's CF(clean).
Decision: no hypothesis test; this is a cost measurement. Reporting rule: Table 2's clean-cost row must give both numbers, negated cards and positive cards.
Code unchanged (run_pilot.py hash as in PREREG_P0c); the job only filters the trials to clean_pos.
