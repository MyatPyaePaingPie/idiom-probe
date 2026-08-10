"""Preflight checks for the local probe runner (Windows box, RTX 3060, Ollama).

Settles the four unknowns that the probe design depends on, by calling the real
thing rather than trusting docs (see VERIFICATION.md for why):

  1. GPU + VRAM        -- does an 8B model fit at Q8 (~10 GB) or only Q4 (~6 GB)?
  2. Ollama logprobs   -- the logprob-elicitation task is the core of the probe.
                          Ollama historically did not expose logprobs; verify on
                          the installed version. Fallback: llama.cpp llama-server.
  3. Base-model tags   -- base-vs-instruct (H3) needs real base weights. Probe the
                          Ollama registry for candidate tags instead of assuming
                          (OpenRouter lesson: "base llama" listings can be a mirage).
  4. Dolma index       -- if infini-gram hosts a Dolma index, OLMo becomes the
                          corpus-exact headline model (RedPajama only approximates
                          Llama 1's corpus, and no current model's).

Usage (on the runner machine):
    python scripts/preflight.py [ollama_host]
ollama_host defaults to env OLLAMA_HOST or http://localhost:11434.
From WSL, if localhost does not reach the Windows Ollama, pass the Windows host IP.

Stdlib only. Read-only except for one 1-token generation against an already
installed model (for the logprobs check). Downloads nothing.
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

INFINIGRAM = "https://api.infini-gram.io/"
REGISTRY = "https://registry.ollama.ai/v2/library"

# Candidate tags for base (-text) and instruct weights. Probed against the
# registry manifest endpoint; found = tag exists, nothing is pulled.
TAG_CANDIDATES = [
    ("llama3", "8b-text-q8_0", "base"),
    ("llama3", "8b-text-q4_K_M", "base"),
    ("llama3", "8b-text-fp16", "base"),
    ("llama3", "8b-instruct-q8_0", "instruct"),
    ("llama3.1", "8b-text-q8_0", "base"),
    ("llama3.1", "8b-instruct-q8_0", "instruct"),
    ("olmo2", "7b", "unknown (check page)"),
    ("olmo2", "7b-1124-q8_0", "base?"),
    ("olmo2", "7b-1124-instruct-q8_0", "instruct"),
]

# Candidate infini-gram index names for Dolma (OLMo's training corpus).
DOLMA_CANDIDATES = [
    "v4_dolma-v1_7_llama",
    "v4_dolma-v1_6-sample_llama",
    "v4_dolma_v1_7",
]

TEST_QUERY = "Bob's your uncle"


def http_json(url, payload=None, headers=None, timeout=30):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {})
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def check_gpu() -> None:
    print("== 1. GPU / VRAM")
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=15,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  [FAIL] nvidia-smi not runnable ({e}). On WSL, run from Windows instead.")
        return
    if out.returncode != 0:
        print(f"  [FAIL] nvidia-smi error: {out.stderr.strip()}")
        return
    for line in out.stdout.strip().splitlines():
        print(f"  [PASS] {line.strip()}")
        try:
            mib = int(line.split(",")[1].strip().split()[0])
            if mib >= 10000:
                print("         8B fits at Q8 (~9-10 GB): use Q8 for the logprob task.")
            elif mib >= 6000:
                print("         8B fits at Q4 only. Q4 logprobs are noisier; consider")
                print("         partial CPU offload for a Q8 run (slower but sound).")
            else:
                print("         Under 6 GB: 8B needs heavy offload. Expect slow runs.")
        except (IndexError, ValueError):
            pass


def check_ollama(host: str) -> None:
    print(f"== 2. Ollama at {host}: server + logprobs")
    try:
        ver = http_json(f"{host}/api/version", timeout=10)
        print(f"  [PASS] server up, version {ver.get('version', '?')}")
    except Exception as e:  # noqa: BLE001 - surface, never swallow
        print(f"  [FAIL] cannot reach Ollama: {e}")
        print("         Start Ollama, or pass the right host (see usage in docstring).")
        return

    try:
        tags = http_json(f"{host}/api/tags", timeout=10).get("models", [])
    except Exception as e:  # noqa: BLE001
        print(f"  [FAIL] /api/tags: {e}")
        return
    if not tags:
        print("  [SKIP] no models installed; logprobs check needs one.")
        print("         Pull anything small (e.g. `ollama pull llama3.2:1b`) and rerun.")
        return
    model = min(tags, key=lambda m: m.get("size", 1 << 60))["name"]
    print(f"  installed models: {', '.join(m['name'] for m in tags)}")
    print(f"  logprobs probe uses smallest: {model}")

    # OpenAI-compatible completions endpoint with logprobs. This is the exact
    # call the probe's logprob-elicitation task needs.
    ok = False
    try:
        res = http_json(
            f"{host}/v1/completions",
            {"model": model, "prompt": "The capital of France is", "max_tokens": 1,
             "temperature": 0, "logprobs": 5},
            timeout=120,
        )
        lp = (res.get("choices") or [{}])[0].get("logprobs")
        if lp and (lp.get("token_logprobs") or lp.get("content") or lp.get("tokens")):
            print(f"  [PASS] /v1/completions returns logprobs: {json.dumps(lp)[:120]}...")
            ok = True
        else:
            print(f"  [FAIL] /v1/completions answered but logprobs field is {lp!r}")
    except Exception as e:  # noqa: BLE001
        print(f"  [FAIL] /v1/completions with logprobs: {e}")

    if not ok:
        try:
            res = http_json(
                f"{host}/v1/chat/completions",
                {"model": model, "max_tokens": 1, "temperature": 0,
                 "logprobs": True, "top_logprobs": 5,
                 "messages": [{"role": "user", "content": "Say hi"}]},
                timeout=120,
            )
            lp = (res.get("choices") or [{}])[0].get("logprobs")
            if lp and lp.get("content"):
                print(f"  [PASS] /v1/chat/completions returns logprobs: {json.dumps(lp)[:120]}...")
                ok = True
            else:
                print(f"  [FAIL] /v1/chat/completions logprobs field is {lp!r}")
        except Exception as e:  # noqa: BLE001
            print(f"  [FAIL] /v1/chat/completions with logprobs: {e}")

    if not ok:
        print("  VERDICT: this Ollama does NOT expose logprobs. Fallback for the")
        print("  logprob task: llama.cpp llama-server (CUDA build) with the same GGUF,")
        print("  which serves an OpenAI-compatible API with logprobs. Ollama remains")
        print("  fine for the generation tasks (production, hallucination trap).")


def check_registry_tags() -> None:
    print("== 3. Ollama registry: base / instruct tag existence (no downloads)")
    hdr = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
    for repo, tag, kind in TAG_CANDIDATES:
        url = f"{REGISTRY}/{repo}/manifests/{tag}"
        try:
            http_json(url, headers=hdr, timeout=15)
            print(f"  [FOUND]     {repo}:{tag}  ({kind})")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  [NOT FOUND] {repo}:{tag}")
            else:
                print(f"  [ERROR]     {repo}:{tag}: HTTP {e.code}")
        except Exception as e:  # noqa: BLE001
            print(f"  [ERROR]     {repo}:{tag}: {e}")
    print("  Full tag lists: https://ollama.com/library/<model>/tags")
    print("  If no base OLMo tag exists, fallback is llama.cpp + a GGUF from HF.")


def check_dolma_index() -> None:
    print("== 4. infini-gram: Dolma index (for corpus-exact OLMo pairing)")
    found = None
    for idx in DOLMA_CANDIDATES:
        try:
            res = http_json(
                INFINIGRAM,
                {"index": idx, "query_type": "count", "query": TEST_QUERY},
                timeout=30,
            )
        except Exception as e:  # noqa: BLE001
            print(f"  [ERROR]     {idx}: {e}")
            continue
        if "error" in res:
            print(f"  [NOT FOUND] {idx}: {str(res['error'])[:100]}")
        else:
            print(f"  [FOUND]     {idx}: count({TEST_QUERY!r}) = {res.get('count'):,}")
            if found is None:  # candidates are ordered best-first
                found = idx
    if not found:
        # A bogus index name makes the API enumerate what it does serve.
        try:
            res = http_json(
                INFINIGRAM,
                {"index": "bogus_index_name", "query_type": "count", "query": TEST_QUERY},
                timeout=30,
            )
            print(f"  server's own index list (from error): {str(res.get('error'))[:400]}")
        except Exception as e:  # noqa: BLE001
            print(f"  [ERROR] could not elicit index list: {e}")
    else:
        print(f"  Next: rerun count_idioms.py with INDEX = {found!r} and OLMo as headline model.")


def main() -> None:
    host = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("OLLAMA_HOST")
            or "http://localhost:11434")
    if not host.startswith("http"):
        host = "http://" + host
    host = host.rstrip("/")

    print("idiom-probe runner preflight (all checks are live calls, none download)")
    print()
    check_gpu()
    print()
    check_ollama(host)
    print()
    check_registry_tags()
    print()
    check_dolma_index()
    print()
    print("Done. Anything [FAIL]/[NOT FOUND] above is a design decision, not a detail:")
    print("no logprobs -> serve with llama.cpp; no base tag -> GGUF from HF;")
    print("no Dolma index -> Llama-family stays the headline, corpus match by assumption.")


if __name__ == "__main__":
    main()
