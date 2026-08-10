# Phase 2 results: building a frequency-matched British/American idiom set

Date: 2026-08-09. No model has been probed yet. Everything here is corpus measurement
and hand classification, which is exactly the groundwork the probe needs.

---

## What we set out to do

Test whether LLMs handle British idioms worse than American ones. The naive version of
this study is worthless: British idioms are rarer, models are worse at rare things
(Razeghi et al., ~70-point accuracy gap between top and bottom frequency decile,
VERIFIED), so "British idioms are harder" would just restate "these idioms are rarer."

The fix is **frequency matching**. Pair each British idiom with an American idiom of
equal corpus frequency. If a gap survives matching, rarity is not the explanation.

## Step 1: raw frequencies (n=80)

80 candidate idioms, 40 per variety, counted in RedPajama (1.4T tokens, the LLaMA
training corpus) via the infini-gram API.

Raw medians: **British 4,552 vs American 34,161** — a 7.5x population gap.
24 pairs matchable within 1.5x.

## Step 2: the confound

Raw n-gram counts do not distinguish idiomatic from literal usage. `hard cheese` scores
40,570, but sampling actual usages returns parmesan and cheddar, not the "bad luck"
sense. Matching on raw counts would pair a thousand real idiomatic uses against forty
thousand while appearing perfectly balanced.

**Predicted (wrongly) that this would bias against British idioms**, since the British
set contains more literally-plausible strings (hard cheese, spend a penny, full of beans,
over the moon, on your bike).

## Step 3: measuring the confound

Pulled 885 attested usages (up to 20 per idiom) from RedPajama via infini-gram
`search_docs`, centered on the needle. Hand-classified every one as literal or idiomatic.

**Result: the prediction was wrong.**

| | mean idiomatic rate | items with rate < 1.0 |
|---|---:|---:|
| British (n=40) | **0.881** | 9 / 40 |
| American (n=40) | **0.882** | 11 / 40 |

Contamination is severe at the item level and statistically identical between varieties.
Four idioms have a rate of exactly **zero** — their entire raw count is noise — and they
split across both varieties:

| Idiom | Raw | Idiomatic rate | Adjusted |
|---|---:|---:|---:|
| `the bases loaded` (US) | 196,488 | 0.00 | 0 |
| `on your bike` (UK) | 112,797 | 0.00 | 0 |
| `hard cheese` (UK) | 40,570 | 0.00 | 0 |
| `spend a penny` (UK) | 24,350 | 0.00 | 0 |
| `bought the farm` (US) | 27,770 | 0.17 | 4,628 |
| `a home run` (US) | 808,609 | 0.30 | 242,583 |

So: **per-item screening is mandatory, aggregate variety correction is not.** Anyone
running this study on raw counts would have four items that are pure noise, but would
not get a systematically biased British/American comparison.

## Step 4: the matched set

Dropped the 4 dead items. Matched on `adjusted = raw_count x idiomatic_rate`.

**21 matched pairs within 1.5x, mean within-pair ratio 0.87.** Full set in
`data/pairs.json`. The headline item survives matching:

```
Bob's your uncle          4,870   <->   the ball is in your court     7,283
```

## The population finding

After adjustment, median frequency is **3,905 (British) vs 33,961 (American) — an 8.7x
gap**. This is not itself a claim about models; it is a fact about the corpus. But it is
the reason the matched design is necessary, and it is a result in its own right: in the
corpus that trained LLaMA, British idioms are roughly an order of magnitude rarer than
American ones.

## Two artifacts found along the way

1. **Substring false matches.** `drop the ball` matches inside "drop the ball**ot**".
   Any idiom that is a prefix of a longer word has an inflated raw count. Needs a
   word-boundary check before the counts are trusted.
2. **Metalinguistic usage.** Low-frequency idioms return dictionary entries and
   "list of British idioms" pages rather than natural use (`a dog's dinner`: 3 of 6
   samples). These are idiomatic but not *usage*, and they may be exactly what a model
   memorizes. Worth tracking as a separate category.

## Status

- [x] Candidate set, 80 idioms
- [x] Raw frequencies (infini-gram, verified live)
- [x] 885 usages sampled and hand-classified
- [x] Adjusted frequencies + 21 matched pairs
- [ ] Write the probe items over the matched pairs
- [ ] Run against models
- [ ] Analysis

## Honest limitations

- Regional labels are my own judgment, not a dictionary source. `full of beans` and
  `take the biscuit` have US currency too. Labels need an external authority.
- Classification is mine alone: single rater, no second opinion, no inter-rater
  agreement. Rates near 0 or 1 are robust to this; mid-range ones (0.17, 0.30, 0.67)
  are not.
- 6-10 samples per idiom gives a rate estimate with wide error bars in the middle of the
  range. Fine for screening dead items, weak for fine-grained adjustment.
- RedPajama is LLaMA's corpus. Conclusions transfer to LLaMA-family models most
  directly, others by assumption.
