"""Pull attested usages of each candidate idiom from RedPajama via infini-gram.

Purpose: raw n-gram counts conflate literal and idiomatic usage, and the contamination
is systematically WORSE for British idioms in our set (many are literally-plausible
strings: "hard cheese", "spend a penny", "full of beans"). Matching on raw counts would
manufacture a false "British idioms are harder" result.

So: sample real usages, hand-classify literal vs idiomatic, and match on
    adjusted_freq = raw_count * idiomatic_rate

Output feeds manual classification. Snippets are centered on the needle and trimmed so a
human can judge each in one line.
"""

import json
import time
import urllib.request

API = "https://api.infini-gram.io/"
INDEX = "v4_rpj_llama_s4"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (idiom-probe research)",
}
WINDOW = 110  # chars either side of the needle
MAXNUM = 10  # hard API cap per call
ROUNDS = 1  # each call returns a fresh random sample; raise for deeper stage-2 sampling


def search_docs(query: str, n: int, retries: int = 3) -> dict:
    payload = json.dumps(
        {"index": INDEX, "query_type": "search_docs", "query": query, "maxnum": n}
    ).encode()
    req = urllib.request.Request(API, data=payload, headers=HEADERS)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - surface, never swallow
            if attempt == retries - 1:
                return {"error": str(e)}
            time.sleep(2**attempt)
    return {"error": "unreachable"}


def snippet(doc: dict, needle: str) -> str | None:
    spans = doc.get("spans") or []
    txt = "".join(s[0] if isinstance(s, (list, tuple)) else str(s) for s in spans)
    i = txt.lower().find(needle.lower())
    if i < 0:
        return None  # needle outside the returned window; unusable for judging
    seg = txt[max(0, i - WINDOW) : i + len(needle) + WINDOW]
    return " ".join(seg.split())


def main() -> None:
    freqs = json.load(open("data/frequencies.json"))["items"]
    out = []
    for k, row in enumerate(freqs, 1):
        idiom = row["idiom"]
        snips, seen = [], set()
        for _ in range(ROUNDS):
            res = search_docs(idiom, MAXNUM)
            if "error" in res:
                print(f"[{k}/{len(freqs)}] FAIL {idiom!r}: {res['error']}")
                break
            for doc in res.get("documents", []):
                s = snippet(doc, idiom)
                if s and s not in seen:
                    seen.add(s)
                    snips.append(
                        {"text": s, "source": (doc.get("metadata") or "")[:80]}
                    )
            time.sleep(0.3)
        out.append(
            {
                "idiom": idiom,
                "variety": row["variety"],
                "raw_count": row["count"],
                "n_usable": len(snips),
                "samples": snips,
            }
        )
        print(f"[{k}/{len(freqs)}] {idiom:34s} {len(snips):>2} usable")
        time.sleep(0.4)

    with open("data/usages.json", "w") as f:
        json.dump(out, f, indent=2)
    total = sum(r["n_usable"] for r in out)
    print(f"\n{len(out)} idioms, {total} usable snippets -> data/usages.json")


if __name__ == "__main__":
    main()
