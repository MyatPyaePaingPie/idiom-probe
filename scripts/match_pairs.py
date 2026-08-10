"""Build frequency-matched British/American idiom pairs from adjusted frequencies.

Matching is the methodological core of the probe: if British idioms underperform
American ones at EQUAL adjusted corpus frequency, rarity is ruled out as the cause.

Algorithm (greedy, reconstructed after the fact -- see provenance note below):
  1. Drop items with adjusted frequency 0 (their raw count is pure noise).
  2. Sort British idioms by adjusted frequency, ascending.
  3. Each British idiom takes the still-unused American idiom with the smallest
     ABSOLUTE difference in adjusted frequency, subject to the pair being within
     RATIO_CAP (1.5x) of each other. No candidate within the cap = unmatched.

This greedy is not globally optimal (a min-cost matching finds slightly better
total ratios) but it is what produced the committed set, and the committed set is
what RESULTS.md describes. Do not swap in a different matcher without regenerating
pairs.json and updating RESULTS.md together.

Provenance note: this script was written after data/pairs.json was first committed,
to close a reproducibility gap (the file originally had no generating code). The
algorithm above was reconstructed by testing candidates against the committed file
and is verified to reproduce it byte-for-byte, including pair order.

Reads  data/adjusted.json
Writes data/pairs.json  (ordered by British adjusted frequency, ascending)
"""

import json

RATIO_CAP = 1.5


def ratio(a: float, b: float) -> float:
    return max(a, b) / min(a, b)


def main() -> None:
    adj = json.load(open("data/adjusted.json"))
    brit = sorted(
        (r for r in adj if r["variety"] == "british" and r["adj"] > 0),
        key=lambda r: r["adj"],
    )
    amer = [r for r in adj if r["variety"] == "american" and r["adj"] > 0]

    used, pairs, unmatched = set(), [], []
    for b in brit:
        cands = [
            a
            for a in amer
            if a["idiom"] not in used and ratio(b["adj"], a["adj"]) <= RATIO_CAP
        ]
        if not cands:
            unmatched.append(b["idiom"])
            continue
        best = min(cands, key=lambda a: abs(b["adj"] - a["adj"]))
        used.add(best["idiom"])
        pairs.append({"british": b, "american": best})

    out = "data/pairs.json"
    with open(out, "w") as f:
        json.dump(pairs, f, indent=2)

    ratios = [ratio(p["british"]["adj"], p["american"]["adj"]) for p in pairs]
    print(f"{len(pairs)} pairs -> {out}")
    print(f"unmatched british ({len(unmatched)}): {unmatched}")
    print(f"mean british/american ratio: "
          f"{sum(p['british']['adj'] / p['american']['adj'] for p in pairs) / len(pairs):.3f}")
    print(f"mean symmetric (smaller/larger) ratio: "
          f"{sum(1 / r for r in ratios) / len(ratios):.3f}")
    print(f"worst pair ratio: {max(ratios):.3f} (cap {RATIO_CAP})")


if __name__ == "__main__":
    main()
