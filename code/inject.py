"""Controlled transcript-error injection with explicit WER accounting.
Conditions (single-edit ones share exactly one edit per utterance -> identical per-item WER):
  clean        : no edit
  neg_drop     : delete the negation cue (1 deletion)
  func_drop    : delete one non-negation function word (1 deletion)   [control for 'a word went missing']
  content_sub  : substitute one content word by a near-homophone (1 substitution)
  other_1w     : insert ONE word from a bystander (imperative verb or entity) -> exact 1 insertion
  other_intent : insert a bystander fragment carrying a valid intent (k insertions, k = fragment length)
  other_chatter: insert a bystander fragment with no intent (k insertions)
Insert position: sentence end (most common leakage: bystander speaks right after the user) or start (prefix) -- both supported.
"""
import random, re, json
from seed_items import ITEMS, TOOLS, POS_UTTERANCES, BYSTANDER_INTENT, BYSTANDER_CHATTER, BYSTANDER_1W, CONTENT_SUB, FUNCTION_WORDS

def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    d = [[0]*(len(h)+1) for _ in range(len(r)+1)]
    for i in range(len(r)+1): d[i][0] = i
    for j in range(len(h)+1): d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1] + (r[i-1] != h[j-1]))
    return d[len(r)][len(h)] / max(1, len(r))

def _delete_once(utt, token):
    toks = utt.split()
    idx = [i for i, t in enumerate(toks) if t == token]
    assert idx, (utt, token)
    i = idx[0]
    return " ".join(toks[:i] + toks[i+1:]), i

def make_conditions(item, rng, insert_pos="end"):
    iid, tool_names, utt, neg, gold, flipped = item
    toks = utt.split()
    out = {}
    out["clean"] = {"transcript": utt, "edits": 0, "spk_spans": [(0, len(toks), 1)]}
    t, _ = _delete_once(utt, neg)
    out["neg_drop"] = {"transcript": t, "edits": 1, "spk_spans": [(0, len(toks)-1, 1)]}
    # function word: pick one present, not the negation, prefer not adjacent to negation to avoid double meaning change
    cands = [w for w in FUNCTION_WORDS if w in toks and w != neg]
    fw = rng.choice(cands)
    t, _ = _delete_once(utt, fw)
    out["func_drop"] = {"transcript": t, "edits": 1, "spk_spans": [(0, len(toks)-1, 1)], "dropped": fw}
    cands = [w for w in toks if w in CONTENT_SUB]
    cw = rng.choice(cands)
    assert len(CONTENT_SUB[cw].split()) == 1, ("content substitution must be one word", cw)
    i = toks.index(cw)
    t = " ".join(toks[:i] + [CONTENT_SUB[cw]] + toks[i+1:])
    out["content_sub"] = {"transcript": t, "edits": 1, "spk_spans": [(0, len(t.split()), 1)], "sub": (cw, CONTENT_SUB[cw])}
    # single-word other-speaker leak (exact 1 insertion -> WER 1/L like the other one-edit conditions)
    w = rng.choice(BYSTANDER_1W)
    if insert_pos == "end":
        t = utt + " " + w; spans = [(0, len(toks), 1), (len(toks), len(toks)+1, 2)]
    else:
        t = w + " " + utt; spans = [(0, 1, 2), (1, 1+len(toks), 1)]
    out["other_1w"] = {"transcript": t, "edits": 1, "spk_spans": spans, "fragment": w}
    # P0b: same single bystander word placed INSIDE the utterance at the clause boundary (before but/and/with/without), else at the midpoint
    bnd = [i for i, tk in enumerate(toks) if tk in ("but", "and", "with", "without")]
    pos = bnd[0] if bnd else len(toks) // 2
    t = " ".join(toks[:pos] + [w] + toks[pos:])
    out["other_1w_mid"] = {"transcript": t, "edits": 1, "spk_spans": [(0, pos, 1), (pos, pos+1, 2), (pos+1, len(toks)+1, 1)], "fragment": w, "pos": pos}
    for name, pool in (("other_intent", BYSTANDER_INTENT), ("other_chatter", BYSTANDER_CHATTER)):
        frag = rng.choice(pool)
        k = len(frag.split())
        if insert_pos == "end":
            t = utt + " " + frag; spans = [(0, len(toks), 1), (len(toks), len(toks)+k, 2)]
        else:
            t = frag + " " + utt; spans = [(0, k, 2), (k, k+len(toks), 1)]
        out[name] = {"transcript": t, "edits": k, "spk_spans": spans, "fragment": frag}
    for c in out.values():
        c["wer"] = round(wer(utt, c["transcript"]), 4)
    return out

def build(seed=0, insert_pos="end"):
    rng = random.Random(seed)
    rows = []
    for item in ITEMS:
        iid, tool_names, utt, neg, gold, flipped = item
        conds = make_conditions(item, rng, insert_pos)
        for cname, c in conds.items():
            rows.append({"item_id": iid, "condition": cname, "tools": [TOOLS[n] for n in tool_names],
                         "utterance_clean": utt, "transcript": c["transcript"], "spk_spans": c["spk_spans"],
                         "wer": c["wer"], "edits": c["edits"], "gold": gold, "flipped": flipped,
                         "meta": {k: v for k, v in c.items() if k not in ("transcript", "spk_spans", "wer", "edits")}})
    # P0c positive mirrors: one clean condition each, gold = flipped call (boolean genuinely wanted)
    for item in ITEMS:
        iid, tool_names, utt, neg, gold, flipped = item
        pu = POS_UTTERANCES[iid]
        rows.append({"item_id": iid + "_pos", "condition": "clean_pos", "tools": [TOOLS[n] for n in tool_names],
                     "utterance_clean": pu, "transcript": pu, "spk_spans": [(0, len(pu.split()), 1)], "wer": 0.0, "edits": 0,
                     "gold": flipped, "flipped": gold, "meta": {}})
    return rows

if __name__ == "__main__":
    import sys, collections
    rows = build(seed=int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    with open("trials.jsonl", "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    by = collections.defaultdict(list)
    for r in rows: by[r["condition"]].append(r["wer"])
    for k, v in by.items(): print(f"{k:14s} n={len(v):3d} meanWER={sum(v)/len(v):.3f}")
    print("wrote", len(rows), "trials")
