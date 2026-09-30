# How people are thinking about metaphor in 2026, and what it says about LLM metaphor use

Lit review for the USF metaphors group (Brizan). Written 2026-09-30.
Question we are steering toward: **how much do LLMs use or generate metaphors, and in which
circumstances?** Working hypothesis (Paing): LLMs deploy metaphor abundantly in creative or
open-ended assignments and sparingly when asked for definitive assessments.

Verification convention (per workspace rules): every paper below was checked by fetching its
abstract page or PDF on 2026-09-30. VERIFIED means the claim was read from the source.
UNVERIFIED means it comes from a search snippet or a secondary summary. Nothing here is from
an agent's memory.

---

## 1. The primary paper

**Regneri, Aghajari, Kroedel (2026). "Artful Writing, Authentic Emotions: Distinguishing
Human-Written from LLM-Generated Metaphors by Annotation and Classification."**
Proceedings of Learning Non-Literal Expressions with Small Data @ LREC 2026, pp. 51-76,
Palma, May 2026. University of Hamburg (Informatics + Philosophy).
PDF: https://aclanthology.org/2026.nonliteral-1.6.pdf  Data: OSF (link in paper).
Status: VERIFIED, full PDF read.

### What they did

- Two datasets of **novel** metaphors, 20 human-written each, standardized to analogy syntax
  ("X is like a Y") so grammar does not confound the comparison.
  - **Poetry**: metaphors extracted from Persian, German and English poems, each tagged by
    two experts with one or two of six emotions (love, pain, longing, fear, pleasure, regret).
  - **Science communication**: explanatory analogies for scientific concepts, restricted to
    figurative meanings not found in dictionaries.
- Four LLMs (Claude Sonnet 4.5, ChatGPT 5, Gemini 2.5, Mistral) were given the same targets
  (the X) and asked to invent a source (the Y). Poetry prompts asked the model to pick two
  emotions and convey them; science prompts asked it to act as a science communicator.
  Result: 100 analogies per domain (20 human + 80 LLM), 200 total.
- Crowdsourced annotation on MTurk, 10 raters per item: quality, writing (does the author
  seem professional), creativity, comprehensibility, "machine?" (1 = surely human, 5 = surely
  machine). Poetry also got emotion labels; science got helpfulness and expertise.
- Classifiers: RoBERTa embeddings on text, a classifier on the annotations, a length-only
  baseline, and zero-shot "was this written by a machine?" prompts to the same four chatbots.

### What they found (numbers from the paper)

| Finding | Poetry | Science |
|---|---|---|
| Human raters' accuracy at spotting LLM authorship | 0.42 (below chance) | 0.41 |
| Text classifier (RoBERTa) accuracy | 0.83 | 0.60 |
| Length-only baseline | 0.73 | 0.70 |
| Claude / Gemini zero-shot as judge | 1.00 / 1.00 | 0.73 / 0.88 |
| Emotion-guessing accuracy on human vs LLM metaphors (overall) | 68.7 vs 64.6 | n/a |

- **Humans cannot tell.** The "machine" rating differs by 0.02 between human and LLM items.
  Raters even judged ChatGPT's analogies the most human-like.
- **LLM metaphors rate higher than human ones on polish.** In poetry, all four models beat
  humans on "professional writing"; Claude also beat humans significantly on creativity and
  overall quality. Human poetic metaphors are less standardized and split the raters more.
- **Humans win on emotion.** Even though LLMs were told which emotions to convey and humans
  were not, raters recovered the intended emotion more reliably from human metaphors,
  significantly so for "love" and "pleasure." Emotion conveyance is the one feature that made
  an item look human (rho -0.26).
- **Science metaphors are indistinguishable** on every rating dimension. Only length separates
  them (LLM science analogies are shorter, human ones longer and more variable).
- **Machines detect machines.** Surface structure carries an authorship signal that human
  readers do not perceive. Claude and Gemini hit perfect accuracy on poetry. Mistral was
  easiest to detect and worst at conveying emotion.
- Authors' conclusion, quoted: "While LLMs are excellent at generating figurative language to
  explain complex concepts, they struggle with generating less concrete, more sentimental text."

### Why this is the right anchor for us

1. It is the only 2026 paper that puts human and LLM metaphor **production** side by side on
   matched targets. Everything else in the field is comprehension or detection.
2. It splits the result by **circumstance** (poetic vs explanatory), which is exactly the axis
   of the hypothesis. The finding is not "LLMs are worse at metaphor." It is "LLMs match or
   beat humans on explanatory metaphor and fall short on affective metaphor."
3. It gives us a reusable design: matched targets, analogy syntax to remove grammatical
   confounds, crowd ratings plus classifier, and the warning that raters' intuitions about
   what looks "human" are wrong (they treat polish as machine-like and quality as human-like,
   the opposite of the truth).

### Limitations the paper has (some stated, some ours)

- n = 20 human items per domain. Everything is small-data by design (the workshop's theme).
- The metaphors were **elicited**. Every LLM was asked to produce a metaphor. The paper says
  nothing about whether a model would reach for a metaphor **unprompted**, which is the
  question we care about.
- Human poetry items were translated and rephrased into analogy syntax, which the authors
  admit could depress their "writing" and "quality" scores.
- The authorship judges were the same chatbots that generated the items (new accounts, but
  the same models). Circularity risk noted by us, not by them.

---

## 2. Supporting 2026 papers, grouped by what they tell us

### 2a. Frequency is still the hidden variable (matters for any density measure)

**Momen, Zarrieß (2026). "The Frequency Confound in Language-Model Surprisal and Metaphor
Novelty."** *SEM 2026. arXiv 2605.06506. VERIFIED (abstract).
Surprisal from eight Pythia sizes across 154 training checkpoints. Word frequency predicts
human novelty ratings better than surprisal does, and the surprisal-novelty correlation is
an artifact of the surprisal-frequency relationship changing during training.
**For us:** if we score metaphor novelty with a model, we must control lexical frequency, or
"novel" will just mean "rare words." Same lesson as idiom-probe's frequency matching.

**Pissani, Jobanputra, Demberg (2026). "LLMs replicate metaphor norms based on word
co-occurrence but struggle with topic-vehicle mappings."** Frontiers in Language Sciences,
June 2026. VERIFIED (article page).
Eight open LLMs (Llama 3.3 70B, Qwen3 32B, gpt-oss-120b, DeepSeek V3.2, others) normed 300
two-word metaphors on familiarity, aptness, concreteness, metaphoricity, constituency. Models
track humans on familiarity and metaphoricity (frequency-driven) and diverge on aptness and
the dimensions that require identifying topic and vehicle.
**For us:** LLM-as-annotator is fine for "is this metaphorical and how familiar," and not fine
for "is this a good mapping." Use it for detection and density, not for quality.

### 2b. When do LLMs reach for the figurative reading?

**Eichel, Rakshit, Schulte im Walde (2026). "Contextualising (Im)plausible Events Triggers
Figurative Language."** Nonliteral @ LREC 2026. VERIFIED (abstract).
Subject-verb-object triples varied on plausibility and abstract/concrete constituents, judged
by humans and LLMs. Humans separate "implausible" from "non-literal." LLMs show "a bias to
trade implausibility for non-literal, plausible interpretations."
**For us:** this is a **trigger condition** for LLM figurative language that has nothing to
do with creativity. When the literal reading does not fit, the model reframes it as
metaphor. Any production study must separate "asked to be creative" from "literal reading
unavailable."

### 2c. Metaphor and originality are linked, but only in some registers

**Sitter, Zarrieß, Momen, Herrmann (2026). "Decomposing Creativity: Two Small Datasets
Combining Originality Ratings and Metaphor Annotations."** Nonliteral @ LREC 2026.
VERIFIED (abstract).
MetaphOrig: German spatial descriptions from literary prose (KOLIMO) and travel reports
(Wikivoyage), with sentence-level originality ratings from crowds and from four LLMs
(GPT-5, Qwen2.5 32B, Mistral Small 3.2, Llama 3.2 3B) plus word-level metaphor annotation.
Originality density correlates with metaphor density **only in the literary subset**, and
the pattern holds whether humans or LLMs did the rating.
**For us:** direct support for the register half of the hypothesis. Metaphor density is a
creativity signal in literary text and not in functional text. This is human data, so it
is the human baseline shape we should expect our model outputs to be compared against.

### 2d. What LLM creative output looks like in 2026

**Klinge, Ortlieb, Koller (2026). "LLMs Generate Kitsch."** EMNLP 2026. arXiv 2604.25929.
VERIFIED (abstract; PDF partially parsed).
Readers rate LLM stories as kitschier than human ones (stock emotions, competent but
conventional form) and still prefer reading them. The authors attribute it to training.
**For us:** abundance of figurative language is not the same as quality of figurative
language. If LLMs do use more metaphor in creative tasks, expect it to be conventional
metaphor. Density and conventionality must be measured separately.

**Sui (2026). "LLMs Exhibit Significantly Lower Uncertainty in Creative Writing Than
Professional Writers."** arXiv 2602.16162, Feb 2026. VERIFIED (abstract).
28 LLMs on story continuation. Human text carries more uncertainty; the gap is larger for
instruction-tuned and reasoning models and "more pronounced in creative than functional
domains."
**For us:** the creative-vs-functional split is where model behavior diverges most from
humans, which is the same axis as the hypothesis. It also predicts base-vs-instruct
differences (idiom-probe H3).

**Patel, Crossman, Aggarwal, Wenger (2026). "Are LLMs becoming similarly creative? Evidence
from three years of models."** arXiv 2608.19437, Aug 2026. VERIFIED (abstract).
Output diversity on open-ended tasks has decreased significantly across model generations.
**For us:** model recency is a variable. A 2024 model and a 2026 model may differ in
metaphor variety even at the same density.

### 2e. Register is the unit of comparison

**Nieth, Gracheva, Mahlberg, Eskofier, Salin (2026). "How Human-Like Are Large Language
Models? A Register-Aware Linguistic Evaluation Framework."** arXiv 2605.23651, May 2026
(v4 Sep 2026). VERIFIED (abstract).
Compares LLM corpora to human reference corpora per register using Maximum Mean Discrepancy
over Biber's 67 lexico-grammatical features. Seven open instruction-tuned models, five
English registers. All models deviate from humans; which model is closest depends on
register, not size. Metaphor is not among the 67 features.
**For us:** this is the methodological template. Two-sample comparison, per register, human
reference corpus. Our contribution would be adding a metaphor feature to a framework like
this.

### 2f. The field's own framing this year

- **ACL 2026 tutorial, "The Interplay between Metaphors and NLP"** (Boisson, Camacho-Collados,
  Sanchez-Bayona, Agerri). VERIFIED (program page). Frames the field as theory-driven
  resource design plus LLM-era interpretation, multilingual and multimodal. Sanchez-Bayona
  and Agerri's 2025 finding (LLM metaphor "understanding" tracks lexical overlap and length)
  is the skeptical baseline the tutorial builds on.
- **He et al. (2026). "Metaphor Reasoning is Meta-reasoning."** ACL 2026 main, pp. 6914-6935.
  VERIFIED (anthology page). Trains models with RL on generated metaphorical riddles;
  transfer to six out-of-distribution reasoning domains, dependent on scale. Treats metaphor
  as a reasoning primitive, not a stylistic device. Useful contrast for how CS is framing
  metaphor vs how linguistics is.
- **Hu et al. (2026). "Metaphors are a Source of Cross-Domain Misalignment of Large
  Reasoning Models."** arXiv 2601.03388. VERIFIED (abstract). Metaphors in training data
  activate features that carry reasoning patterns across domains incorrectly. Not about
  output, but it means metaphor in the pretraining mix has behavioral consequences.
- **Bollepally, Sloman-Moll, Yamauchi (2026). "Can LLMs interpret figurative language as
  humans do?"** arXiv 2601.09041. VERIFIED (abstract). Surface-level agreement with humans,
  representational divergence, worst on idioms and slang. Comprehension side, consistent
  with the group's earlier reading.
- **Fuoli et al. (2026), published version** of the metaphor identification paper the group
  already has (arXiv 2509.24866) appears in *Applied Corpus Linguistics*. UNVERIFIED: the
  ScienceDirect page returned 403; journal name comes from search results only.

---

## 3. What the 2026 literature says about the hypothesis

**Hypothesis:** LLMs use metaphor abundantly in creative or open-ended assignments and less
in definitive assessments.

**What is supported:**
- The creative-vs-functional axis is where LLM output diverges most from human output
  (Sui; Regneri's poetry-vs-science split).
- In human text, metaphor density tracks originality only in literary registers (Sitter),
  so a register effect on metaphor is the expected human shape.
- When asked, LLMs produce explanatory metaphor at human level and poetic metaphor that
  raters score as more polished and more creative than human poetry (Regneri).

**What is not supported, or complicates it:**
- Nobody has measured **spontaneous** metaphor rate by task type. Every 2026 production
  study prompts for a metaphor. The claim "LLMs use metaphor more in creative tasks" has no
  direct evidence for or against it. That is the gap.
- LLMs also produce figurative readings when the literal reading is implausible (Eichel),
  which is a second trigger unrelated to creativity and could inflate counts in odd contexts.
- Abundance is likely conventional abundance. LLM creative output is rated kitschy (Klinge)
  and homogenizing over time (Patel). Density without a novelty measure would miss this.
- The human-vs-LLM difference that survives scrutiny is affective, not structural: humans
  convey emotion through metaphor better (Regneri). "Less definitive assessment" may be
  proxying for "affective content," and those should be separated.

**Sharpened hypothesis, in two parts:**
- H-density: metaphor density in LLM output increases monotonically with task openness
  (factual answer < technical explanation < evaluative assessment < persuasive essay <
  personal reflection < fiction/poetry), and the slope is steeper than the human slope on
  the same prompts.
- H-novelty: the extra metaphor is conventional. Novel-metaphor rate does not rise with
  openness in LLM output, while it does in human output.

---

## 4. A concrete experiment the group could run

Instrument, assembled from the papers above:

1. **Prompt ladder**: 6 task types spanning definitive to open (see H-density), 30 prompts
   each, identical prompts to every model. Topics held constant across rungs where possible
   (the same topic asked as a fact, an explanation, an assessment, an essay, a reflection,
   a story).
2. **Human baseline**: human-written text in matching registers. Candidates: Stack Exchange
   answers (factual/explanatory), review sites and op-eds (evaluative/persuasive), personal
   blogs or essays (reflective), short fiction and poetry corpora (creative). Match length.
3. **Models**: open models locally (Llama 3.1 8B base and instruct, OLMo 2, per idiom-probe's
   preflight) plus two or three frontier models via API. Base vs instruct tests whether
   post-training drives the pattern (Sui's finding).
4. **Metaphor annotation**: MIPVU / Pragglejaz procedure. Run a fine-tuned detector in the
   Fuoli style, validated against the VU Amsterdam Metaphor Corpus, and hand-check a sample.
   Do not use the same model as annotator and subject (Regneri circularity, Pissani's
   aptness caveat).
5. **Measures**: metaphors per 100 words (density), conventional vs novel split (dictionary
   sense present or not, as in Regneri's inclusion rule), lexical-frequency-controlled
   novelty (Momen), and type mix (Banaruee's relational vs attributive, already in the
   group's doc).
6. **Analysis**: density ~ openness x source (human/LLM) x model family. Two-sample
   comparison per register in the Nieth style if we want to plug into an existing framework.

Cost and scale: about 180 prompts x ~10 models = ~1,800 generations, plus a human corpus of
similar size. Annotation is the bottleneck; the detector makes it tractable, and a 10%
hand-checked sample keeps it honest.

---

## 5. Honest gaps in this review

- Coverage is arXiv, ACL Anthology, one Frontiers journal, and conference program pages,
  all found via web search on one day. Journal-only linguistics work (Metaphor and Symbol,
  Cognitive Linguistics, Journal of Pragmatics) is under-covered and may hold the best
  "how people think about metaphor in 2026" paper from the linguistics side.
- Regneri's PDF was read in full. The others were read at abstract level only.
- No paper was found that measures unprompted metaphor rate in LLM output by task type.
  Absence in search is not absence in the literature. Worth one more targeted pass before
  claiming novelty to the professor.
