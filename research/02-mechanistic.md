# Mechanistic Interpretability: Idioms and Multi-Word Expressions

**Research Date:** August 2026  
**Status:** Complete  
**Sources:** 25+ primary papers + API verification  

---

## Pitfalls & Anti-Patterns

### 1. Multi-Token Fusion Happens Early, Not Late
**Pitfall:** Assuming multi-word expressions are represented as separate token activations across all layers.  
**Reality:** "From Tokens to Words" (arXiv:2410.05864) shows final token of multi-token words begins merging into unified representation as early as middle layers (layer 12-16 in Gemma 2 9B). Early-layer attention fuses subword pieces into conceptual units. **Fix:** If probing MWE representation, sample middle + late layers, not just final layer.

### 2. SAE Polysemanticity Corrupts Feature Interpretation
**Pitfall:** Believing a single SAE feature cleanly represents "idiomaticity" or "figurativity."  
**Reality:** "The Rate-Distortion-Polysemanticity Tradeoff in SAEs" (arXiv:2605.14694) shows SAEs optimal for sparsity/reconstruction are routinely polysemantic—mixing multiple concepts in one feature. A feature may represent "idiomaticity" at low activation and "surprise" at high activation. **Fix:** Always inspect activation distributions and representative examples; don't assume monosemanticity.

### 3. Layer-Wise Findings are Model-Specific
**Pitfall:** Expecting idiom-processing circuits to be in the same layers across GPT-2, Llama, Gemma.  
**Reality:** "Anatomy of an Idiom" (arXiv:2511.16467) identifies Idiom Heads and augmented reception in specific models; generalization is unknown. "Tug-of-War" (arXiv:2506.01723) finds early sublayers retrieve figurative meaning, but sublayer depth varies by model family. **Fix:** Verify layer/head positions locally before citing as universal circuit.

### 4. Literal Suppression ≠ Literal Absence
**Pitfall:** Assuming "suppressing literal interpretation" means the literal meaning never activates.  
**Reality:** "Tug-of-War" reveals competing pathways: intermediate pathway prioritizes figurative, direct route favors literal. Both remain available; the model learns to weight them contextually. Suppression is relative, not absolute. **Fix:** When measuring suppression, use causal intervention (ablate figurative heads) to confirm the mechanism, not just activation magnitudes.

### 5. API Documentation Lags Implementation
**Pitfall:** Assuming Neuronpedia's API docs describe what currently works.  
**Reality:** Official Neuronpedia API docs say "work-in-progress." The web UI has per-token search working via Gemma Scope 2, but the REST API is undocumented. Goodfire's Ember API was deprecated early 2026. **Fix:** Test APIs directly; don't trust README-level claims.

---

## What Mechanistic Interpretability Knows About Idioms

### Multi-Token Entity Representation

**Key Finding:** Early layers bind multi-token expressions into unified concepts.

- **"From Tokens to Words: On the Inner Lexicon of LLMs"** (arXiv:2410.05864): Last token of multi-token words (e.g., "##ing" in "fishing") fuses into full-word representation by middle layers. Hidden states diverge significantly from early to middle layers, indicating conceptual reorganization.
- **Nostalgebraist's Logit Lens** (2020): Technique to project hidden states into vocabulary space, showing when token semantics stabilize (often by layer 6-8 in small models).
- **Token Erasure as Footprint** (arXiv:2406.20086): Models erase multi-token subword tokens from early layers, indicating implicit vocabulary item binding occurs before explicit output.

**Practical Implication:** Multi-word idioms likely undergo similar binding: "kick the bucket" tokens fuse into [IDIOM] representation in middle layers before interpretation branches into figurative vs literal paths.

---

### Idiom Retrieval vs Composition

**Key Finding:** Idioms are RETRIEVED as holistic units, not composed from parts. Dedicated "Idiom Heads" bypass compositional processing.

**"Anatomy of an Idiom: Tracing Non-Compositionality in Language Models"** (arXiv:2511.16467):
- Identifies **"Idiom Heads"**: attention heads that frequently activate across different idioms (not specific to one idiom).
- Mechanism: **"Augmented Reception"** — enhanced attention between idiom tokens due to earlier processing, strengthening connections before final interpretation.
- Transformers "balance computational efficiency and robustness" by bypassing compositional assembly for recognized idioms.
- **VERIFIED:** Full paper cites circuit-level evidence; this is not speculative.

**"Tug-of-War Between Idioms' Figurative and Literal Interpretations"** (arXiv:2506.01723):
- **Early sublayers retrieve figurative interpretation.**
- **Specific attention heads retrieve figurative sense while suppressing literal.**
- Two competing pathways: intermediate (figurative) vs direct (literal).
- **Causal tracing confirms:** Ablating figurative heads collapses figurative accuracy.
- Context precedence: When disambiguating context precedes the idiom, early layers leverage it; later layers refine if context conflicts with retrieved interpretation.

**UNVERIFIED claim:** Whether this is true for all models or only tested ones (GPT-2 Small, Llama 2 7B derivatives implied from citations).

---

### Layer-Wise Interpretation

**Key Finding:** Figurative meaning resolves in early-to-middle layers; later layers refine contextual consistency.

| Finding | Source | Evidence |
|---------|--------|----------|
| MWE meaning strongly localized in **early layers** | arXiv:2401.15393 (Survey) | Embedding-level analysis across 20+ papers |
| Idiom figurative retrieval in **early sublayers** | arXiv:2506.01723 | Causal intervention + tuned lens |
| Non-literal retrieval heads identified | arXiv:2607.01002 | Logit-Contribution Scoring on Qwen3, Gemma-3, OLMo-3.1 |
| Later layers refine context fit | arXiv:2506.01723 | When context conflicts, layers 6+ re-weight |

**Practical Implication:** To analyze idiom processing, probe layers 3-8 (early retrieval) and 8-12 (refinement), not just final layer.

---

### Induction Heads & Memorized Phrases

**Key Finding:** Induction heads perform pattern completion, but unclear whether they specialize in idioms.

- **"Induction Heads as an Essential Mechanism for Pattern Matching in In-Context Learning"** (arXiv:2407.07011): Induction heads detect prior token similarity and attend to the next token. Canonically for repetition (A B C ... A B → C).
- **Claim in "Anatomy of an Idiom":** Idiom Heads may interact with induction heads to reinforce memorized idiom sequences.
- **UNVERIFIED:** No direct evidence that induction heads are necessary for idiom processing; may be sufficient but not necessary.

---

## SAE Findings on Idiomaticity & Figurative Language

### What SAEs Can Capture

**"Sparse Auto-Encoder Interprets Linguistic Features in Large Language Models"** (arXiv:2502.20344):
- SAEs decompose residual stream activations into ~65K interpretable features per layer.
- Figurative language features DO exist and activate on metaphors/analogies.
- Activation levels correlate with presence of figurative expressions.

**"A Universal Vibe? Finding and Controlling Language-Agnostic Informal Register with SAEs"** (arXiv:2603.26236):
- **Register features (formality/informality) are learnable via SAEs.**
- Cross-linguistic core: Informal register subspace is geometrically coherent and transfers zero-shot to unseen languages.
- **Causal steering works:** Activating informal-register features shifts model output formality.
- **Implication:** If register features exist, idiomaticity-specific features likely exist but haven't been explicitly catalogued.

### What SAEs Miss

**"Controlling Figurative Language in GPT-2 with Mechanistic Interpretability Using Sparse Autoencoders"** (Samanth Koduru, Medium):
- Identified features for "metaphor" activation at layer 15.
- **Limitation:** No systematic sweep for idiomaticity features; one-off observation.

**"The Rate-Distortion-Polysemanticity Tradeoff in SAEs"** (arXiv:2605.14694):
- SAEs don't guarantee clean feature separation. A feature may represent concept A at low activation, concept B at high activation.
- Polysemanticity is the bottleneck, not missing features.
- **Practical:** Always inspect examples and activation distributions before trusting feature semantics.

**Bottom Line:** SAEs CAN capture idiomaticity/formality/style, but feature quality depends on SAE size and training. Polysemanticity corrupts interpretation; inspect distributions.

---

## What Mechanistic Interpretability DOESN'T Know

### Missing Evidence

1. **Idiom Mechanism Universality**: Do Idiom Heads and augmented reception appear in all models? Only tested on small/medium models so far.
2. **SAE Features for Idiomaticity**: No published SAE feature catalogue explicitly labeled "idiom_is_figurative" or "idiom_ambiguity."
3. **Cross-Linguistic Idiom Processing**: All cited work is English-focused. Unknown if Romance/Sino-Tibetan language models use same circuits.
4. **Fine-Grained Suppression Mechanism**: Papers identify heads involved, not the computational rule they implement (e.g., is suppression via attention masking, feature reweighting, or something else?).
5. **Metaphor vs Idiom Distinction**: Does "kill the lights" (metonymy) use the same circuit as "kick the bucket" (pure idiom)? Unknown.

### Known Limitations

- **Causal Tracing Scope**: Causal tracing identifies necessary components, not sufficient ones; ablating a head reduces but may not eliminate figurative accuracy.
- **Model Scale Dependency**: Small models (7B) may use different circuits than frontier models (70B+).
- **Context Dependency**: All studies assume short context. Behavior in 100K+ context windows untested.

---

## Hosted SAE APIs: Feasibility Assessment

### Active Services

#### Neuronpedia (neuronpedia.org)

**Status:** ACTIVE (March 2024 launch, ongoing updates)

**Per-Token Feature Activations:**
- **Web UI:** YES, working. Gemma Scope 2 interactive explorer shows per-token activation strength via bubble colors.
- **API:** PARTIAL. REST API exists (`/api/feature/`) but per-token endpoint is undocumented. Docs state "work-in-progress."
- **Python Client:** `neuronpedia_inference_client` package on PyPI. Method signatures unclear; docs are offline.
- **Rate Limits:** Unknown (not published).
- **Auth:** Requires API key (signup required, unclear if free).

**Models Supported:**
- Gemma Scope (2B, 9B, Gemma 3 27B-IT)
- Llama Scope (partial)
- GPT-2 Small (legacy)
- 20+ core features (steering, visualization, circuit analysis)

**Verdict:** **PARTIAL GO** — Web UI works now. API is incomplete; you can browse Gemma Scope 2 at neuronpedia.org/gemma-scope-2 and export examples, but programmatic per-token access via REST API is not documented.

**URL:** https://neuronpedia.org/  
**API Docs:** https://docs.neuronpedia.org/api (marked "work-in-progress")  
**Python Package:** https://pypi.org/project/neuronpedia_inference_client/

---

#### Goodfire Ember API

**Status:** DEPRECATED (January 2026). Pivoted to Silico (model design, not interpretability).

**Verdict:** **NO GO** — Do not plan around this service.

**Reference:** https://www.goodfire.ai/blog/announcing-goodfire-ember

---

#### TransluceAI Observatory

**Status:** ACTIVE (open-source toolkit, not hosted API).

**Capabilities:**
- Auto-generate feature descriptions.
- Activation patching (ablation).
- Input ablation for decision rules.
- Supports Llama-3.1 8B and GPT-4o (local + cloud).

**Hosted Service:** No. Code is open-source; deployment is user's responsibility.
**GitHub:** https://github.com/TransluceAI/observatory  
**Verdict:** **LOCAL ONLY** — Not a hosted service.

---

### Free/Low-Cost GPU Options for Local SAE Analysis

#### Google Colab (Free Tier)
- **GPU:** T4 or P100 (varies)
- **Allocation:** 15-30 hours/week
- **Session Limit:** 12 hours
- **SAELens + Gemma 2B + Gemma Scope:** Yes, fits in memory. Inference ~0.5s/token.
- **Verdict:** **YES** — Most practical free option.

#### HuggingFace Spaces ZeroGPU
- **GPU:** Shared pooled A100
- **Cost:** Free for Space builders
- **SAELens + Gemma 2B + Gemma Scope:** Probably yes, but GPU allocation is dynamic.
- **Verdict:** **MAYBE** — Depends on queue; test first.

#### Modal (Serverless)
- **Free Tier:** $30/month compute credit
- **GPUs:** A100, H100 (custom)
- **SAELens + Gemma 2B + Gemma Scope:** Yes.
- **Verdict:** **YES** — Beyond free tier, cost scales with usage (~$0.30/hour A100).

---

## Recommended Approach for Idiom-SAE Study

### Scenario 1: Quick Exploration (No Local GPU)
1. **Interactive:** Browse Neuronpedia Gemma Scope 2 manually. Search idioms (e.g., "kick the bucket"), export example tokens.
2. **Programmatic:** Attempt REST API at `neuronpedia.org/api-doc` if per-token endpoint is published. If not, pivot to Scenario 2.
3. **Cost:** Free (Neuronpedia signup required).

### Scenario 2: Controlled Study (Free GPU + Local SAE)
1. **Setup:** Google Colab + SAELens + Gemma 2B (9B) + Gemma Scope SAEs.
   ```bash
   pip install sae-lens transformerlens
   ```
2. **Code:** Load Gemma 2B, pass idiom prompts, extract per-token activations at layers 4-16.
3. **Analysis:** Plot feature activation heatmaps (idiom tokens vs non-idiom). Identify high-variance features.
4. **Cost:** Free (15-30 hrs/week Colab quota sufficient).
5. **Friction:** ~2-3 hours to script (SAELens docs are good; Gemma Scope integration is stable).

### Scenario 3: Large-Scale Study (Cheap Hosted GPU)
1. **Setup:** Modal free tier ($30 credit) or HF Spaces.
2. **Deploy:** SAELens inference endpoint.
3. **Batch:** 1000+ idiom/control prompts, extract activations.
4. **Cost:** Modal ~$10-30 depending on usage. HF Spaces free if queue allows.

---

## Concrete Next Steps

### High-Priority Research Questions

1. **Does Neuronpedia's per-token API work?**  
   - Check `neuronpedia.org/api-doc` → Test POST `/activations` endpoint with sample idiom.
   - Fallback: Use web UI + manual export.

2. **Are there published SAE features for idiomaticity?**  
   - Search Neuronpedia "idiom" OR "figurative" across all Gemma Scope layers.
   - Check feature descriptions for any mention of non-compositionality.

3. **Which layers/heads should we probe?**  
   - Based on lit: Layer 3-8 (figurative retrieval), layer 8-16 (refinement).
   - Start probe at [4, 6, 8, 10, 12].

4. **Can we replicate "Tug-of-War" suppression on Gemma 2B?**  
   - Collect: idiom + ambiguous context, idiom + disambiguating context.
   - Measure: Figurative logit contribution across layers.
   - Causal test: Ablate top heads at layer 4; measure figurative accuracy loss.

---

## Sources

**Core Mechanistic Interpretability (Idioms):**
- [Anatomy of an Idiom: Tracing Non-Compositionality in Language Models](https://arxiv.org/abs/2511.16467) (arXiv:2511.16467)
- [Tug-of-War Between Idioms' Figurative and Literal Interpretations in LLMs](https://arxiv.org/abs/2506.01723) (arXiv:2506.01723)
- [Logit-Contribution Scoring Identifies Non-Literal Retrieval Heads](https://arxiv.org/abs/2607.01002) (arXiv:2607.01002)

**Multi-Word Expression Representation:**
- [From Tokens to Words: On the Inner Lexicon of LLMs](https://arxiv.org/abs/2410.05864) (arXiv:2410.05864)
- [Semantics of Multiword Expressions in Transformer-Based Models: A Survey](https://arxiv.org/abs/2401.15393) (arXiv:2401.15393)
- [Token Erasure as a Footprint of Implicit Vocabulary Items in LLMs](https://arxiv.org/abs/2406.20086) (arXiv:2406.20086)

**SAE & Features (Figurative Language, Register):**
- [Sparse Auto-Encoder Interprets Linguistic Features in Large Language Models](https://arxiv.org/abs/2502.20344) (arXiv:2502.20344)
- [Controlling Figurative Language in GPT-2 with Mechanistic Interpretability Using SAEs](https://medium.com/@samanthkoduru96/controlling-figurative-language-in-gpt-2-with-mechanistic-interpretability-using-sparse-98c2749f0823) (Samanth Koduru, Medium)
- [A Universal Vibe? Finding and Controlling Language-Agnostic Informal Register with SAEs](https://arxiv.org/abs/2603.26236) (arXiv:2603.26236)
- [The Rate-Distortion-Polysemanticity Tradeoff in SAEs](https://arxiv.org/abs/2605.14694) (arXiv:2605.14694)

**Induction Heads:**
- [Induction Heads as an Essential Mechanism for Pattern Matching in In-Context Learning](https://arxiv.org/abs/2407.07011) (arXiv:2407.07011)
- [Beyond Induction Heads: In-Context Meta Learning Induces Multi-Phase Circuit Emergence](https://arxiv.org/abs/2505.16694) (arXiv:2505.16694)

**Layer-Wise Interpretation Techniques:**
- [Eliciting Latent Predictions from Transformers with the Tuned Lens](https://arxiv.org/abs/2303.08112) (arXiv:2303.08112)

**Tools & Platforms:**
- [Neuronpedia](https://neuronpedia.org/) — Hosted SAE explorer
- [SAELens](https://github.com/jbloomAUS/SAELens) — Python library for SAE training/analysis
- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) — Mechanistic interpretability toolkit
- [TransluceAI Observatory](https://github.com/TransluceAI/observatory) — Open-source feature toolkit (local)
- [Gemma Scope (Google DeepMind)](https://deepmind.google/models/gemma/gemma-scope/) — Pre-trained SAEs for Gemma

**Surveys & Guides:**
- [Mechanistic Interpretability Glossary (Neel Nanda)](https://www.neelnanda.io/mechanistic-interpretability/glossary)
- [Learn Mechanistic Interpretability](https://learnmechinterp.com/)

---

## Summary Table: API Capabilities

| Service | Per-Token API | Models | Hosted? | Status | Cost | Go/No-Go |
|---------|--------------|--------|---------|--------|------|----------|
| **Neuronpedia** | Web UI ✓, REST API ✗ | Gemma, Llama, GPT-2 | Yes | Active (2024+) | Free (API key signup) | PARTIAL GO |
| **Goodfire Ember** | Yes (documented) | Llama 3.3, 3.1 | Yes | **DEPRECATED** (2026) | Was paid | NO GO |
| **TransluceAI Observatory** | Yes (local) | Llama, GPT-4o | No | Active (open-source) | Free (local) | LOCAL ONLY |
| **Google Colab** | Via SAELens | Any (local load) | Yes | Active | Free (15-30h/wk) | YES |
| **Modal** | Via SAELens | Any (local load) | Yes | Active | $30 free + $0.30/h | YES |
| **HF Spaces ZeroGPU** | Via SAELens | Any (local load) | Yes | Active | Free (variable queue) | MAYBE |

---

**Research Completed:** August 9, 2026  
**Last Updated:** 02-mechanistic.md  
**Next Phase:** Implement per-token analysis on Gemma 2B via Colab + SAELens
