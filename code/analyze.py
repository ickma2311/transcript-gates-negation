"""Analyze pilot results: per (model, condition, gate) rates with bootstrap CIs, pre-registered contrasts H1-H3, and (P1) rank transfer."""
import json, sys, os, glob, collections, random
WRONG = {"WRONG_ACTION", "FLIPPED", "EXTRA_CALL"}
def load(path): return [json.loads(l) for l in open(path)]
def rate(rows, pred): return sum(pred(r) for r in rows) / max(1, len(rows))
def boot_diff(a, b, pred, n=5000, seed=0):
    """Paired bootstrap: resample card ids shared by both cells, then difference of rates."""
    rng = random.Random(seed)
    A = {r["item_id"]: r for r in a}; B = {r["item_id"]: r for r in b}
    ids = sorted(set(A) & set(B))
    if not ids: return float("nan"), float("nan")
    diffs = []
    for _ in range(n):
        smp = [rng.choice(ids) for _ in ids]
        diffs.append(sum(pred(A[i]) for i in smp)/len(smp) - sum(pred(B[i]) for i in smp)/len(smp))
    diffs.sort(); return diffs[int(0.025*n)], diffs[int(0.975*n)]
def did(by, c1, c2, g1, g0, pred, n=5000, seed=0):
    """Difference-in-differences: [rate(c1,g0)-rate(c1,g1)] - [rate(c2,g0)-rate(c2,g1)], paired bootstrap over cards."""
    cells = {k: {r["item_id"]: r for r in by.get(k, [])} for k in ((c1, g0), (c1, g1), (c2, g0), (c2, g1))}
    ids = sorted(set.intersection(*[set(v) for v in cells.values()])) if all(cells.values()) else []
    if not ids: return None
    def est(smp):
        f = lambda k: sum(pred(cells[k][i]) for i in smp)/len(smp)
        return (f((c1, g0)) - f((c1, g1))) - (f((c2, g0)) - f((c2, g1)))
    rng = random.Random(seed); bs = sorted(est([rng.choice(ids) for _ in ids]) for _ in range(n))
    return est(ids), bs[int(0.025*n)], bs[int(0.975*n)]
def table(rows):
    by = collections.defaultdict(list)
    for r in rows: by[(r["condition"], r["gate"])].append(r)
    print(f"{'condition':16s}{'gate':9s}{'n':>4s}{'WA':>7s}{'CF':>7s}{'OK':>7s}{'NOCALL':>8s}{'EXTRA':>7s}  wer")
    for (c, g), rs in sorted(by.items()):
        print(f"{c:16s}{g:9s}{len(rs):4d}{rate(rs, lambda r: r['outcome'] in WRONG)*100:7.1f}{rate(rs, lambda r: r['outcome']=='CONFIRM')*100:7.1f}"
              f"{rate(rs, lambda r: r['outcome']=='CORRECT')*100:7.1f}{rate(rs, lambda r: r['outcome']=='NO_CALL')*100:8.1f}{rate(rs, lambda r: r['outcome']=='EXTRA_ARG')*100:7.1f}  {sum(r['wer'] for r in rs)/len(rs):.3f}")
    return by
def contrasts(by):
    wa = lambda r: r["outcome"] in WRONG; cf = lambda r: r["outcome"] == "CONFIRM"
    def d(c1, g1, c2, g2, pred, name):
        a, b = by.get((c1, g1), []), by.get((c2, g2), [])
        if not a or not b: print(f"  {name}: missing cells"); return None
        diff = rate(a, pred) - rate(b, pred); lo, hi = boot_diff(a, b, pred)
        print(f"  {name}: {diff*100:+.1f}pp  [95% CI {lo*100:+.1f}, {hi*100:+.1f}]"); return diff
    print("Pre-registered contrasts:")
    h2 = d("neg_drop", "none", "func_drop", "none", wa, "H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp)")
    h1 = d("other_1w", "confirm", "neg_drop", "confirm", cf, "H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp)")
    h1b = d("other_intent", "confirm", "neg_drop", "confirm", cf, "H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary)")
    h3 = d("other_intent", "none", "other_intent", "spktag", wa, "H3  WA(other_intent) none - spktag             (GO needs >= +30pp)")
    h3b = d("clean", "spktag", "clean", "none", wa, "H3b WA(clean) spktag - none                    (must be <= +5pp)")
    d("neg_drop", "spktag", "neg_drop", "none", wa, "H3c WA(neg_drop) spktag - none                 (expected ~0)")
    d("other_1w_mid", "confirm", "neg_drop", "confirm", cf, "P0b CF(other_1w_mid) - CF(neg_drop) @confirm   (continue only if >= +25pp)")
    d("other_1w", "confirm_generic", "neg_drop", "confirm_generic", cf, "P0b CF(other_1w) - CF(neg_drop) @confirm_generic (non-leading prompt)")
    for gate in ("confirm", "confirm_generic"):
        for c in ("other_1w", "other_1w_mid"):
            x = did(by, c, "neg_drop", gate, "none", wa)
            if x: print(f"  DiD WA-reduction[{c}] - WA-reduction[neg_drop] under {gate}: {x[0]*100:+.1f}pp [95% CI {x[1]*100:+.1f}, {x[2]*100:+.1f}]")
    clean_cf = rate(by.get(("clean", "confirm"), []), cf)
    print(f"  clean false-confirm rate @confirm: {clean_cf*100:.1f}%  (must be <= 25%)")
    cf_all = [rate(by.get((c, "confirm"), []), cf) for c in ("neg_drop", "func_drop", "content_sub", "other_1w", "other_intent", "other_chatter") if (c, "confirm") in by]
    print(f"  CF on error conditions @confirm: {[round(x*100,1) for x in cf_all]}")
    go = (h1 is not None and h1 >= 0.25) and (h2 is not None and h2 >= 0.40) and clean_cf <= 0.25
    stop_gate_dead = cf_all and max(cf_all) < 0.10
    print(f"  => {'GO' if go else ('STOP (confirm gate dead)' if stop_gate_dead else 'NOT GO on this model')}")
def rank_transfer(text_rows, asr_rows):
    wa = lambda r: r["outcome"] in WRONG
    m = {"neg_drop": "asr_neg", "func_drop": "asr_func", "content_sub": "asr_content", "other_1w": "asr_other1w", "other_intent": "asr_otherfrag"}
    t = {k: rate([r for r in text_rows if r["condition"] == k and r["gate"] == "none"], wa) for k in m}
    a = {k: rate([r for r in asr_rows if r["condition"] == v and r["gate"] == "none"], wa) for k, v in m.items()}
    n = {k: len([r for r in asr_rows if r["condition"] == v and r["gate"] == "none"]) for k, v in m.items()}
    ks = list(m); rt = sorted(ks, key=lambda k: -t[k]); ra = sorted(ks, key=lambda k: -a[k])
    rank_t = {k: i for i, k in enumerate(rt)}; rank_a = {k: i for i, k in enumerate(ra)}
    dsum = sum((rank_t[k] - rank_a[k])**2 for k in ks); nn = len(ks); rho = 1 - 6*dsum/(nn*(nn*nn-1))
    for k in ks: print(f"  {k:14s} text WA {t[k]*100:5.1f}  asr WA {a[k]*100:5.1f} (n={n[k]})")
    print(f"  Spearman rho over {nn} types = {rho:.2f}  (GO needs >= 0.8 and every type n >= 30)")
def optbool_wrapper(rows, trials):
    """Deterministic post-filter on the none-gate outputs: if the (first) call sets any OPTIONAL boolean to true -> CONFIRM."""
    import run_pilot as rp
    out = []
    for r in rows:
        if r["gate"] != "none": continue
        t = trials[(r["item_id"], r["condition"])]
        calls = rp.parse_calls(r["raw"]); fired = False
        for c in calls:
            sch = next((tt["function"]["parameters"] for tt in t["tools"] if tt["function"]["name"] == c.get("name")), None)
            if not sch: continue
            req = set(sch.get("required", []))
            for k, v in (c.get("arguments") or {}).items():
                if isinstance(v, bool) and v and k not in req and sch["properties"].get(k, {}).get("type") == "boolean": fired = True
        r2 = dict(r); r2["gate"] = "wrapper_optbool"; r2["outcome"] = "CONFIRM" if fired else r["outcome"]; out.append(r2)
    return out
def p0c(by, model_dir):
    wa = lambda r: r["outcome"] in WRONG; cf = lambda r: r["outcome"] == "CONFIRM"
    print("P0c (optional-boolean confirmation rule):")
    for g in ("confirm_optbool", "wrapper_optbool"):
        if ("neg_drop", g) not in by: continue
        blocked = rate(by[("neg_drop", g)], cf); wa_neg = rate(by[("neg_drop", g)], wa)
        cn = rate(by.get(("clean", g), []), cf); cp = rate(by.get(("clean_pos", g), []), cf)
        pooled = by.get(("clean", g), []) + by.get(("clean_pos", g), []); cpool = rate(pooled, cf)
        wa_pos = rate(by.get(("clean_pos", g), []), wa)
        print(f"  [{g}] blocked(neg_drop)={blocked*100:.1f}%  WA(neg_drop)={wa_neg*100:.1f}%  CF(clean_neg)={cn*100:.1f}%  CF(clean_pos)={cp*100:.1f}%  CF(clean pooled 84)={cpool*100:.1f}%  WA(clean_pos)={wa_pos*100:.1f}%")
        for c in ("func_drop", "content_sub", "other_1w", "other_1w_mid", "other_intent"):
            if (c, g) in by: print(f"      CF({c})={rate(by[(c,g)], cf)*100:.1f}%  WA={rate(by[(c,g)], wa)*100:.1f}%")
        verdict = "WORTH 120-CARD CONFIRMATORY" if (blocked >= 0.60 and cpool <= 0.30) else "CLOSE"
        print(f"      => {verdict} (rule: blocked >= 60% and pooled clean CF <= 30%)")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "colab_out"
    for d in sorted(glob.glob(os.path.join(root, "*"))):
        f = os.path.join(d, "results.jsonl")
        if not os.path.isfile(f): continue
        rows = load(f)
        tpath = os.path.join(d, "trials.jsonl")
        if os.path.isfile(tpath) and any(r["gate"] == "none" for r in rows):
            trials = {(t["item_id"], t["condition"]): t for t in load(tpath)}
            if all((r["item_id"], r["condition"]) in trials for r in rows): rows = rows + optbool_wrapper(rows, trials)
        print(f"\n===== {d}  (n={len(rows)}) ====="); by = table(rows)
        # Contrast / decision logic needs the pre-registered cells; runs like p0d (positive mirrors only) get the descriptive table only.
        # p0/p0b (confirm gate present): pre-registered contrasts + decision; p0c (positive mirrors present): optional-boolean rule
        # evaluation; p0d (neither): descriptive table only.
        if d.endswith("_asr"):
            tf = os.path.join(d[:-4], "results.jsonl")
            if os.path.isfile(tf): print("Rank transfer text -> ASR:"); rank_transfer(load(tf), rows)
        elif {("neg_drop", "none"), ("func_drop", "none"), ("clean", "confirm")} <= set(by): contrasts(by)
        elif ("clean_pos", "none") in by and ("neg_drop", "none") in by: p0c(by, d)
        else: print("  (descriptive run: pre-registered contrast cells absent, no contrasts or decision computed)")
