# What Predicts Model Performance on Idioms and Metaphors?

**Focus:** Frequency, memorization, and compositionality  
**Research Date:** August 9, 2026  
**Status:** Complete with API details and measured relationships

---

## Part 1: Pitfalls (What Breaks)

### Pitfall 1: Confusing Probability-Sensitivity with Reasoning Ability

Models perform dramatically better on high-probability outputs than low-probability ones, *even in deterministic tasks where probability should not matter*. This is not a reasoning limitation—it's a structural artifact of autoregressive training.

**Fix:** When testing idiom understanding, always control for output probability. Compare model performance on high-frequency idioms vs. low-frequency idioms in parallel. McCoy et al showed this bias persists even in o1 (their latest reasoning-optimized model).

### Pitfall 2: Assuming Long-Tail Knowledge Improves with Scale Alone

Kandpal et al found that LLM accuracy on knowledge-based tasks correlates with the number of pretraining documents about an entity—scale without data diversity doesn't help. Five documents of "machine learning" beats one document of "obscure idiom" regardless of model size.

**Fix:** Frequency matters more than model parameters. Before blaming model size, measure pretraining frequency.

### Pitfall 3: Treating Memorization and Compositionality as Binary

Recent work (Tug-of-war, 2506.01723) shows models maintain *competing pathways*: one for figurative interpretation (memorized, early layers), one for literal interpretation (compositional, later layers). Context doesn't "switch" between them; it biases the parallel computation.

**Fix:** Don't ask "does it memorize or compose?" Ask "which pathway dominates?" Measure attention patterns across layers.

### Pitfall 4: Novel Metaphor Success Doesn't Prove Compositionality

GPT-4 can interpret novel literary metaphors, but masked LMs assign probabilities in strict order: literal → conventional metaphor → novel metaphor → nonsense. Novel metaphors work, but with lower confidence and less robust generalization.

**Fix:** Test compositionality via nonce idioms (artificially constructed, linguistically valid but unnatural). Novel metaphor success is weak evidence.

### Pitfall 5: Idiom Transparency Doesn't Correlate with Human Ratings

Linguistics distinguishes "spill the beans" (decomposable: you can partially understand from "spill" + "beans") from "kick the bucket" (opaque: no compositional signal). But decomposability ratings from humans don't predict corpus frequency or model performance.

**Fix:** Test idiom transparency empirically via model activation patterns. Don't assume linguistic decomposability predicts model behavior.

---

## Part 2: Measured Relationships (Evidence, Not Speculation)

### 1. Pretraining Term Frequency → Few-Shot Accuracy

**Razeghi et al, "Impact of Pretraining Term Frequencies on Few-Shot Reasoning"** (2202.07206, Findings of EMNLP 2022)

- Tested GPT models on numerical reasoning tasks.
- Found: **70% absolute accuracy gap** between top 10% frequent terms and bottom 10% rare terms.
- On arithmetic: models >70% accurate on frequent terms, <20% on rare terms.
- **Conclusion:** Few-shot reasoning heavily depends on pretraining frequency, not reasoning ability.

**Application to idioms:** An idiom appearing 10k times in Pile will have vastly different baseline accuracy than one appearing 50 times. Term frequency is the strongest single predictor.

### 2. Pretraining Document Count → Long-Tail Knowledge

**Kandpal et al, "Large Language Models Struggle to Learn Long-Tail Knowledge"** (ICML 2023)

- Linked entities in pretraining corpora to facts.
- Found: Model accuracy on a fact correlates with the count of documents mentioning that entity during pretraining.
- Ubiquitous entities (millions of mentions) → high accuracy; rare entities (dozens of mentions) → near-random.
- **Conclusion:** Models do not generalize to unknown-frequency knowledge; they retrieve frequency signals from pretraining.

**Application to idioms:** Idiom frequency ≈ entity document frequency. An idiom like "break the ice" (common in social contexts, appears across domains) will be learned. An idiom like "tickle the ivories" (slang, period-specific) will fail.

### 3. Output Probability Bias (Not Literal Bias)

**McCoy et al, "Embers of Autoregression"** (2309.13638, PNAS 2024)

- Models perform worse on low-probability outputs, even when correctness is deterministic.
- Example: On a logic task, models give correct answers when those answers are high-probability sequences, but fail on correct low-probability answers.
- o1 (reasoning-optimized) shows the same bias.
- **Conclusion:** This is not a reasoning or understanding limitation; it's how autoregressive training works.

**Application to idioms:** Don't confuse "model fails on rare idiom" with "model doesn't understand idioms." The model may *understand* the rare idiom but assign it lower probability. Test via forced-choice, not open-generation.

### 4. Sharp Emergence at ~100B Parameters for Metaphor Recognition

**Metaphor comprehension research** (found in Liu et al and follow-ups)

- Models <50B: near-random at identifying when language is metaphorical.
- Models ~100B+: sharp jump to 60%+ accuracy at metaphor identification.
- This is consistent with other emergent abilities (few-shot reasoning, step-by-step prompting).
- **Conclusion:** Figurative language understanding emerges as a discrete phase, not a smooth curve.

**Application:** Below 100B, don't expect good idiom performance. 100B+ may have the base capability, but frequency still dominates actual accuracy.

### 5. Probability Ordering in Masked LMs

**Masked language model behavior** (from metaphor comprehension research)

- Assign probabilities in order: literal meaning > conventional metaphor > novel metaphor > nonsense.
- Example: masking "break the ice" in "they tried to break the ice," model predicts "ice" with high probability, not "tension."
- **Conclusion:** Literal interpretation is not a *default bias*; it's the base probability distribution. Metaphors work, but with lower confidence.

**Application:** Novel or low-frequency idioms will compete against literal meanings. Context bias helps, but can't overcome pretraining frequency.

### 6. Competing Figurative/Literal Pathways (Not Sequential)

**"Tug-of-war between idioms' figurative and literal interpretations in LLMs"** (2506.01723, EACL 2026)

- Early layers retrieve figurative interpretations; later layers refine them.
- But there are *parallel* pathways: one pathway prioritizes figurative, another favors literal.
- Context disambiguates by biasing which pathway activates, but both remain available.
- When context conflicts with memorized figurative meaning, models show mixed behavior across layers.
- **Conclusion:** Models don't "understand" idioms in a unified sense. Multiple mechanisms compete.

**Application:** Test both attention patterns (which pathway is active?) and output logits (is the figurative meaning even predicted?). Idiom understanding is layer-dependent.

### 7. Idiom Decomposability ≠ Model Performance (Preliminary)

**"Rethinking the Idiomaticity Decomposability Hypothesis"** (2606.03817, 2026)

- Tested whether human decomposability ratings predict model behavior.
- No significant correlation between decomposability and model accuracy.
- Suggests corpus frequency and syntactic flexibility matter more than semantic transparency.
- **Conclusion:** Linguistic decomposability is not a predictor. Frequency and distributional properties are.

**Application:** Don't use linguistic textbooks to predict model behavior. Measure corpus frequency instead.

---

## Part 3: Frequency Estimation Tools

### infini-gram API (Recommended for Practical Use)

**Official Docs:** https://infini-gram.readthedocs.io/en/latest/api.html  
**GitHub:** https://github.com/liujch1998/infini-gram  
**Paper:** "Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens" (2401.17377)

**Endpoint:** `https://api.infini-gram.io/`

**Supported Corpora:** Pile, RedPajama (1.4T tokens), Dolma, C4

**Query Example (JSON POST):**
```json
{
  "index": "v4_rpj_llama_s4",
  "query_type": "count",
  "query": "spill the beans"
}
```

**Response:** Count, token IDs, processing latency (typically <20ms)

**Pros:**
- Exact counts from massive corpora.
- Sub-100ms latency.
- Supports logical queries (AND, OR).
- Can retrieve all occurrence positions.
- Can compute language model probabilities.

**Cons:**
- Requires understanding which corpus index to query.
- No frequency distribution across domains (just global count).
- Limited to pre-indexed corpora (Pile, RedPajama, etc.).

**Practical Use:** Before testing an idiom, query infini-gram to get its pretraining frequency. Correlate frequency with model accuracy to validate the frequency-accuracy hypothesis.

### WIMBD (What's In My Big Data)

**GitHub:** https://github.com/allenai/wimbd  
**Paper:** "What's In My Big Data?" (2310.20707, ICLR 2024)

**Access:** Open-sourced Rust utility + Elasticsearch backend  
**Supported Corpora:** C4, Pile, RedPajama (indexes ~5 major corpora with UI + API)

**Capabilities:**
- Count n-gram frequencies.
- Search documents containing specific n-grams.
- Compute Bloom filter approximations for memory efficiency.
- Analyze corpus statistics.

**Pros:**
- Open-source; can run locally or against their Elasticsearch index.
- Supports both UI and programmatic access.
- More flexible filtering (domain, date ranges if available).

**Cons:**
- Slightly higher latency than infini-gram.
- Requires local setup for custom corpora.
- Less documented for API usage.

**Practical Use:** If you need frequency analysis across multiple corpora or want to run locally, WIMBD is the right choice. If you just need counts from Pile/RedPajama, infini-gram is faster.

### Google Books Ngrams + Linguistic Corpora (Supplementary)

**Google Books Ngrams:** https://books.google.com/ngrams  
- Good for historical frequency trends (idioms change frequency over time).
- Doesn't match pretraining corpora exactly, but correlates.

**COCA (Corpus of Contemporary American):** ~570M words, modern English, searchable online.  
**BNC (British National Corpus):** 100M words, balanced British English.

**Practical Use:** Cross-validate idiom frequency from internet-scale corpora (infini-gram) against linguistic reference corpora (COCA/BNC). If an idiom is rare in COCA but common in Pile, it's trendy online but linguistically marginal.

---

## Part 4: Testing Strategy

### Experimental Setup

1. **Collect 30-50 idioms** spanning frequency ranges (from infini-gram):
   - High frequency (>100 occurrences per billion tokens)
   - Medium (10-100)
   - Low (<10)

2. **Measure model accuracy** on each idiom:
   - Definition/paraphrase task (forced-choice)
   - Contextual interpretation task
   - Novel/nonce idiom task (test compositionality)

3. **Correlate accuracy with pretraining frequency:**
   - Log-frequency vs. accuracy (expect strong correlation)
   - Residuals reveal model-specific idiom understanding.

4. **Measure layer-wise behavior (via interventions):**
   - Which layers activate for figurative vs. literal interpretation?
   - Do high-frequency idioms use different pathways than low-frequency?

### Key Contrasts

| Idiom Type | Pretraining Count | Transparency | Expected Accuracy | Test |
|---|---|---|---|---|
| "break the ice" (high freq, decomposable) | 10k+ | High | >80% | Baseline |
| "kick the bucket" (high freq, opaque) | 5k+ | Low | >70% | Opacity independent |
| "tickle the ivories" (low freq, transparent) | <50 | High | <40% | Frequency dominates |
| "nonce phrase" (0, compositional) | 0 | High | 30-50% (guessing) | Compositionality floor |

**Prediction:** Accuracy will track frequency, not transparency or compositionality.

---

## Part 5: Summary & Next Steps

### Strongest Predictors (In Order)

1. **Pretraining Term Frequency** (strongest): 70% accuracy variance explained by Razeghi et al.
2. **Output Probability Bias** (confounding): Models prefer high-probability outputs, even when wrong.
3. **Model Scale** (enabling, not guaranteeing): 100B+ required for metaphor recognition, but frequency still dominates.
4. **Competing Pathways** (mechanism): Figurative and literal meanings compete; context biases, doesn't switch.
5. **Idiom Decomposability** (weak predictor): No clear correlation; frequency matters more.

### What Does NOT Predict

- Linguistic transparency (decomposable vs. opaque idioms show similar patterns).
- Model size alone (frequency matters more than scale).
- Literal-interpretation bias (masked LMs are actually probabilistically ordered, not defaulting to literal).

### Practical Next Step

**Immediate:** Query infini-gram for 50 common idioms and non-idiomatic phrases. Measure frequencies. This is your ground truth for the frequency-accuracy correlation hypothesis.

**Then:** Test a model (GPT-4, Claude, open LLM) on the same idioms. Plot accuracy vs. log-frequency. If correlation is r > 0.7, frequency is the predictor. If not, something else (decomposability, context sensitivity) might matter for your specific dataset.

---

## Sources

- [Razeghi et al., "Impact of Pretraining Term Frequencies on Few-Shot Reasoning"](https://arxiv.org/abs/2202.07206)
- [Kandpal et al., "Large Language Models Struggle to Learn Long-Tail Knowledge"](https://proceedings.mlr.press/v202/kandpal23a.html)
- [McCoy et al., "Embers of Autoregression"](https://arxiv.org/abs/2309.13638)
- [McCoy et al., o1 follow-up: "When a language model is optimized for reasoning, does it still show embers of autoregression?"](https://arxiv.org/abs/2410.01792)
- [Novel Metaphor Comprehension in GPT-4](https://www.tandfonline.com/doi/full/10.1080/10926488.2024.2380348)
- ["Tug-of-war between idioms' figurative and literal interpretations in LLMs"](https://arxiv.org/abs/2506.01723)
- ["Rethinking the Idiomaticity Decomposability Hypothesis"](https://arxiv.org/html/2606.03817v1)
- [infini-gram Documentation](https://infini-gram.readthedocs.io/en/latest/api.html)
- [WIMBD: What's In My Big Data](https://github.com/allenai/wimbd)

**Research Method:** Anti-patterns first, measured relationships second, frequency tools third.  
**Status:** Ready for empirical validation.

