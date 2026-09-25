"""Run trials x gates through an LLM (vLLM on GPU, HF or mock for smoke) and score tool-call outcomes.
Gates:
  none    : plain voice-assistant system prompt
  confirm : same + 'if a recognition error could change the action, reply CONFIRM: <question> instead of calling'
  spktag  : transcript shown with [speaker 1]/[speaker 2] tags (speaker 1 = enrolled user), run on ALL conditions; oracle labels
Outcome per trial: CORRECT | WRONG_ACTION | FLIPPED (neg_drop only: matches transcript-faithful call) | EXTRA_CALL | CONFIRM | NO_CALL | PARSE_FAIL
"""
import json, re, os, sys, time, argparse, collections

SYS_BASE = ("You are a voice assistant. The user's request below is an automatic speech-recognition transcript of what they said. "
            "Decide which tool to call, if any, and call it with the right arguments. Only set optional boolean arguments when the user "
            "clearly asked for them. If no tool applies, answer briefly in text.")
SYS_CONFIRM = SYS_BASE + (" Speech transcripts can contain recognition errors (a missing or extra word, a substituted word, or words from "
            "another person in the room). If such an error could change which action you take or how you fill an argument, do NOT call a tool; "
            "instead reply with exactly one line of the form 'CONFIRM: <one short yes/no question to the user>'. Otherwise call the tool.")
SYS_CONFIRM_GENERIC = SYS_BASE + (" If you are not confident about which action the user wants or how to fill an argument, do NOT call a tool; "
            "instead reply with exactly one line of the form 'CONFIRM: <one short yes/no question to the user>'. Otherwise call the tool.")
SYS_CONFIRM_OPTBOOL = SYS_BASE + (" Rule: before calling a tool, if the call would set any OPTIONAL boolean argument (one not listed as required) to true, "
            "do NOT call the tool; instead reply with exactly one line 'CONFIRM: <one short yes/no question naming that option>'. "
            "If no optional boolean would be set to true, call the tool directly.")
SYS_SPKTAG = SYS_BASE + (" The transcript is annotated with speaker tags. Only [speaker 1] is the enrolled user of this device; "
            "ignore anything said by other speakers, it is not addressed to you.")

def tag_transcript(row):
    toks = row["transcript"].split()
    parts = []
    for s, e, spk in row["spk_spans"]:
        parts.append(f"[speaker {spk}] " + " ".join(toks[s:e]))
    return " ".join(parts)

def build_messages(row, gate):
    if gate == "none": sys_p, user = SYS_BASE, row["transcript"]
    elif gate == "confirm": sys_p, user = SYS_CONFIRM, row["transcript"]
    elif gate == "confirm_generic": sys_p, user = SYS_CONFIRM_GENERIC, row["transcript"]
    elif gate == "confirm_optbool": sys_p, user = SYS_CONFIRM_OPTBOOL, row["transcript"]
    elif gate == "spktag": sys_p, user = SYS_SPKTAG, tag_transcript(row)
    else: raise ValueError(gate)
    return [{"role": "system", "content": sys_p}, {"role": "user", "content": user}]

TC_RE = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.S)
def parse_calls(text):
    calls = []
    for m in TC_RE.findall(text):
        try: calls.append(json.loads(m))
        except Exception: pass
    if not calls:  # fallback: bare json objects with name/arguments
        for m in re.findall(r"\{[^{}]*\"name\"[^{}]*\"arguments\"\s*:\s*\{[^{}]*\}[^{}]*\}", text, re.S):
            try: calls.append(json.loads(m))
            except Exception: pass
    return calls

def norm(v):
    if isinstance(v, str): return re.sub(r"[^a-z0-9]", "", v.lower())
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return int(v)
    return v

def call_matches(call, gold, tools=None):
    """Returns 'ok' | 'extra_arg' | False. extra_arg = gold matched but the call also set an argument the user never mentioned."""
    (gname, gargs), = gold.items()
    if call.get("name") != gname: return False
    args = call.get("arguments", {}) or {}
    schema = {}
    for t in (tools or []):
        if t["function"]["name"] == gname: schema = t["function"]["parameters"]["properties"]
    for k, v in args.items():  # enum violation or unknown argument = wrong action
        if k not in schema: return False
        en = schema[k].get("enum")
        if en and isinstance(v, str) and v.lower() not in [e.lower() for e in en]: return False
    for k, v in gargs.items():
        if isinstance(v, bool):
            if bool(args.get(k, False)) != v: return False
        elif isinstance(v, int):
            if norm(args.get(k)) != v: return False
        else:
            a = norm(args.get(k, ""))
            g = norm(v)
            if not (a == g or (g and g in a) or (a and a in g)): return False
    # extra booleans set true that gold has False or absent -> mismatch; other unrequested args -> extra_arg
    extra = False
    for k, v in args.items():
        if isinstance(v, bool) and v and not gargs.get(k, False): return False
        if k not in gargs and not isinstance(v, bool) and v not in (None, "", "none"): extra = True
    return "extra_arg" if extra else "ok"

def score(row, text):
    calls = parse_calls(text)
    if (re.search(r"^\s*CONFIRM\s*:", text, re.M | re.I) or re.search(r"\bCONFIRM:", text)) and not calls: return "CONFIRM"
    # a reply that both asks CONFIRM and emits a tool call is scored by the call (the action would execute)
    if not calls:
        return "NO_CALL" if text.strip() else "PARSE_FAIL"
    ok = [call_matches(c, row["gold"], row["tools"]) for c in calls]
    if any(ok) and len(calls) > 1: return "EXTRA_CALL"
    if ok and ok[0] == "ok": return "CORRECT"
    if ok and ok[0] == "extra_arg": return "EXTRA_ARG"
    if row["condition"] == "neg_drop" and any(call_matches(c, row["flipped"], row["tools"]) for c in calls): return "FLIPPED"
    return "WRONG_ACTION"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", default="trials.jsonl"); ap.add_argument("--backend", default="mock", choices=["mock", "hf", "vllm"])
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct"); ap.add_argument("--gates", default="none,confirm,spktag")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--out", default=os.environ.get("OUT_DIR", "out"))
    ap.add_argument("--max_tokens", type=int, default=200)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rows = [json.loads(l) for l in open(a.trials)]
    if a.limit: rows = rows[:a.limit]
    gates = a.gates.split(",")
    jobs = [(r, g) for r in rows for g in gates]   # spktag runs on every condition (non-insertion conditions are all [speaker 1])
    print(f"[stage] {len(jobs)} prompts, backend={a.backend}, model={a.model}", flush=True)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.model)
    prompts = [tok.apply_chat_template(build_messages(r, g), tools=r["tools"], tokenize=False, add_generation_prompt=True) for r, g in jobs]
    t0 = time.time()
    if a.backend == "mock":
        outs = []
        for r, g in jobs:
            (gname, gargs), = (r["flipped"] if r["condition"] == "neg_drop" else r["gold"]).items()
            outs.append(f"<tool_call>{json.dumps({'name': gname, 'arguments': gargs})}</tool_call>")
    elif a.backend == "hf":
        import torch
        from transformers import AutoModelForCausalLM
        m = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.float32)
        outs = []
        for i, p in enumerate(prompts):
            ids = tok(p, return_tensors="pt")
            with torch.no_grad(): g = m.generate(**ids, max_new_tokens=a.max_tokens, do_sample=False)
            outs.append(tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True))
            print(f"[progress] {i+1}/{len(prompts)} {time.time()-t0:.0f}s", flush=True)
    else:
        os.environ.setdefault("VLLM_ATTENTION_BACKEND", "TRITON_ATTN")
        from vllm import LLM, SamplingParams
        import torch
        print("[stage] cuda devices:", torch.cuda.device_count(), flush=True)
        llm = LLM(model=a.model, dtype="half", max_model_len=4096, gpu_memory_utilization=0.85)
        sp = SamplingParams(temperature=0, max_tokens=a.max_tokens)
        # throughput probe on first 32
        t1 = time.time(); probe = llm.generate(prompts[:32], sp); dt = time.time() - t1
        ntok = sum(len(o.outputs[0].token_ids) for o in probe)
        print(f"[stage] throughput probe: {ntok/dt:.0f} tok/s on 32 prompts ({dt:.1f}s)", flush=True)
        res = llm.generate(prompts, sp)
        outs = [o.outputs[0].text for o in res]
    print(f"[stage] generation done in {time.time()-t0:.0f}s", flush=True)
    tally = collections.Counter()
    with open(os.path.join(a.out, "results.jsonl"), "w") as f:
        for (r, g), o in zip(jobs, outs):
            s = score(r, o)
            tally[(r["condition"], g, s)] += 1
            f.write(json.dumps({"item_id": r["item_id"], "condition": r["condition"], "gate": g, "wer": r["wer"], "outcome": s, "raw": o, "model": a.model}) + "\n")
    order = ["clean", "clean_pos", "neg_drop", "func_drop", "content_sub", "other_1w", "other_1w_mid", "other_intent", "other_chatter"]
    seen = list(dict.fromkeys(r["condition"] for r in rows))
    conds = [c for c in order if c in seen] + [c for c in seen if c not in order]
    outcomes = ["CORRECT", "EXTRA_ARG", "FLIPPED", "WRONG_ACTION", "EXTRA_CALL", "CONFIRM", "NO_CALL", "PARSE_FAIL"]
    lines = [f"model={a.model}", "condition      gate      " + " ".join(f"{o[:8]:>8s}" for o in outcomes) + "     n"]
    for c in conds:
        for g in gates:
            n = sum(tally[(c, g, o)] for o in outcomes)
            if n == 0: continue
            lines.append(f"{c:14s} {g:9s} " + " ".join(f"{tally[(c,g,o)]/n*100:8.1f}" for o in outcomes) + f" {n:5d}")
    summary = "\n".join(lines); print(summary)
    open(os.path.join(a.out, "summary.txt"), "w").write(summary + "\n")

if __name__ == "__main__":
    main()
