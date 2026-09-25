"""Recompute the pair-level facts quoted in the note's §2–§3 from the raw P0c/P0 outputs.
Usage: python code/pair_check.py results/p0c results/p0"""
import json, sys, collections
p0c, p0 = sys.argv[1], sys.argv[2]
for m in ["Qwen2.5-3B-Instruct", "Qwen2.5-7B-Instruct-AWQ"]:
    tr = [json.loads(l) for l in open(f"{p0c}/{m}/trials.jsonl")]
    neg = {t["item_id"]: t for t in tr if t["condition"] == "neg_drop"}
    pos = {t["item_id"][:-4]: t for t in tr if t["condition"] == "clean_pos"}
    same = [i for i in neg if neg[i]["transcript"] == pos[i]["transcript"]]
    butand = [i for i in neg if i not in same and neg[i]["transcript"].replace(" but ", " and ") == pos[i]["transcript"]]
    other = [i for i in neg if i not in same and i not in butand]
    raw = {(r["item_id"], r["condition"], r["gate"]): r["raw"] for r in map(json.loads, open(f"{p0c}/{m}/results.jsonl"))}
    ident = {g: sum(raw[(i, "neg_drop", g)] == raw[(i + "_pos", "clean_pos", g)] for i in same) for g in ("none", "confirm_optbool")}
    len_ = {(r["item_id"], r["condition"], r["gate"]): r["outcome"] for r in map(json.loads, open(f"{p0c}/{m}/results_lenient.jsonl"))}
    pairs18 = same + butand
    flip_and_correct = sum(len_[(i, "neg_drop", "none")] == "FLIPPED" and len_[(i + "_pos", "clean_pos", "none")] == "CORRECT" for i in pairs18)
    c = collections.Counter(r["outcome"] for r in map(json.loads, open(f"{p0/'' if False else p0}/{m}/results_lenient.jsonl")) if r["condition"] == "neg_drop" and r["gate"] == "none")
    pos_ok = sum(len_[(i + "_pos", "clean_pos", "none")] == "CORRECT" for i in neg)
    print(f"{m}: verbatim-identical pairs {len(same)}/42 {sorted(same)}; but/and-only {len(butand)}/42; other {len(other)}/42")
    print(f"   identical raw outputs on the {len(same)} pairs: {ident}")
    print(f"   on the {len(pairs18)} pairs (identical or but/and): neg_drop=FLIPPED & clean_pos=CORRECT @none: {flip_and_correct}/{len(pairs18)}")
    print(f"   P0 neg_drop @none (lenient): {dict(c)}; P0c clean_pos CORRECT @none: {pos_ok}/42")
