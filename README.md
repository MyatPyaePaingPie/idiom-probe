# idiom-probe

**Question:** Can LLMs deploy slang and idioms (like "Bob's your uncle") in contextually
appropriate places, what predicts when they fail, and what is actually happening inside
the model when they succeed?

**Status:** Phase 1 (literature) complete, 2026-08-09. Phase 2 (probe design) pending decisions.

---

## Phase 1 findings

Raw agent output in `research/01-05*.md`. Synthesis below. **Verification status is marked
on every load-bearing claim** — see `VERIFICATION.md` for what was checked and what was not.

### 1. Idioms are retrieved, not composed

The mechanistic picture (UNVERIFIED, see caveat): dedicated attention heads fire on
idiomatic sequences and *suppress* the literal reading. Figurative meaning is retrieved
early (layers ~3-8); later layers (~8-16) adjudicate against context. The literal pathway
is not deleted, it is outcompeted. Multi-token expressions fuse into a single conceptual
unit before the figurative/literal branch point.

If this holds, it answers the framing question directly: the model is not reasoning its way
from "Bob" + "uncle" to "there you have it." It is doing lexical lookup of a stored unit,
then letting context arbitrate between two live readings. "Thought process" is the wrong
frame. It is closer to retrieval-plus-arbitration than to inference.

### 2. Frequency dominates everything else

Pretraining frequency is the strongest evidenced predictor of idiom accuracy. Linguistic
transparency (decomposable "spill the beans" vs opaque "kick the bucket") reportedly does
**not** predict performance.

Measured live via infini-gram against RedPajama (1.4T tokens, the LLaMA training corpus):

| Idiom | Count | Tokens (LLaMA) |
|---|---:|---|
| spill the beans | 103,423 | 5 |
| kick the bucket | 32,571 | 3 |
| taking the mickey | 12,802 | 4 (`mic`+`key`) |
| Bob's your uncle | 4,870 | 5 |

The motivating example is **21x rarer** than "spill the beans." Tokenization fragments it too.
Both are measurable per-item variables, so frequency stops being hand-waving and becomes a
regression line.

### 3. The measurement gap is real, and it is ours

Every English figurative-language benchmark found measures **comprehension** (classify,
interpret, paraphrase, retrieve). None measures **production** — whether a model deploys an
idiom appropriately, or detects that someone else has not.

The one benchmark with an appropriateness task is **Chengyu-Bench** (EMNLP 2025,
arXiv:2506.18105) — and it is Chinese. VERIFIED directly. Leading models score >95% on
sentiment but only ~85% on appropriateness and ~40% on open cloze. Comprehension is close
to solved; deployment is not.

**No English equivalent was found.** That is the hole this probe fills.

### 4. Dialect and region: measured for harm, unmeasured for idiom

Dialect disparities are well documented (AAVE sentencing bias, Hofmann et al. Nature 2024).
But whether models handle *British* idioms worse than American ones — the exact asymmetry
"Bob's your uncle" raises — appears **unmeasured**. Second gap we can fill cheaply.

### 5. Post-training compresses stylistic range

RLHF measurably reduces output diversity (Kirk et al., ICLR 2024). Whether it specifically
flattens *figurative* language is asserted but not measured. Third gap.

---

## Probe design (draft)

**Item set:** ~180 items, frequency-stratified using infini-gram counts (high >100/B,
mid 10-100/B, low <10/B), balanced across British / American / neutral origin.

**Five task types:**

1. **Comprehension** (baseline, calibrates against existing benchmarks)
2. **Appropriateness detection** — port of Chengyu-Bench's task to English. Given an idiom
   used in context, is it apt? Violation types: register (casual idiom in legal brief),
   region (British idiom in US-marked context), domain, anachronism.
3. **Production** — given meaning + register + audience + region constraints, deploy an idiom.
4. **Hallucination trap** — prompt for a plausible non-existent idiom. Does it invent or decline?
5. **Logprob elicitation** — P(idiom completion | context) directly, sidestepping generation.

**Why logprobs matter:** McCoy et al. showed models do worse on low-probability *outputs*
regardless of understanding. Open generation therefore confounds competence with output
probability. Forced-choice plus logprobs separates them.

**Primary hypothesis:** accuracy correlates with log(infini-gram frequency), r > 0.6.
**Secondary:** British-origin idioms underperform American at matched frequency (tests
whether corpus composition, not just raw count, drives the gap).
**Tertiary:** base models produce more varied figurative language than instruct siblings.

---

## Constraints

- No local GPU, no MPS. Hosted inference only (revisit if Colab is acceptable).
- Open models only. No Claude/GPT numbers, so claims are about open models, not "LLMs."
- Base-vs-instruct requires a provider serving raw base weights. OpenRouter does **not**
  (verified 2026-08-09: all Llama 3.x entries are instruct). Replicate does.

## Tooling verified working

- **infini-gram** — `POST https://api.infini-gram.io/`, index `v4_rpj_llama_s4`,
  `query_type: count`. No auth, ~40ms. Confirmed live.
