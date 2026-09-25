"""Bundle pilot sources into one self-contained Colab job (colab CLI has no upload; exec -f runs a single file)."""
import json, sys
files = {f: open(f).read() for f in ["seed_items.py", "inject.py", "run_pilot.py", "acoustic_p1.py"]}
models = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-3B-Instruct,Qwen/Qwen2.5-7B-Instruct-AWQ"
stage = sys.argv[2] if len(sys.argv) > 2 else "p0"   # p0 | p1 | both
gates = sys.argv[3] if len(sys.argv) > 3 else "none,confirm,confirm_generic,spktag"
src = f'''
import os, subprocess, time, shutil, json
t0 = time.time()
FILES = json.loads({json.dumps(json.dumps(files))})
WORK, OUT = "/content/pilot", "/content/out"
os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
for name, body in FILES.items():
    open(os.path.join(WORK, name), "w").write(body)
def sh(c):
    """Stream output line by line (the Colab client times out on long silences); drop tqdm spam, keep a heartbeat."""
    print(f"[stage] $ {{c[:90]}} ({{time.time()-t0:.0f}}s)", flush=True)
    p = subprocess.Popen(c, shell=True, cwd=WORK, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
    last = time.time(); tail = []
    for line in p.stdout:
        tail.append(line); tail = tail[-80:]
        if ("Processed prompts" in line or "it/s" in line) and time.time() - last < 60: continue
        print(line.rstrip()[-300:], flush=True); last = time.time()
    p.wait()
    if p.returncode != 0:
        print("".join(tail)[-6000:], flush=True); raise SystemExit(f"FAILED: {{c}}")
STAGE = "{stage}"
sh("nvidia-smi -L")
sh("python inject.py 0")
if STAGE == "p0d":
    _p = os.path.join(WORK, "trials.jsonl"); _rows = [l for l in open(_p) if json.loads(l)["condition"] == "clean_pos"]
    open(_p, "w").writelines(_rows); print(f"[stage] filtered to {{len(_rows)}} clean_pos trials", flush=True)
if STAGE in ("p1", "both"):
    sh("apt-get -qq install -y espeak-ng > /dev/null 2>&1; pip install -q kokoro soundfile faster-whisper 2>&1 | tail -2")
    sh(f"OUT_DIR={{OUT}}/asr python acoustic_p1.py --out {{OUT}}/asr 2>&1 | grep -v -i warning | tail -30")
sh("pip install -q vllm==0.11.2 2>&1 | tail -3")
for m in "{models}".split(","):
    tag = m.split("/")[-1]
    if STAGE in ("p0", "both", "p0d"):
        sh(f"VLLM_ATTENTION_BACKEND=TRITON_ATTN python run_pilot.py --backend vllm --model {{m}} --gates {gates} --out {{OUT}}/{{tag}} 2>&1 | grep -v -i warning | tail -40")
        shutil.copy(os.path.join(WORK, "trials.jsonl"), f"{{OUT}}/{{tag}}/trials.jsonl")
    if STAGE in ("p1", "both"):
        sh(f"VLLM_ATTENTION_BACKEND=TRITON_ATTN python run_pilot.py --trials {{OUT}}/asr/trials_asr.jsonl --backend vllm --model {{m}} --gates none,confirm --out {{OUT}}/{{tag}}_asr 2>&1 | grep -v -i warning | tail -40")
sh(f"cd {{OUT}} && tar czf /content/out.tgz . && ls -la /content/out.tgz")
print(f"[stage] all done in {{time.time()-t0:.0f}}s", flush=True)
'''
open("job_bundle.py", "w").write(src)
print("wrote job_bundle.py", len(src), "bytes; models:", models)
