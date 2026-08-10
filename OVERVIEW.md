# idiom-probe: project overview for external review

Prepared 2026-08-10 for review. Repo: `github.com/MyatPyaePaingPie/idiom-probe`.
Status: literature phase and corpus groundwork complete; no model has been probed yet.
Feedback is most useful now, before the probe items are written and any inference is run.

## Summary

Can LLMs *deploy* idioms appropriately (production), not just explain them
(comprehension)? And are they worse at British idioms than American ones? A naive
British/American comparison is confounded: British idioms are rarer in training data,
and models are reliably worse on rare items. This project's contribution so far is the
groundwork that removes that confound: a set of 21 British/American idiom pairs matched
on *idiomatic-usage-adjusted* training-corpus frequency, built with measured (not
estimated) counts from the actual pretraining corpus. If a British deficit survives
frequency matching, rarity is ruled out as the explanation.

## Motivation and gap

Two gaps found in the literature phase (raw notes in `research/`, verification status
for every load-bearing claim in `VERIFICATION.md`):

1. Every English figurative-language benchmark found measures comprehension
   (classify, interpret, paraphrase). None measures production or appropriateness.
   The one benchmark with an appropriateness task, Chengyu-Bench (EMNLP 2025,
   arXiv:2506.18105), is Chinese. Leading models score >95% on its sentiment task but
   only ~85% on appropriateness and ~40% on open cloze: comprehension is near ceiling,
   deployment is not. No English equivalent exists.
2. Whether models handle British idioms worse than American ones appears unmeasured,
   despite dialect disparities being well documented elsewhere.

Mechanistic background (verified sources, arXiv:2506.01723 and arXiv:2511.16467):
idiom processing looks like retrieval plus arbitration, with dedicated attention heads
retrieving the figurative reading early while suppressing (not deleting) the literal
one. Pretraining frequency is the strongest evidenced predictor of item-level accuracy
(~70-point gap between top and bottom frequency deciles, arXiv:2202.07206).

## What has been built (all in this repo, all reproducible)

Pipeline (each data file has generating code, except the one hand step):

1. **Raw counts.** 80 candidate idioms (40 British, 40 American) counted in RedPajama
   (1.4T tokens) via the infini-gram API (`scripts/count_idioms.py`). Raw medians:
   British 4,552 vs American 34,161.
2. **Contamination measurement.** Raw n-gram counts conflate literal and idiomatic use
   ("hard cheese" is mostly actual cheese). Sampled attested usages per idiom from the
   corpus (`scripts/sample_usages.py`); 540 of 885 sampled snippets were classified
   literal-vs-idiomatic (first pass, 6-10 per idiom).
3. **The self-caught negative result.** We predicted contamination would
   systematically inflate British counts (more literally-plausible strings in the
   British set). Measured: mean idiomatic rate 0.881 British vs 0.882 American,
   statistically identical. Contamination is severe per item (4 idioms' counts are
   100% noise) but not variety-biased. Per-item screening is mandatory; aggregate
   variety correction is not.
4. **Adjusted frequencies and matching.** adjusted = raw x idiomatic rate
   (`scripts/compute_adjusted.py`), then greedy nearest-neighbour matching within a
   1.5x cap (`scripts/match_pairs.py`), yielding **21 matched pairs** (e.g. "Bob's
   your uncle" 4,870 vs "the ball is in your court" 7,283).

Standalone corpus finding: after adjustment, the median British idiom is **8.7x rarer**
than the median American one (3,905 vs 33,961) in the corpus measured.

## Planned experiment (not yet run)

**Instrument:** ~180 items over the matched pairs, five task types:
comprehension (calibration), appropriateness detection (English port of
Chengyu-Bench's task; register/region/domain violations), production under
constraints, hallucination traps (plausible fake idioms: invent or decline?), and
forced-choice logprob elicitation.

**Why logprobs:** open generation confounds competence with output probability
(McCoy et al.); forced-choice scoring separates them. Logprob elicitation runs first;
it is the cheapest task and directly tests both headline hypotheses.

**Hypotheses:**
- H1: item accuracy correlates with log adjusted frequency (predicted r > 0.6),
  regression over all ~76 usable items.
- H2: British idioms underperform American at matched frequency, paired Wilcoxon over
  the 21 pairs. n=21 powers a moderate-to-large effect only; a null is reported as
  such, not as evidence of no effect.
- H3: base models produce more varied figurative language than their instruct
  siblings (RLHF is known to compress diversity; whether it flattens figurative
  language specifically is unmeasured).

**Models and runner:** open models only, run locally (RTX 3060, Ollama or
llama.cpp; `scripts/preflight.py` live-verifies VRAM, logprob support, and model
availability before any run). Primary candidate pairing: OLMo 2 with the Dolma
index (verified present on infini-gram), which makes the frequency variable
corpus-exact rather than by-assumption. Llama 3 as generalization check. A planned
mechanistic follow-up uses Neuronpedia's public SAE API (verified working, zero GPU):
find idiom-selective features, measure per-token activations, and steer as a causal
check on the retrieval-vs-composition picture.

## Known limitations (self-reported)

- **Rater circularity.** The literal-vs-idiomatic classification was done by an LLM
  (Claude), single rater, no inter-rater agreement, and only tallies were retained.
  Classifier weakness on rare British items could leak into the labels. Rates near
  0 or 1 are robust; mid-range rates are not.
- **Exact-string counts.** infini-gram matches the exact tokenized form; inflected
  and case variants are uncounted, and the resulting bias is per item, unmeasured.
  A known substring artifact ("drop the ball" matches inside "drop the ballot") is
  documented but not yet corrected.
- **Regional labels** are the author's judgment, not from a dialect authority; some
  "British" items have US currency.
- **Corpus-model mismatch** for the current counts: RedPajama approximates Llama 1's
  corpus, not any current model's. The Dolma/OLMo re-count is the planned fix.
- **Small n.** 21 pairs limits H2 to detecting substantial effects.

Process note: the repo keeps a verification log (`VERIFICATION.md`) separating
VERIFIED / REFUTED / UNVERIFIED for every claim the design leans on, after two cases
where API availability asserted from documentation turned out to be false on a live
call. Claims in this overview marked "verified" were checked by direct fetch or API
call, not from secondary sources.

## Questions for the reviewer

1. **Matching methodology.** Greedy nearest-neighbour within 1.5x gave 21 pairs from
   37x39 candidates. Would optimal (min-cost) matching, caliper matching on log
   frequency, or covariate adjustment in regression (instead of matching at all) be
   preferable, given the small n?
2. **Power and stats.** For H2, is a paired Wilcoxon over 21 pairs plus a
   mixed-effects model over item-level responses (items nested in pairs, random item
   effects) the right combination? What would you pre-register?
3. **Rater circularity.** Beyond a second human rater over a subsample, what would
   make the contamination adjustment credible? Is the mid-range-rate fragility
   disqualifying for the affected items?
4. **Item design.** Any prior art on appropriateness-violation taxonomies (register,
   region, domain, anachronism) worth adopting, so the categories are principled
   rather than invented?
5. **Frequency variable.** Should the exact-string count be replaced by a
   variant-summed count (inflections, case), and is there a principled way to bound
   the error of not doing so?
6. **Is the corpus finding standalone?** Is the 8.7x adjusted rarity gap, plus the
   contamination-is-variety-neutral negative result, worth writing up on its own
   (short paper / workshop), independent of the model probe?
