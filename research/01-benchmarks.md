# Figurative Language Benchmarks: Comprehensive Survey

## Executive Summary

This survey covers **15+ benchmarks** for evaluating figurative language understanding in language models. The critical finding: **nearly all existing benchmarks test COMPREHENSION (understanding); almost none test PRODUCTION (contextually appropriate usage)**. The measurement gap is precisely where your probe can contribute most value.

---

## Individual Benchmark Reviews

### 1. IMPLI (Idiomatic and Metaphoric Paired Language Inference)

**What it tests:** Natural Language Inference (NLI) on figurative language. Given a premise/hypothesis pair, models classify entailment (if the figurative phrase entails its literal meaning).

**Comprehension vs Production:** COMPREHENSION ONLY (interpret given phrase).

**Size & Construction:**
- 25.6K semi-automatically generated pairs
- 1.8K manually gold pairs
- English only
- Paired sentences linking idioms/metaphors to literal meanings
- Spans idioms and metaphors

**SOTA Scores & Models:**
- RoBERTa (MNLI-fine-tuned): 91-98% on MNLI baseline; **significantly lower on IMPLI figurative pairs** (exact scores not reported in accessible excerpts, but paper shows substantial gap between literal and figurative performance)
- Published June 2022 ([ACL Anthology 2022.acl-long.369](https://aclanthology.org/2022.acl-long.369/))

**Key Finding:** Models perform poorly on non-entailing pairs, suggesting they don't truly understand figurative language; they may rely on surface-level heuristics.

**Contamination:** Not mentioned in available sources; pre-2023 dataset carries lower contamination risk.

---

### 2. FigurativeQA / FigQA

**What it tests:** Two distinct (sometimes confused) benchmarks:
- **FigurativeQA:** Yes/no question answering over figurative vs literal contexts
- **Fig-QA:** Winograd-style pairing (correct interpretation of figurative phrases with divergent meanings)

**Comprehension vs Production:** COMPREHENSION ONLY.

**Size & Construction:**
- FigurativeQA: 400 yes/no QA pairs from product/restaurant reviews
- Fig-QA: 10,256 crowdsourced examples of metaphors and implications (Winograd-style)
- English only
- Extracted from real reviews and crowdsourced

**SOTA Scores & Models:**
- FigurativeQA with RoBERTa-base (BoolQ fine-tuned):
  - Amazon figurative: 83.43% ± 1.1
  - Amazon figurative (converted to literal): 93.5% ± 1.12
  - Yelp figurative: 66.84% ± 2.61
  - Yelp figurative (converted to literal): 90% ± 1.44
  - Clear performance drop on figurative contexts
- Fig-QA: models significantly below human performance, especially zero-shot ([ACL Anthology 2022.flp-1.23](https://aclanthology.org/2022.flp-1.23/))

**Key Finding:** Massive performance gap when contexts shift from literal to figurative (10-30% drop).

**Contamination:** Not explicitly discussed; mid-2022 publication suggests lower risk for older LLMs.

---

### 3. FLUTE (Figurative Language Understanding Through Textual Explanations)

**What it tests:** NLI with explanations for figurative language. Models must classify entailment AND generate natural language explanations.

**Comprehension vs Production:** COMPREHENSION WITH EXPLANATION GENERATION (hybrid; still interpretation-focused).

**Size & Construction:**
- 9,000 figurative NLI instances
- Spans 5 types: Sarcasm, Simile, Metaphor, Idiom, Paraphrase
- English only
- Human-AI collaborative annotation (GPT-3, crowd workers, expert annotators)

**SOTA Scores & Models:**
- T5 fine-tuned on FLUTE: baseline established; exact numbers referenced in paper but not fully extracted
- Gemma-2 (9B) fine-tuned on FLUTE: 72.8% acc@60 on explanation generation (2024)
- Open-source LLMs outperform GPT-4o on explanation coherence
- Zero-shot performance poor across all models; fine-tuning helps significantly

**Key Finding:** Explanation generation reveals weak understanding; templated, low-quality reasoning even with fine-tuning.

**Contamination:** Not discussed; dataset designed for explanation-based evaluation (less likely to appear verbatim in pretraining).

---

### 4. PIE Corpus (Potential Idiomatic Expression)

**What it tests:** TWO different corpora exist:
- **PIE-English:** Classification of idioms into 10 semantic categories (metaphor, simile, euphemism, irony, personification, hyperbole, etc.)
- **PIE-Parallel:** Paraphrase task (idiom vs literal paraphrase identification)

**Comprehension vs Production:** PIE-English is CLASSIFICATION (comprehension); PIE-Parallel is PARAPHRASE INTERPRETATION (comprehension).

**Size & Construction:**
- PIE-English: 20,100+ instances, ~1,200 idioms across 10 classes
- PIE-Parallel: 823 idioms, parallel corpus with literal paraphrases
- English only
- Mixed sourcing (web + annotation)

**SOTA Scores & Models:** Not clearly reported in search results.

**Contamination:** Not discussed; older dataset (2021-2022).

---

### 5. IDIOMEM

**What it tests:** Probing dataset for memorization behavior in transformer LMs. Does the model memorize or reason about idioms?

**Comprehension vs Production:** COMPREHENSION (predicting contextual idiom usage from prefix).

**Size & Construction:**
- English idioms
- Designed specifically to distinguish memorization from understanding
- Task: predict idiom completion given context

**SOTA Scores & Models:** Paper focuses on memorization analysis rather than SOTA rankings; exact scores not in accessible results.

**Contamination:** Specifically designed to study this; lower contamination risk by design.

---

### 6. EPIE (English Potential Idiomatic Expression Disambiguation)

**What it tests:** Sense disambiguation. Given an expression in context, classify whether it's used literally or idiomatically.

**Comprehension vs Production:** COMPREHENSION (classify sense, not generate).

**Size & Construction:**
- English focus
- Literal vs idiomatic sense labels
- Contextual sentences

**SOTA Scores & Models:** Details sparse in search results; appears to be a foundational disambiguation dataset.

**Contamination:** Not discussed.

---

### 7. iSarcasm

**What it tests:** Binary sarcasm detection. Is the tweet sarcastic?

**Comprehension vs Production:** COMPREHENSION (classify sarcasm).

**Size & Construction:**
- 777 sarcastic + 3,707 non-sarcastic tweets
- Twitter source
- Author-labeled (not crowdsourced inference)
- Tweets + non-sarcastic rephrases for context

**SOTA Scores & Models:**
- SOTA: RoBERTa + Mutation Data Augmentation (Papers with Code)
- iSarcasmEval shared task (2022) extended to English + Arabic
- Models categorize sarcasm subtypes: sarcasm, irony, satire, understatement, overstatement, rhetorical questions

**Contamination:** Not discussed; tweet data carries natural contamination risk (some tweets may appear in pretraining).

---

### 8. SemEval-2018 Task 3 (Irony Detection in Tweets)

**What it tests:** Irony detection (Task A: binary) and irony type classification (Task B: multi-class).

**Comprehension vs Production:** COMPREHENSION (classify irony).

**Size & Construction:**
- Training: 3,834 tweets
- Test: 784 tweets
- English only
- Collected via irony-related hashtags (#irony, #sarcasm, #not)
- Manually annotated to minimize noise

**SOTA Scores & Models:**
- Task A (binary): F1 = 0.71
- Task B (fine-grained): F1 = 0.51
- 43 teams submitted (Task A); 31 teams (Task B)
- Established benchmark for irony detection

**Contamination:** Not discussed; 2018 vintage, but tweets are public data (likely in some pretraining corpora).

---

### 9. SemEval-2022 Task 6 (Intended Sarcasm Detection in English & Arabic)

**What it tests:** Sarcasm detection across English and Arabic, with emphasis on intended/author-labeled sarcasm.

**Comprehension vs Production:** COMPREHENSION.

**Size & Construction:**
- Multilingual (English + Arabic)
- Author-labeled for intent
- Shared task format

**SOTA Scores & Models:** Specific scores not fully captured in search results; represents continuation of iSarcasm work.

**Contamination:** Not discussed.

---

### 10. PARSEME Shared Task (Multi-Word Expression Identification)

**What it tests:** Identification and classification of verbal MWEs (Verbal Multi-Word Expressions, subset of idioms/figurative language).

**Comprehension vs Production:** COMPREHENSION (identify + classify).

**Size & Construction:**
- 18-20 languages (high typological diversity)
- Annotated datasets per language
- Multiple editions (PARSEME 1.1, 2.0)
- Focus on verbal MWEs (like phrasal verbs, complex predicates)

**SOTA Scores & Models:**
- PARSEME 2.0: top systems achieve ~48.39% F1
- Diverse system architectures; neural tagging approaches dominant

**Contamination:** Not discussed; multilingual data reduces overlap risk with English pretraining.

---

### 11. DICE (Dataset for Idiomatic Contrastive Evaluation)

**What it tests:** Contextual idiom interpretation. Can models use context to disambiguate literal vs figurative readings?

**Comprehension vs Production:** COMPREHENSION (classify sense given context).

**Size & Construction:**
- Controlled contrastive dataset
- Idiomatic expressions in both literal and figurative contexts
- Measures influence of collocational frequency and sentence probability
- Published 2025 (ACL)

**SOTA Scores & Models:**
- GPT-4, Gemini, and other frontier models tested
- Key finding: **LLMs frequently fail when context is critical**
- Larger models sometimes worse (relying on memorization over reasoning)

**Key Finding:** This benchmark reveals a major gap: models don't leverage context reliably.

**Contamination:** New dataset (2025); minimal contamination risk by design.

---

### 12. MIDI (Multilingual Idioms in Dialogue)

**What it tests:** Idiom comprehension across language resource levels (high, medium, low) and contexts (sentence vs multi-turn dialogue).

**Comprehension vs Production:** COMPREHENSION.

**Size & Construction:**
- 18 typologically diverse languages/dialects
- Includes both literal and figurative usage in sentences and dialogues
- High/medium/low resource language coverage

**SOTA Scores & Models:**
- GPT-5.2, Gemini 2.5 Pro (proprietary)
- DeepSeek-R1-Distill-Llama, Gemma-3, Llama-3.1 (open-source)
- Activation steering on memorization/reasoning dimensions improves scores, especially for low-resource languages
- Significant gaps remain in low-resource settings

**Key Finding:** Multilingual; reveals persistent gaps in low-resource idiom understanding.

**Contamination:** Not discussed; multilingual diversity reduces risk.

---

### 13. Chengyu-Bench (Chinese Idiom Understanding)

**What it tests:** THREE tasks:
1. **Evaluative Connotation:** Classify idiom as positive or negative
2. **Appropriateness:** Detect incorrect usage in context (register, domain, situation mismatch)
3. **Open Cloze:** Fill blanks in passages without options

**Comprehension vs Production:** Task 1 is COMPREHENSION; Task 2 is COMPREHENSION (identify misuse); Task 3 is HYBRID (needs contextual reasoning).

**Size & Construction:**
- 2,937 human-verified examples
- 1,765 common Chinese idioms (Chengyu)
- Chinese language
- Diverse corpora

**SOTA Scores & Models:**
- Evaluative Connotation: ~95%+ accuracy (frontier LLMs)
- Appropriateness: ~85% accuracy (significant room for improvement)
- Open Cloze: ~40% top-1 accuracy (challenging)

**Key Finding:** Models excel at sentiment/connotation but struggle with contextual appropriateness. This is **the closest existing benchmark to your production-oriented goal**, though still primarily comprehension.

**Contamination:** Not discussed; Chinese-specific data lower contamination risk for English-trained models.

---

### 14. IdiomX (Multilingual Idiom Understanding, Retrieval, Interpretation)

**What it tests:** FOUR tasks:
1. Idiom detection
2. Context-to-idiom retrieval
3. Cross-lingual idiom alignment (Arabic-to-English)
4. Idiom interpretation (explain meaning)

**Comprehension vs Production:** COMPREHENSION + RETRIEVAL (closest to generation, but still interpretation-focused).

**Size & Construction:**
- 190K+ contextualized examples
- 12K+ idioms
- English, Arabic, French
- Multi-stage pipeline: lexical resources → normalization → LLM enrichment → validation

**SOTA Scores & Models:**
- Contextual transformers (BERT, multilingual models) improve detection substantially
- Hybrid retrieval + reranking (Sentence-BERT based) effective for retrieval
- Specific numerical SOTA not fully captured in accessible results

**Contamination:** Not discussed; synthetically augmented data reduces contamination risk.

---

### 15. G-IdiomAlign (Gloss-Pivoted Idiom Alignment)

**What it tests:** Cross-lingual idiom alignment and generation. Tasks:
1. Multiple-Choice Idiom Equivalence (identify meaning-equivalent idiom in another language)
2. Gloss-Contrastive Generation (generate idiom given meaning gloss)

**Comprehension vs Production:** Task 1 is COMPREHENSION; Task 2 is PRODUCTION (generate idiom from meaning).

**Size & Construction:**
- 9 core languages (with representation from underrepresented families)
- Each idiom linked to English gloss (Wiktionary)
- Two evaluation settings: multiple-choice + open generation

**SOTA Scores & Models:**
- Exact scores not fully captured
- Key finding: Models show **pervasive bias to literal translations**
- Adding glosses yields limited improvements
- Difficulty in producing canonical, meaning-equivalent idioms in unconstrained space

**Key Finding:** This is the closest existing benchmark to PRODUCTION; still incomplete (multiple-choice vs truly open generation).

**Contamination:** Not discussed; glosses reduce verbatim overlap risk.

---

### 16. VIVID (Vietnamese Idioms for Validation and Interpretation Depth)

**What it tests:** Idiom and proverb understanding in Vietnamese (low-resource language).

**Comprehension vs Production:** COMPREHENSION.

**Size & Construction:**
- 1,636 Vietnamese idioms/proverbs
- Dual-layer annotations
- Vietnamese language
- Addresses gap in low-resource figurative language evaluation

**SOTA Scores & Models:** Not fully detailed in search results.

**Contamination:** Not discussed; low-resource language data minimal pretraining overlap.

---

### 17. FLUID QA (Multilingual Figurative Language Usage in Dialogue)

**What it tests:** Figurative language usage across dialogue contexts. Covers simile, metaphor, idiom, sarcasm across languages and dialogue turns.

**Comprehension vs Production:** COMPREHENSION (identify/classify figurative usage in dialogue).

**Size & Construction:**
- Multilingual: English, Chinese, Korean
- Dialogue format (multi-turn)
- Categories: simile, metaphor, idiom, sarcasm

**SOTA Scores & Models:** Not fully detailed; published 2025 (ACL/EMNLP).

**Key Finding:** Highlights that figurative difficulty varies by language and figurative type; dialogue context important.

**Contamination:** Not discussed; new dataset (2025).

---

## Synthesis: Measurement Gap

### What Existing Benchmarks Measure Well
- **Comprehension:** Detecting whether a phrase is figurative, interpreting its meaning (90% of benchmarks)
- **Classification:** Categorizing idioms by type, sentiment, level of figurativity
- **Disambiguation:** Literal vs figurative sense selection (with context)
- **Retrieval:** Finding equivalent idioms across languages

### The Critical Gap: PRODUCTION / APPROPRIATE DEPLOYMENT

**None of the 15+ benchmarks comprehensively measure:**

1. **Contextually Appropriate Idiom Deployment** — Can a model use "Bob's your uncle" or "hit the hay" in a naturally appropriate spot, with correct register, audience, and situational fit?

2. **Detection of Inappropriate Usage** — Can a model flag when someone misuses an idiom (register mismatch, wrong dialect, wrong domain)? Chengyu-Bench Task 2 (Appropriateness) is the closest, but limited to Chinese.

3. **Multi-dimensional Pragmatics** — Does the model understand:
   - Regional variation (British "Bob's your uncle" vs American equivalents)?
   - Register mismatch (formal vs casual)?
   - Domain violations (business idiom in poetry)?
   - Temporal/cultural shift (obsolete idioms)?
   - Audience understanding (does listener know this idiom)?

4. **Generation Under Constraints** — Can a model generate an idiom that fits a specific meaning + context + register + audience? G-IdiomAlign Task 2 touches this but doesn't fully measure appropriateness.

5. **Hallucination Prevention** — When prompted to use an idiom, does the model invent false idioms or appropriately decline? FFE-Hallu (Persian) addresses this for hallucination detection but only for comprehension.

### Why This Gap Matters for Your Probe

Existing benchmarks measure **what a model understands**. Your probe should measure **what a model can do**. The frontier difference: a model might correctly classify "cry over spilled milk" as an idiom but fail to deploy it naturally, or deploy it inappropriately (e.g., using it in a formal legal brief).

---

## Contamination & Pretraining Data Risk

### General Findings
- Broader LLM contamination research ([Detecting Pretraining Data from Large Language Models](https://arxiv.org/pdf/2310.16789)) shows 10-20% of typical benchmarks may overlap with pretraining
- Figurative language benchmarks published before 2023 have lower contamination risk for models trained after 2023
- Multilingual datasets (MIDI, IdiomX, VIVID) have lower English-LLM contamination risk
- Synthetically augmented datasets (IdiomX) reduce verbatim overlap but risk systematic biases

### Specific Contamination Concerns by Benchmark
- **iSarcasm, SemEval Task 3:** Tweet-source data likely in pretraining (Twitter/internet scrapes)
- **FLUTE, FigQA:** Curated data, lower risk; but GPT-3-augmented (potential upstream bias)
- **PIE, IDIOMEM:** Academic datasets, minimal contamination risk
- **Chengyu-Bench, VIVID:** Language-specific; low contamination for English-primary models

---

## Design Recommendations for Your Own Probe

### 1. Focus on Production-Oriented Tasks (Major Gap)

Existing benchmarks skip this entirely. Design tasks that measure:
- **Idiom insertion:** Given a narrative context, choose appropriate spot and form to insert an idiom
- **Appropriateness judgment:** Flag inappropriate usage (register, region, domain, audience mismatch)
- **Contextual constraint satisfaction:** Can the model generate/select an idiom that meets multiple constraints (meaning + register + audience)?

### 2. Incorporate Multi-Dimensional Pragmatics

Don't just test "does the model know this idiom?" Instead test:
- **Register variation:** Formal, casual, colloquial idioms in matching contexts
- **Regional variation:** British, American, Australian, Indian English idioms (if multilingual)
- **Temporal decay:** Obsolete vs modern idioms; can the model avoid outdated usage?
- **Audience modeling:** Does the model adapt idiom choice to audience knowledge (child, ESL learner, domain expert)?

### 3. Use Controlled Contrastive Design (Follow DICE Model)

Design idiom pairs where:
- **Target:** Appropriate usage in context
- **Literal control:** Same sentence with literal phrase instead
- **Register violation:** Same idiom, register-inappropriate context
- **Regional violation:** Same meaning, different regional idiom (wrong one chosen)
- **Hallucination trap:** Prompt that might elicit false idiom; measure refusal vs invention

### 4. Measure Both Binary Judgment and Open Generation

- **Comprehension layer:** Can the model select/identify appropriate idiom from choices?
- **Production layer:** Can the model explain or generate appropriate usage without scaffolding?
- **Pragmatic layer:** Can the model explain WHY a given usage is appropriate/inappropriate (register, audience, domain)?

### Example Task Structure:
```
Context: [Brief narrative]
Task A: Is this idiom use appropriate here? Yes/No
Task B: Why or why not? [Open explanation]
Task C: Rewrite the sentence with appropriate idiom use (if current is inappropriate)
Task D: Would [specific audience type] understand this idiom? Yes/No
```

---

## Sources

1. [IMPLI: Investigating NLI Models' Performance on Figurative Language](https://aclanthology.org/2022.acl-long.369/) — ACL 2022
2. [FigurativeQA: A Test Benchmark for Figurativeness Comprehension for Question Answering](https://aclanthology.org/2022.flp-1.23/) — ACL Workshop 2022
3. [FLUTE: Figurative Language Understanding through Textual Explanations](https://aclanthology.org/2022.emnlp-main.481/) — EMNLP 2022
4. [PIE Corpus](https://aclanthology.org/2021.mwe-1.5/) — ACL MWE Workshop 2021
5. [PARSEME Shared Task](https://aclanthology.org/volumes/2026.mwe-1/) — Multiple years
6. [Rolling the DICE on Idiomaticity: How LLMs Fail to Grasp Context](https://aclanthology.org/2025.acl-long.362/) — ACL 2025
7. [Multilingual Idioms in Sentences and Conversations (MIDI)](https://aclanthology.org/2026.acl-long.564/) — ACL 2026
8. [Chengyu-Bench: Benchmarking Large Language Models for Chinese Idiom Understanding and Use](https://aclanthology.org/2025.emnlp-main.119/) — EMNLP 2025
9. [IdiomX: A Multilingual Benchmark for Idiom Understanding, Retrieval, and Interpretation](https://arxiv.org/abs/2606.02584) — arXiv 2606.02584 (April 2026)
10. [G-IdiomAlign: A Gloss-Pivoted Benchmark for Cross-Lingual Idiom Alignment](https://arxiv.org/pdf/2606.18989) — arXiv 2606.18989 (June 2026)
11. [VIVID: A Culturally Grounded Benchmark Exposing the Figurative Language Gap in Vietnamese NLP](https://arxiv.org/html/2608.03095) — arXiv 2608.03095 (August 2026)
12. [FLUID QA: A Multilingual Benchmark for Figurative Language](https://aclanthology.org/2025.emnlp-main.1540.pdf) — EMNLP 2025
13. [SemEval-2018 Task 3: Irony Detection in English Tweets](https://aclanthology.org/S18-1005/) — SemEval 2018
14. [iSarcasm: A Dataset of Intended Sarcasm](https://researchgate.net/publication/343300501_iSarcasm_A_Dataset_of_Intended_Sarcasm) — ACL 2020
15. [Detecting Pretraining Data from Large Language Models](https://arxiv.org/pdf/2310.16789) — Contamination risk analysis
16. [FFE-Hallu: Hallucinations in Fixed Figurative Expressions](https://arxiv.org/pdf/2601.20105) — arXiv 2601.20105 (Persian idiom hallucinations)
17. [SarcasmBench: Towards Evaluating Large Language Models on Sarcasm Understanding](https://www.computer.org/csdl/journal/ta/2025/04/11146812/29GBxQiBx9m) — IEEE 2025

