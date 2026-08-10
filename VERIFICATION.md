# Verification log

Per `.claude/rules/learnings.md` (2026-07-30): separate VERIFIED from UNVERIFIED before
any claim gets repeated out loud. Agent output is not evidence. Every row below was
checked by direct fetch or live API call on 2026-08-09.

## VERIFIED

| Claim | How checked | Result |
|---|---|---|
| Idioms are retrieved early and the literal reading is actively suppressed; competing figurative/literal pathways | Fetched arXiv:2506.01723 | CONFIRMED. "Tug-of-war between idioms' figurative and literal interpretations in LLMs", Oh/Huang/Pink/Hahn/Demberg. Causal tracing. Early sublayers + specific attention heads retrieve figurative while suppressing literal; intermediate pathway favors figurative, parallel direct route favors literal |
| "Idiom Heads" exist, found by causal intervention | Fetched arXiv:2511.16467 | CONFIRMED. "Anatomy of an Idiom: Tracing Non-Compositionality in Language Models", Gomes. Idiom Heads + "augmented reception" via path patching |
| Frequency gap of ~70 points between top and bottom decile | Fetched arXiv:2202.07206 | CONFIRMED, quoted correctly: "above 70% (absolute) more accurate on the top 10% frequent terms in comparison to the bottom 10%" |
| Chengyu-Bench exists, has appropriateness task, ~85% SOTA | Fetched aclanthology.org/2025.emnlp-main.119 + search | CONFIRMED. EMNLP 2025, arXiv:2506.18105, 2,937 examples / 1,765 idioms |
| EnDive is a real cross-dialect benchmark incl. Jamaican English | Search + ACL Findings PDF | CONFIRMED. EMNLP 2025 Findings, arXiv:2504.07100. 5 dialects (AAVE, IndE, JamE, ChcE, CollSgE), 12 tasks, incl. GPT-4o / Claude 3.5 / LLaMa-3-8B. NOTE: the specific per-dialect percentages the agent quoted are still unchecked |
| infini-gram public API works | Live POST to api.infini-gram.io | CONFIRMED. Exact counts, ~40ms, no auth |
| Replicate hosts base Llama 3 8B | Fetched replicate.com/meta/meta-llama-3-8b | CONFIRMED present, no deprecation notice |
| Neuronpedia `/api/activation/new` accepts arbitrary text, no auth | Live POST | CONFIRMED. Returns per-token activation values for a named feature. No API key needed |
| Neuronpedia OpenAPI spec location | Probed 6 candidate paths | `/swagger.json` is the real spec (26 endpoints). All other candidates return the SPA shell with HTTP 200 — status code alone is not a validity check here |

## REFUTED

| Claim | Source | Reality |
|---|---|---|
| OpenRouter serves `meta-llama/llama-3-8b` **base**, "Verified August 2026" | post-training agent, its PRIMARY recommendation | **FALSE.** Live query of openrouter.ai/api/v1/models (400 models): every Llama 3.x 8B/70B entry is `-instruct`. No base Llama |
| Neuronpedia per-token API is "undocumented / work-in-progress", verdict PARTIAL GO | mechanistic agent | **OVERSTATED.** The spec is published at `/swagger.json` with 26 documented endpoints. `/api/activation/new` works unauthenticated today. Verdict should be **GO** |

Lesson (both cases): the agent read docs or blog posts and inferred availability instead of
calling the endpoint. One curl settled each. Where an API is load-bearing, call it.

## Neuronpedia: what the study actually needs

| Endpoint | Purpose | Auth |
|---|---|---|
| `POST /api/search-all` | Given text, return **which** features fire (top-k). This is the discovery step | **API key required** (free signup) |
| `POST /api/activation/new` | Given a **known** feature + text, return per-token activations. The measurement step | None observed |
| `GET /api/feature/{modelId}/{layer}/{index}` | Feature metadata + existing explanation | Not checked |
| `POST /api/steer` | Causal test: clamp a feature and see if figurative reading breaks | Not checked |

Implication: the whole mechanistic phase is runnable with **zero GPU**. Get a free
Neuronpedia key, use `search-all` to find idiom-selective features, `activation/new` to
measure them per item, and `steer` for a causal check. Colab is now the fallback, not the
requirement.

## STILL UNVERIFIED

- **Decomposability does not predict accuracy.** Contradicts psycholinguistic intuition. No
  primary source opened. If we rely on it, check first — or just measure it ourselves.
- **EnDive per-dialect numbers** (Jamaican 53.19% vs SAE 88.47%, etc.). Benchmark is real;
  these specific figures are not checked.
- **Kirk et al. ICLR 2024 diversity magnitudes.** Paper real; agent cited arXiv 2310.06452
  for it, ID unconfirmed.
- **Replicate logprobs.** Schema introspection returned an empty property list, which is
  inconclusive rather than negative. Matters less now that Colab is available.
- **MDial** benchmark and its numbers. Not checked at all.
