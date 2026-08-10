"""Query infini-gram for corpus frequency of candidate idioms.

Frequency matching is the whole methodological point: if British idioms underperform
American ones at EQUAL corpus frequency, the cause is not rarity. Without matching,
"British idioms are harder" collapses to "these idioms are rarer".

Index v4_rpj_llama_s4 = RedPajama (1.4T tokens), the LLaMA training corpus.
"""

import json
import time
import urllib.request

API = "https://api.infini-gram.io/"
INDEX = "v4_rpj_llama_s4"

# Regional labels are provisional; see README "Labelling provenance" for the caveat.
BRITISH = [
    "Bob's your uncle", "taking the mickey", "throw a spanner in the works",
    "gone pear-shaped", "a damp squib", "not my cup of tea", "over the moon",
    "the bee's knees", "storm in a teacup", "donkey's years", "chalk and cheese",
    "swings and roundabouts", "a load of codswallop", "lose the plot",
    "a nosy parker", "off your trolley", "pop your clogs", "put a sock in it",
    "round the bend", "take the biscuit", "throw a wobbly", "know your onions",
    "full of beans", "a dog's dinner", "a curate's egg", "spend a penny",
    "all mouth and no trousers", "sod's law", "hard cheese", "chuffed to bits",
    "mad as a box of frogs", "see a man about a dog", "bang out of order",
    "the dog's bollocks", "cock a snook", "a right pig's ear", "on your bike",
    "plain as a pikestaff", "gone to pot", "a turn-up for the books",
]

AMERICAN = [
    "out of left field", "touch base", "a ballpark figure", "step up to the plate",
    "throw a curveball", "right off the bat", "cover all the bases", "jump the shark",
    "ride shotgun", "my two cents", "bought the farm", "close but no cigar",
    "the whole nine yards", "your John Hancock", "pass the buck", "hit the hay",
    "shoot the breeze", "go postal", "jump on the bandwagon", "drop the ball",
    "take a rain check", "hit it out of the park", "behind the eight ball",
    "a dime a dozen", "sell like hotcakes", "blow off steam", "plead the fifth",
    "a Hail Mary", "a slam dunk", "off base", "run interference",
    "Monday morning quarterback", "the bases loaded", "a home run",
    "back to the drawing board", "throw under the bus", "the ball is in your court",
    "bring your A game", "in the same ballpark", "call an audible",
]


def count(query: str, retries: int = 3) -> dict:
    payload = json.dumps(
        {"index": INDEX, "query_type": "count", "query": query}
    ).encode()
    req = urllib.request.Request(
        API, data=payload, headers={"Content-Type": "application/json"}
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - surface, never swallow
            if attempt == retries - 1:
                return {"error": str(e)}
            time.sleep(2**attempt)
    return {"error": "unreachable"}


def main() -> None:
    rows = []
    for variety, idioms in (("british", BRITISH), ("american", AMERICAN)):
        for idiom in idioms:
            res = count(idiom)
            if "error" in res or res.get("count") is None:
                print(f"  FAIL {idiom!r}: {res.get('error', res)}")
                continue
            rows.append(
                {
                    "idiom": idiom,
                    "variety": variety,
                    "count": res["count"],
                    "n_tokens": len(res.get("tokens", [])),
                    "tokens": res.get("tokens", []),
                }
            )
            print(f"  {variety:9s} {res['count']:>8,}  {idiom}")

    rows.sort(key=lambda r: -r["count"])
    out = "data/frequencies.json"
    with open(out, "w") as f:
        json.dump({"index": INDEX, "items": rows}, f, indent=2)
    print(f"\n{len(rows)} idioms counted -> {out}")

    zero = [r["idiom"] for r in rows if r["count"] == 0]
    if zero:
        print(f"ZERO-COUNT (unusable, drop): {zero}")


if __name__ == "__main__":
    main()
