"""DEVIATION (post hoc, exploratory): lenient re-scoring of saved raw outputs.
Strict scorer (frozen) required every gold argument to match, including free-text strings ('4 o'clock' vs 'four o'clock').
Lenient: function name + every boolean / integer / enum argument must match gold (extra true booleans still count as wrong);
free-text string arguments are NOT scored. Everything else (CONFIRM, EXTRA_CALL, parse) unchanged. Writes results_lenient.jsonl."""
import json, sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_pilot as rp

def lenient_matches(call, gold, tools):
    (gname, gargs), = gold.items()
    if call.get("name") != gname: return False
    args = call.get("arguments", {}) or {}
    schema = {}
    for t in tools:
        if t["function"]["name"] == gname: schema = t["function"]["parameters"]["properties"]
    for k, v in args.items():
        if k not in schema: return False
        en = schema[k].get("enum")
        if en and isinstance(v, str) and v.lower() not in [e.lower() for e in en]: return False
    for k, v in gargs.items():
        if isinstance(v, bool):
            if bool(args.get(k, False)) != v: return False
        elif isinstance(v, int):
            if rp.norm(args.get(k)) != v: return False
        elif schema.get(k, {}).get("enum"):
            if str(args.get(k, "")).lower() != str(v).lower(): return False
    for k, v in args.items():
        if isinstance(v, bool) and v and not gargs.get(k, False): return False
    return True

def score_lenient(row, text):
    calls = rp.parse_calls(text)
    if (re.search(r"^\s*CONFIRM\s*:", text, re.M | re.I) or re.search(r"\bCONFIRM:", text)) and not calls: return "CONFIRM"
    if not calls: return "NO_CALL" if text.strip() else "PARSE_FAIL"
    ok = [lenient_matches(c, row["gold"], row["tools"]) for c in calls]
    if any(ok) and len(calls) > 1: return "EXTRA_CALL"
    if ok[0]: return "CORRECT"
    if row["condition"] == "neg_drop" and any(lenient_matches(c, row["flipped"], row["tools"]) for c in calls): return "FLIPPED"
    return "WRONG_ACTION"

if __name__ == "__main__":
    d = sys.argv[1]
    trials = {(r["item_id"], r["condition"]): r for r in map(json.loads, open(f"{d}/trials.jsonl"))}
    rows = [json.loads(l) for l in open(f"{d}/results.jsonl")]
    out = []
    for r in rows:
        t = trials[(r["item_id"], r["condition"])]
        r2 = dict(r); r2["outcome_strict"] = r["outcome"]; r2["outcome"] = score_lenient(t, r["raw"]); out.append(r2)
    with open(f"{d}/results_lenient.jsonl", "w") as f:
        for r in out: f.write(json.dumps(r) + "\n")
    ch = collections.Counter((r["outcome_strict"], r["outcome"]) for r in out if r["outcome_strict"] != r["outcome"])
    print(f"{d}: re-scored {len(out)}; changed {sum(ch.values())}: {dict(ch)}")
