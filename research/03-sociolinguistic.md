# Sociolinguistic Failure Modes of LLMs: Dialect, Register, and Idiom

**Date:** 2026-08-09  
**Status:** Research complete  
**Scope:** Dialect performance disparities, register control, slang/idiom coverage, code-switching, temporal drift, sarcasm/irony detection

---

## I. Measured Dialect Performance Disparities

### 1.1 African American English (AAVE) vs. Standard American English (SAE)

**Hofmann et al., Nature 2024** [Dialect prejudice predicts AI decisions](https://arxiv.org/abs/2403.00742)
- Conviction rate bias: AAVE **68.7%** vs. SAE **62.1%** (6.6 percentage point gap)
- Death sentence bias: AAVE **27.7%** vs. SAE **22.8%** (4.9 percentage point gap)
- Job assignment: speakers of AAVE assigned to less prestigious roles
- Character stereotypes: LLMs associate AAVE with "lazy," "ignorant," "stupid," "dirty" more than any recorded human stereotype
- **Critical finding:** Alignment pipelines (RLHF) exacerbate gap by suppressing overt stereotypes while embedding covert dialect bias deeper

**Blodgett et al. (2016, 2020)** [Racial Disparity in NLP](https://www.semanticscholar.org/paper/Racial-Disparity-in-Natural-Language-Processing%3A-A-Blodgett-Gillis/1d88ffe11b0c1db2be11e0032f8e13f5c5b44a20)
- Perplexity on AA-aligned Twitter corpus: **higher for all model sizes**
- Scaling finding: **Gap does NOT close as models scale.** Both dialects improve with size, but at same rate, maintaining constant offset

**Reward Model Bias (2025)** [Rejected Dialects](https://arxiv.org/pdf/2502.12858)
- Reward models predict preferences with **-4% accuracy drop** for African American Language (AAL) vs. White Mainstream English (WME)
- Models steer conversations away from AAL even when prompted with AAL
- Subjectivity in preference data introduces new dialect biases at alignment stage

### 1.2 Broader English Dialects (Cross-Dialect Benchmarks)

**EnDive Benchmark (2025)** [Cross-Dialect Fairness](https://arxiv.org/abs/2504.07100)
- Tests: GPT-4o, Claude 3.5 Sonnet, DeepSeek-v3, LLaMa-3-8B on 12 reasoning benchmarks
- **Accuracy disparities (example WSC task):**
  - SAE: 91.75% → AAVE: 88.33% (3.4 point drop)
  - SAE: 88.47% → Jamaican English: 53.19% (**35.3 point collapse**)
- Pattern: Frontier models show larger absolute accuracy gaps on lower-resource dialect variants

**MDial: 9-Dialect Conversational Benchmark (2026)** [Dialect-Accurate Dialogues](https://arxiv.org/html/2601.22888v1)
- 3,680+ parallel dialogs across: American (SAE), Australian, British, Canadian, Indian, Irish, Nigerian, Philippine, Scottish
- **Frontier model dialect identification accuracy: <70%** (target 100%)
- Canadian English identification: **<50%** for most models
- Systematic misclassification: non-SAE dialects reassigned as American or British (American bias in training data)

### 1.3 British vs. American English Asymmetry

**"Which English Do LLMs Prefer?" (2025)** [Postcolonial Analysis](https://arxiv.org/abs/2604.04204)
- Audit of 1,813 American-British lexical variants
- **British forms incur higher tokenization cost** (more tokens per word) → computational disadvantage
- Pretraining corpora: **systematic skew toward American English**
- Generation bias: LLMs consistently prefer American variants even when context is British
- Result: Reinforces "American English = standard" epistemically

---

## II. Register and Formality Control (Partially Measured)

### 2.1 The "Register Gap"

**"A Universal Vibe?" (2026)** [SAE Feature Analysis](https://arxiv.org/pdf/2603.26236)
- LLMs exhibit pervasive **"register gap"**: trained on highly edited, formal text; fail to process dynamic, informal language
- Modern alignment pipelines overwhelmingly favor standard, edited text
- Result: Models systematically over-formalize when responding to informal/slang input
- No quantified asymmetry (e.g., British idioms formalized more than American) **yet measured**

### 2.2 Formality Transfer

**Register Analysis for Style Transfer (2026)** [Steering LLMs](https://arxiv.org/html/2505.00679)
- Prompting method based on register analysis improves style transfer strength
- Tested on Arabic dialect→MSA transformation (formality dimension)
- **UNVERIFIED:** Whether English dialect formality transfer (AAVE→formal AAVE) works equally as well

### 2.3 Multi-Style Control

- Limited research on simultaneous control of humor + formality + register in LLMs
- Conjecture: register + dialect interaction not measured (does informal register output better in dialect? worse?)

---

## III. Lexical Overuse and "Try-Hard" Slang

### 3.1 Measured Overuse of Formal/Connective Words

**"Why Does ChatGPT Delve So Much?" (2024)** [Lexical Overrepresentation](https://arxiv.org/pdf/2412.11385)
- 21 focal words identified as overused by ChatGPT-3.5 (e.g., "delve," "explore," "unlock")
- Connective/transitional phrases: **6x more frequent than human writing**
- Cause: Learning from Human Feedback (RLHF) favors certain words as proxy for quality
- Result: Generated text is "easily recognized" by editors; heavy reliance on templates ("It's not just X, it's Y...")

### 3.2 Uncanny Register / "Try-Hard" Slang

**UNVERIFIED - Documented Anecdotally but Not Formally Measured:**
- User reports: LLMs produce "try-hard" slang (forced, outdated, or over-used)
- Examples: inserting Gen-Z slang in formal contexts, using slang terms incorrectly/archaically
- No published benchmark quantifies frequency of inappropriate slang insertion or slang fluency errors
- **Gap:** No paper systematically measures whether LLMs generate recognizable vs. uncanny slang in blind evaluations

---

## IV. Novel Slang and Temporal Drift (Partially Measured)

### 4.1 SLANG Benchmark: Post-Training-Cutoff Slang

**"SLANG: New Concept Comprehension" (2024)** [ACL 2024](https://aclanthology.org/2024.emnlp-main.698/)
- Methodology: Select slang from Urban Dictionary post-dating model knowledge cutoff
- Examples: Select terms added after Jan 2022 for GPT-4 (April 2021 cutoff)
- **Finding:** Models can update terms WITHIN cutoff, but struggle to generalize to post-cutoff terms
- **Interpretation mechanism UNKNOWN:** How do models infer meaning of novel slang? (context? decomposition? failure?)

### 4.2 NewTerm Benchmark (2024)

**Real-Time New Terms Annual Updates** [NewTerm](https://arxiv.org/pdf/2410.20814)
- Models struggle with annually updated vocabulary
- Post-training cutoff comprehension remains open question

---

## V. Sarcasm and Irony Detection (Well-Measured, Poor Performance)

### 5.1 SarcasmBench (2025)

**Multi-Model Sarcasm Evaluation** [IEEE Transactions](https://www.computer.org/csdl/journal/ta/2025/04/11146812/29GBxQiBx9m)
- Compared 11 LLMs + 8 pre-trained models across 6 datasets
- **GPT-4 outperforms others, but still subject to critical failure:**
  - Few-shot IO prompting: best strategy
  - Chain-of-thought: **hurts performance** (sarcasm is holistic, not step-wise)
  - **Catastrophic generalization gap:** near-perfect on synthetic data, random guessing on organic human speech

### 5.2 CAF-I: Collaborative Agent Framework for Irony (2026)

**State-of-the-art Multi-Agent Approach** [GitHub](https://arxiv.org/abs/2506.08430)
- Macro-F1: **76.31** (4.98 point improvement over prior baseline)
- Still requires explicit multi-agent reasoning; single-pass detection fails

### 5.3 Pragmatic Metacognitive Prompting (2024)

**Context-Aware Retrieval** [EMNLP 2024](https://arxiv.org/pdf/2412.04509)
- Retrieval-augmented prompting improves sarcasm detection by **9.87% macro-F1**
- Requires external context retrieval; in-context performance lower

---

## VI. Code-Switching Performance (Multilingual)

### 6.1 LinCE Benchmark and Code-Switching LLMs

**LLM Code-Switching Challenges (2025)**
- Multilingual pre-trained models (XLM-R) struggle with simultaneous multi-language processing
- Token-level code-switching: models perform better when code-switching incorporated in training
- Sentence-level code-switching: significantly enhances cross-lingual transfer
- **Finding:** Open-source LLMs inadequately handle code-switching requiring simultaneous processing

### 6.2 Code-Switching Reveals Language Anchoring (2026)

**Language Anchoring in Multilingual LLMs** [arXiv](https://arxiv.org/pdf/2606.19668)
- Models exhibit "language anchoring" bias in code-switched contexts
- Prefer one language over another even when semantic equivalence holds

---

## VII. Unmeasured Gaps (Research Opportunities)

### 7.1 Regional Idiom Asymmetry

**NOT MEASURED:** Comparative performance on:
- British idioms ("Bob's your uncle," "chuffed," "taking the mickey") vs. American equivalents
- Regional idiom density: Can LLMs distinguish between idiomatic and literal language in dialect X but not Y?
- **Hypothesis (unverified):** Models handle American idioms better due to training corpus skew
- **Probe design:** Minimal pairs (literal vs. idiomatic in paired dialects)

### 7.2 Dialect-Register Interaction

**NOT MEASURED:** Can models match register WITHIN a non-standard dialect?
- E.g., formal AAVE, casual British English, professional Indian English
- Current benchmarks test dialect OR register, not interaction
- **Hypothesis (unverified):** Register control fails in low-resource dialects (prioritizes getting dialect right)

### 7.3 Slang Fluency vs. Appropriateness

**NOT MEASURED:** Blind evaluation of:
- Whether LLM-generated slang is recognized as natural or "try-hard"
- Temporal alignment: Does LLM use current slang or lag 2-3 years?
- Demographic appropriateness: Can models modulate slang age/style by context?

### 7.4 Quantified Over-Formalization in Dialects

**NOT MEASURED:** 
- Does over-formalization happen differentially across dialects?
- Is African American English formalized more aggressively than British English?
- Explicit numerical gap: formal-register bias coefficient by dialect

### 7.5 Indian English, Nigerian English, Australian English Specific Benchmarks

**UNDER-MEASURED:**
- MDial produces conversational data but doesn't isolate core linguistic competence
- Reasoning benchmarks (MMLU, GSM8K) not yet systematically translated/evaluated across these dialects
- **Gap:** No published cross-dialect reasoning benchmark excluding AAVE (which dominates fairness research)

### 7.6 Sarcasm/Irony Generalization Mechanism

**NOT UNDERSTOOD:**
- Why do models fail on organic speech after near-perfect synthetic performance?
- Is it contextual length? Cue density? Pragmatic reasoning?
- **No mechanistic study** of what causes sarcasm detection collapse

---

## VIII. Probe Design Recommendations

### For Idiom-Probe Project

**Tier 1: High-Signal, Well-Motivated Contrasts**

1. **AAVE vs. SAE Minimal Pairs (Criminal Sentencing Context)**
   - Leverage Hofmann et al. existing data; add benign contexts
   - Measure: Does model probability of conviction drop when input rephrased in SAE?
   - Expected signal: 6-7 point accuracy swing (from Nature findings)

2. **British Idioms in Dialect-Neutral vs. Dialect-Marked Contexts**
   - Idiom: "Bob's your uncle"
   - Variant A: Neutral context (no dialect marker)
   - Variant B: British dialect marked (e.g., "Right, Bob's your uncle then, innit")
   - Measure: Comprehension accuracy (does model explain meaning?)
   - Hypothesis: Variant B shows lower accuracy (dialectal overhead)

3. **Register Mismatch: Formal Prompt + Informal Dialect Input**
   - Prompt: "Write a professional email" (formal register request)
   - Input A: Standard English context
   - Input B: AAVE context (identical semantic content)
   - Measure: Over-formalization rate (does model output artificially formal English in response to AAVE?)
   - Expected: Yes, and measurable

4. **Novel Slang Comprehension (Forced Inference)**
   - Use slang term post-dating model cutoff (e.g., "cap" as of 2022, if model cutoff < 2022)
   - Context-only inference task (no definition provided)
   - Measure: Can model infer meaning from usage? Success rate.
   - Compare against human inference from same context

5. **Sarcasm + Dialect Interaction**
   - Sarcastic utterance in SAE: "Oh, great, another meeting"
   - Equivalent in AAVE: "Oh, that's straight up fire, another meeting"
   - Measure: Sarcasm detection accuracy drop (if any) when combined with non-SAE dialect
   - Expected: compound penalty

**Tier 2: Exploration Probes (Unvalidated Hypotheses)**

- Over-use of connectives in dialectal contexts (count "delve," "explore" rates)
- MDial dialect identification accuracy on frontier models (should replicate <70%)
- Formality coefficient by dialect (measure formal-word density in model responses)

---

## IX. Sources and Methodology

### Authoritative Sources

- **Hofmann et al. (2024):** Nature 633(8028):147–54. Dialect prejudice predicts AI decisions about character, employability, criminality. [Nature](https://ora.ox.ac.uk/objects/uuid:4e0fe173-52f2-433d-8042-0ff941919401)
- **Blodgett et al. (2016, 2020):** Racial disparity in NLP; perplexity gaps in African American English. [ACL](https://www.researchgate.net/publication/318129802_Racial_Disparity_in_Natural_Language_Processing%3A_A_Case_Study_of_Social_Media_African-American_English)
- **Ziems et al. (2023):** Multi-VALUE cross-dialectal English benchmark. [ACL Anthology](https://aclanthology.org/2023.acl-long.44/)
- **EnDive (2025):** Cross-dialect benchmark for fairness. [EMNLP](https://arxiv.org/abs/2504.07100)
- **MDial (2026):** 9-dialect conversational benchmark. [ACL 2026](https://arxiv.org/html/2601.22888v1)
- **Reward Model Bias (2025):** Rejected Dialects. [NAACL](https://aclanthology.org/2025.findings-naacl.417/)
- **SarcasmBench (2025):** Sarcasm detection evaluation. [IEEE TA](https://www.computer.org/csdl/journal/ta/2025/04/11146812/29GBxQiBx9m)
- **SLANG Benchmark (2024):** New concept comprehension. [EMNLP](https://aclanthology.org/2024.emnlp-main.698/)

### Data Quality Notes

- **Verified with URLs:** All main claims cross-referenced against paper abstracts or search results
- **Quantitative claims:** Extracted from published results sections
- **Unverified claims:** Marked explicitly (e.g., "UNVERIFIED" on anecdotal "try-hard" slang production)
- **Gaps identified:** Explicitly marked as "NOT MEASURED" or "UNDER-MEASURED"

---

## X. Conclusion

**Measured disparities are substantial and persistent:**
- AAVE conviction bias: 6.6 percentage points
- Extreme dialect drops: Jamaican English −35.3 points on reasoning
- Reward model alignment introduces new biases (−4% accuracy)
- British English disadvantaged in tokenization and generation preference
- Scaling does not close gaps

**Critical gaps remain:**
- No systematic idiom coverage asymmetry studies
- Register-dialect interaction unmeasured
- Slang fluency not formally benchmarked
- Temporal drift mechanisms unknown
- Non-AAVE non-SAE dialect benchmarks sparse

**The research reveals a two-layer problem:** (1) explicit performance disparities measurable and quantifiable, (2) implicit register gaps and register-dialect interactions not yet captured by benchmarks. The idiom-probe should prioritize AAVE-SAE contrasts (highest signal) and British idiom contexts (tests dialect-idiomatic interaction).

