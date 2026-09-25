"""Audit: print raw outputs scored WRONG_ACTION on CLEAN transcripts (scorer strictness check) and a sample per condition."""
import json, sys, collections
d = sys.argv[1]
rows = [json.loads(l) for l in open(f"{d}/results.jsonl")]
trials = {(r["item_id"], r["condition"]): r for r in map(json.loads, open(f"{d}/trials.jsonl"))} if len(sys.argv) < 3 else {}
bad = [r for r in rows if r["condition"] == "clean" and r["gate"] == "none" and r["outcome"] in ("WRONG_ACTION", "EXTRA_ARG")]
print(f"clean/none WRONG_ACTION+EXTRA_ARG: {len(bad)}")
for r in bad:
    t = trials.get((r["item_id"], "clean"), {})
    print(f"- {r['item_id']} [{r['outcome']}] gold={json.dumps(t.get('gold'))}\n    raw={r['raw'][:220]!r}")
print("\nSample CONFIRM replies:")
for r in [r for r in rows if r["outcome"] == "CONFIRM"][:6]: print(f"- {r['condition']}/{r['gate']}: {r['raw'][:160]!r}")
print("\nother_1w EXTRA_CALL / WRONG examples:")
for r in [r for r in rows if r["condition"] == "other_1w" and r["gate"] == "none" and r["outcome"] in ("EXTRA_CALL", "WRONG_ACTION")][:5]:
    print(f"- {r['item_id']}: {r['raw'][:200]!r}")
