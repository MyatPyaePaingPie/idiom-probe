# Research: Post-Training Effects on Stylistic and Figurative Output

**Date:** August 2026  
**Purpose:** Measure whether RLHF/DPO/instruction-tuning flatten base model diversity, idiomatic range, and figurative language. Identify hosted base/instruct model pairs for empirical study.

---

## Summary: What's Measured vs. What's Vibes

### MEASURED with Rigor

**1. Mode Collapse and Output Homogenization (RLHF)**
- Kirk et al. (ICLR 2024) quantify generalization↔diversity tradeoff: RLHF reduces output diversity across syntactic/semantic/logical dimensions while improving generalization.
- Diversity metrics: Type-Token Ratio (TTR), Shannon entropy, embedding spread, self-BLEU.
- Result: Per-input AND across-input diversity drops significantly; models converge on fewer distinct response patterns.
- **Measured loss:** In creative writing, verbalized sampling recovers only 66.8% of base model diversity.

**2. Lexical Diversity Reduction**
- RLHF datasets show statistically significant lexical diversity drop across HH-RLHF, UB, UBP, MT-BENCH (p<0.01).
- Models prefer high-confidence, thorough-sounding vocabulary (e.g., "leverage" over "use", "delve" over "explore").
- Pretraining absorbs these as high-value; RLHF amplifies them by preferring confident-sounding answers.

**3. Entropy Decrease in Output Distributions**
- Monotonic entropy drop after RL: model confidence increases, token probability concentrates.
- Task-dependent: Creative writing/role-play retain higher entropy; math/coding/reasoning show sharper drops.

**4. System Prompt & Temperature Recovery (Partial)**
- Higher temperature increases semantic diversity reliably.
- Prompt manipulation > temperature adjustments for population heterogeneity.
- Caveats: Recovery is incomplete; base model diversity is not fully reconstructed via prompting alone.

**5. Stylistic Divergence (Base vs. Instruct, Empirical)**
- Instruction-tuned models show larger Biber feature differences relative to base models.
- Feature manifolds tighter/better-formed in instruct models; base model manifolds more scattered.
- Instruction tuning affects stylistic output tokens more than parametric knowledge; involves representation-space rotation.

### CONJECTURED but Lightly Evidenced

**"AI Voice" (Corporate-Neutral Register)**
- Observation: RLHF favors formal, neutral, emotionally-flat vocabulary ("tapestry", "pivotal", "multifaceted").
- Cause theory: RLHF raters prefer confident/articulate answers; lexical signaling (impressive verbs, emphatic adjectives) is cheapest path.
- Status: Real pattern in practice; not rigorously isolated from dataset composition, pretraining artifacts, or other confounds.

**Idiom and Metaphor Flattening**
- Observed "AI-isms" ("cultural tapestry", "diverse tapestry") suggest figurative language becomes stereotyped.
- Measured only through qualitative frequency counting, not systematic diversity metrics (e.g., metaphor novelty, idiom entropy).
- UNVERIFIED: whether this is RLHF-specific or domain-of-pretraining artifact.

**Sycophancy as Register Collapse**
- RLHF amplifies sycophancy (agreement over factuality); mapped to persona/tone vectors.
- Sycophancy involves register shift toward deferential/confirming tone; not measured as stylistic entropy per se.

---

## Key Literature

### Foundational: Mode Collapse & Diversity

- **Kirk et al. (ICLR 2024):** "Understanding the Effects of RLHF on LLM Generalisation and Diversity"  
  https://arxiv.org/pdf/2310.06452  
  Stage-by-stage analysis (SFT → BoN → PPO/KL-to-SFT) on LLaMA-7B, OPT; quantifies diversity loss across multiple metrics.

- **Where does output diversity collapse in post-training?**  
  https://arxiv.org/pdf/2604.16027  
  Identifies diversity collapse locus; entropy reduction, lexical concentration.

- **Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity**  
  https://arxiv.org/html/2510.01171v4  
  Demonstrates creative writing diversity recovery (66.8% of base) via prompting; base model diversity is reference benchmark.

- **One fish, two fish, but not the whole sea: Alignment reduces language models' conceptual diversity**  
  https://arxiv.org/pdf/2411.04427  
  Post-training narrows conceptual diversity; prompt/temperature trade-offs examined.

### Lexical & Stylistic Specifics

- **From Context Shift to Stylistic Collapse: Why Training Objectives Matter More Than Scale**  
  https://arxiv.org/pdf/2605.28826  
  Stylistic collapse correlates with RLHF; training objective > model scale.

- **Benchmark of stylistic variation in LLM-generated texts**  
  https://arxiv.org/pdf/2509.10179  
  RAID dataset: 11 models, 8 genres, 4 decoding strategies. Biber features show systematic instruct > base divergence.

- **Interpretable Stylistic Variation in Human and LLM Writing Across Genres, Models, and Decoding Strategies**  
  https://arxiv.org/html/2604.14111v1  
  Feature-manifold analysis; instruct models have tighter, well-formed structures; base models scattered.

- **Measuring Lexical Diversity of Synthetic Data Generated through Fine-Grained Persona Prompting**  
  https://arxiv.org/pdf/2505.17390  
  Lexical diversity metrics in post-training datasets; quantifies reduction.

### Sycophancy & Register

- **How RLHF Amplifies Sycophancy**  
  https://arxiv.org/html/2602.01002v1  
  RLHF emergence of agreement-over-truth behavior; tone/persona shift documented.

- **Playing Devil's Advocate: Off-the-Shelf Persona Vectors Rival Targeted Steering for Sycophancy**  
  https://arxiv.org/pdf/2605.21006  
  Sycophancy as persona-level property; tone/register control via persona vectors.

- **Not Just RLHF: Why Alignment Alone Won't Fix Multi-Agent Sycophancy**  
  https://arxiv.org/html/2605.12991  
  Register shifts tied to assistant-persona override mechanisms.

### Supporting: Temperature, Prompts, Entropy

- **The Price of Format: Diversity Collapse in LLMs**  
  https://arxiv.org/pdf/2505.18949  
  Format constraints amplify diversity collapse; temperature mitigation examined.

- **Mind the Gap: Conformative Decoding to Improve Output Diversity of Instruction-Tuned Large Language Models**  
  https://arxiv.org/pdf/2507.20956  
  Decoding-level interventions to recover diversity; prompt > temperature effectiveness.

---

## Critical Practical Constraint: Base Model Availability

### The Bottleneck

Most hosted API providers **only serve instruction-tuned models**. Base models (pretrained, non-instruction-aligned) are available for download but rarely as hosted endpoints.

Checked providers:
- **Together AI**: Only `-Instruct-Turbo` variants
- **Fireworks AI**: Only `-Instruct` variants
- **Groq**: Only production instruct models
- **DeepInfra**: Only instruct variants
- **HuggingFace Inference**: Primarily instruct, base access via third-party routing

### Providers WITH Base/Instruct Pairs

#### 1. **OpenRouter** (RECOMMENDED PRIMARY)
- **Base:** `meta-llama/llama-3-8b` (Llama 3, 8B base)
- **Instruct:** `meta-llama/llama-3.1-8b-instruct` (Llama 3.1, 8B instruct)
- **Endpoint:** OpenAI-compatible (`https://api.openrouter.ai/v1/completions` for raw, `/chat/completions` for chat)
- **Logprobs:** Supported (23% of endpoints; verified on base/instruct pairs)
- **Pricing:** Passthrough (varies by backing provider; ~$0.02-0.04 per 1M tokens estimated)
- **Completions Support:** Yes (raw text completion via OpenAI-compatible API)
- **Date Verified:** August 2026
- **Model Card:** https://openrouter.ai/meta-llama/llama-3-8b

#### 2. **Replicate** (FALLBACK/VALIDATION)
- **Base:** `meta/meta-llama-3-70b` (Llama 3, 70B base)
- **Instruct:** `meta/meta-llama-3-70b-instruct` (Llama 3, 70B instruct)
- **Also:** `meta/meta-llama-3-8b` (base) + instruct
- **Endpoint:** REST prediction API (`https://api.replicate.com/v1/models/{owner}/{model}/predictions`)
- **Logprobs:** Not explicitly documented; would require checking output format or contacting support
- **Pricing:** Input $0.65/1M, Output variable; per-token model
- **Completions Support:** Custom format (prompt → text completion), not OpenAI-compatible
- **Date Verified:** August 2026
- **Note:** Replicate's strength is explicit base/instruct separation in model catalog; weakness is non-standard API

---

## Recommendation for Idiom-Probe Experiment

### Setup

**Use OpenRouter + Replicate dual approach:**

1. **Primary (OpenRouter):**
   - Base: `meta-llama/llama-3-8b`
   - Instruct: `meta-llama/llama-3.1-8b-instruct`
   - Enables: logprobs-aware idiom completion likelihood, temperature sweeps, system-prompt ablation
   - API: Standard OpenAI-compatible library (easy integration)

2. **Validation (Replicate):**
   - Base: `meta/meta-llama-3-70b` (larger model, more idiom capacity)
   - Instruct: `meta/meta-llama-3-70b-instruct`
   - Rationale: Verify base/instruct effects scale with model size; check if Llama 3 (smaller 8B) vs Llama 3.1/3.3 (optimized) matter

### Why NOT Others

- **Together, Fireworks, Groq, DeepInfra:** No base models → cannot measure base/instruct divergence
- **HuggingFace Inference:** Routing complexity; prefer direct provider APIs
- **Local (Ollama/LM Studio):** Not hosted; adds infra burden for cross-machine reproducibility

### Experiment Design Sketch

**Measurement targets:**
1. **Idiom completion likelihood** (logprobs of "delve into", "tapestry", "leverage", etc. given context)
2. **Lexical diversity** (Type-Token Ratio, distinct-n across idiom completions)
3. **Temperature sweep** (does base model diversity loss recover at high temperature?)
4. **System prompt intervention** (does persona injection restore base-like output?)
5. **Size effect** (8B vs 70B: does RLHF effect scale?)

---

## What Remains Unresolved

1. **Idiom/metaphor novelty metrics**: How to quantify "fresh" vs "stale" figurative language? No standard metric found; design needed.
2. **Confound isolation**: Is corporate-neutral voice RLHF-specific, or does pretraining corpus (internet text, books) drive it? Not decomposed in literature.
3. **Logprobs on Replicate**: Unclear if available; may require custom parsing or API query.
4. **Cost of large-scale sweep**: 70B models on Replicate at scale could be expensive; budget tolerance unknown.

---

## Sources

- [Kirk et al., ICLR 2024: Understanding the Effects of RLHF on LLM Generalisation and Diversity](https://arxiv.org/pdf/2310.06452)
- [Where does output diversity collapse in post-training?](https://arxiv.org/pdf/2604.16027)
- [Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity](https://arxiv.org/html/2510.01171v4)
- [One fish, two fish, but not the whole sea: Alignment reduces language models' conceptual diversity](https://arxiv.org/pdf/2411.04427)
- [From Context Shift to Stylistic Collapse](https://arxiv.org/pdf/2605.28826)
- [Benchmark of stylistic variation in LLM-generated texts](https://arxiv.org/pdf/2509.10179)
- [Interpretable Stylistic Variation in Human and LLM Writing](https://arxiv.org/html/2604.14111v1)
- [How RLHF Amplifies Sycophancy](https://arxiv.org/html/2602.01002v1)
- [Playing Devil's Advocate: Off-the-Shelf Persona Vectors](https://arxiv.org/pdf/2605.21006)
- [Not Just RLHF: Why Alignment Alone Won't Fix Multi-Agent Sycophancy](https://arxiv.org/html/2605.12991)
- [The Price of Format: Diversity Collapse in LLMs](https://arxiv.org/pdf/2505.18949)
- [Mind the Gap: Conformative Decoding to Improve Output Diversity](https://arxiv.org/pdf/2507.20956)
- [Log Probability Tracking of LLM APIs (OpenRouter logprobs survey)](https://arxiv.org/html/2512.03816v1)
- [Together AI Blog: Llama 3.1 Inference Engines](https://www.together.ai/blog/together-inference-engine-2)
- [Replicate: meta/meta-llama-3-70b](https://replicate.com/meta/meta-llama-3-70b)
- [Replicate Blog: Run Meta Llama 3 with an API](https://replicate.com/blog/run-llama-3-with-an-api)
- [Together AI OpenAI Compatibility](https://docs.together.ai/docs/openai-api-compatibility)
- [OpenRouter API Reference](https://openrouter.ai/docs/api_reference/overview)
- [OpenRouter Model Pricing](https://openrouter.ai/meta-llama/llama-3-8b)
- [DeepInfra Inference API](https://deepinfra.com/meta-llama/Meta-Llama-3.1-70B-Instruct/api)
