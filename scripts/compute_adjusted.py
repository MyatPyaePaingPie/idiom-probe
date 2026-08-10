"""Compute contamination-adjusted frequencies: adjusted = raw_count * idiomatic_rate.

Raw n-gram counts conflate literal and idiomatic usage (see RESULTS.md step 2).
The idiomatic rate for each idiom comes from hand-classified usage samples in
data/classifications.json (tallies only; per-snippet verdicts were not retained).

Provenance note: this script was written after data/adjusted.json was first
committed, to close a reproducibility gap (the file originally had no generating
code). It has been verified to reproduce the committed file byte-for-byte.

Reads  data/frequencies.json, data/classifications.json
Writes data/adjusted.json  (same item order as frequencies.json: raw count desc)
"""

import json


def main() -> None:
    freqs = json.load(open("data/frequencies.json"))["items"]
    cls = json.load(open("data/classifications.json"))["items"]

    rows = []
    for r in freqs:
        c = cls[r["idiom"]]
        rate = c["idiomatic"] / c["n"]
        rows.append(
            {
                "idiom": r["idiom"],
                "variety": r["variety"],
                "raw": r["count"],
                "rate": rate,
                "adj": r["count"] * rate,
                "n": c["n"],
            }
        )

    out = "data/adjusted.json"
    with open(out, "w") as f:
        json.dump(rows, f, indent=2)

    dead = [r["idiom"] for r in rows if r["adj"] == 0]
    print(f"{len(rows)} items -> {out}")
    print(f"dead items (rate 0, entire raw count is noise): {dead}")


if __name__ == "__main__":
    main()
