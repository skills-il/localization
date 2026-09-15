# Hebrew NLP Model Comparison Guide

## Model Overview

### DictaLM 3.0 (DICTA, published on HuggingFace late 2025)
DictaLM 3.0 is the current Hebrew LLM family from the Dicta Institute. Base-model lineage per the DictaLM 3.0 Technical Report:
- The **24B** variants are initialized from Mistral-Small-3.1-24B-Base-2503.
- The **Nemotron 12B** variant is initialized from an NVIDIA Nemotron Nano v2 12B base (a hybrid Mamba/Transformer base).
- The **1.7B** variant is initialized from Qwen3-1.7B-Base. It is NOT Nemotron-derived.

All three sizes were continuously pre-trained on roughly 100B Hebrew tokens mixed with about 30B tokens of English data.
- **Variants published on HuggingFace:**
  - `dicta-il/DictaLM-3.0-24B-Base` (24B, BF16) -- strongest open Hebrew model
  - `dicta-il/DictaLM-3.0-24B-Thinking` (24B) -- reasoning model, emits explicit thinking block
  - `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` (12B) -- instruction-tuned, smaller footprint
  - `dicta-il/DictaLM-3.0-Nemotron-12B-Base` (12B, base)
  - `dicta-il/DictaLM-3.0-1.7B-Thinking-GGUF` (1.7B, GGUF) -- runs on laptop via llama.cpp
  - Quantized: `DictaLM-3.0-24B-Base-FP8`, `DictaLM-3.0-24B-Thinking-FP8`, `DictaLM-3.0-24B-Thinking-W4A16`, `DictaLM-3.0-Nemotron-12B-Instruct-FP8`, `DictaLM-3.0-Nemotron-12B-Instruct-W4A16`
- **Licenses:** the 24B models are Apache-2.0; `DictaLM-3.0-Nemotron-12B-Instruct` is under the NVIDIA Open Model License and needs `trust_remote_code=True`
- **Use for:** Text generation, translation, summarization, chat, reasoning, tool calling
- **Hardware (weights only, estimated at 2 bytes per parameter in BF16):** 24B ≈ 48GB, Nemotron-12B ≈ 24GB, 1.7B ≈ 3.5GB. FP8 roughly halves the weight memory and W4A16 roughly quarters it. KV cache and activations come on top.

### DictaBERT family (DICTA)
- **Size:** ~184M parameters (BERT-base)
- **Variants and model IDs:**
  - `dicta-il/dictabert` -- fill-mask base model
  - `dicta-il/dictabert-ner` -- Hebrew NER with 13 entity types (ANG, DUC, EVE, FAC, GPE, INFORMAL, LOC, MISC, ORG, PER, TIMEX, TTL, WOA), also `dicta-il/dictabert-large-ner`
  - `dicta-il/dictabert-sentiment` -- Hebrew sentiment classification, usable without fine-tuning
  - `dicta-il/dictabert-morph` -- morphological tagging
  - `dicta-il/dictabert-seg` -- prefix segmentation
  - `dicta-il/dictabert-joint` -- joint morphology pipeline
  - `dicta-il/dictabert-heq` -- Hebrew extractive QA
  - `dicta-il/dictabert-parse` / `dicta-il/dictabert-large-parse` / `dicta-il/dictabert-tiny-parse` -- dependency parsing
- **Use for:** Classification, NER, sentiment analysis, morphological analysis, QA
- **License:** CC-BY-4.0
- **Hardware:** Runs on CPU; GPU gives a significant batch speedup

### NeoDictaBERT Bilingual Embed (DICTA, 2026)
- **Model ID:** `dicta-il/neodictabert-bilingual-embed`
- **Size:** ~363M parameters, 768-dimensional vectors
- **Usage:** `SentenceTransformer(..., trust_remote_code=True)`, with `encode_query` (queries prefixed `query: `) and `encode_document`
- **Strengths:** Modern Hebrew-English sentence embedding model, the recommended starting point over AlephBERT for new projects
- **Use for:** Semantic search, clustering, cross-lingual retrieval

### AlephBERT (Bar-Ilan University, legacy)
- **Size:** BERT-base architecture
- **HuggingFace:** `onlplab/alephbert-base`
- **Use for:** Similarity baselines and research; for new projects prefer NeoDictaBERT
- **Hardware:** Runs on CPU

### ivrit.ai Whisper Models
- **Base:** Fine-tunes of OpenAI Whisper, Apache-2.0. The ivrit.ai corpus as a whole is over 22,000 hours. Each checkpoint lists its own training data on its model card (whisper-large-v3: Knesset plenums ~4700h, crowd-transcribe-v5 ~300h, crowd-recital ~50h; turbo-ct2: 295h crowd-transcribe-v5 plus 93h professionally transcribed speech from other sources)
- **Key variants:**
  - `ivrit-ai/whisper-large-v3` (1.55B) -- standard accuracy target, transformers
  - `ivrit-ai/whisper-large-v3-turbo-ct2` (809M, CTranslate2) -- lighter inference via `faster-whisper`
  - `ivrit-ai/faster-whisper-v2-d4` -- legacy, based on whisper-large-v2 and crowd-transcribe-v4 (September 2024)
- **Use for:** Speech-to-text, audio transcription, voice interfaces
- **Hardware:** the turbo build (809M) is much smaller than large-v3 (1.55B); with faster-whisper use `compute_type="int8"` on CPU

## Task-to-Model Mapping

| Task | First Choice | Alternative | Notes |
|------|-------------|-------------|-------|
| Text generation (best) | DictaLM 3.0 24B Base | DictaLM 3.0 Nemotron-12B Instruct | 24B for quality, 12B for cost |
| Reasoning / math | DictaLM 3.0 24B Thinking | DictaLM 3.0 24B Base | Thinking model emits an explicit chain-of-thought block |
| Laptop / edge LLM | DictaLM 3.0 1.7B Thinking GGUF | DictaLM 3.0 Nemotron-12B W4A16 | Run via llama.cpp |
| Classification | DictaBERT | Fine-tuned DictaBERT | Fine-tune on your data |
| NER | DictaBERT NER | DictaBERT Large NER | Pre-trained NER variant |
| Sentiment | DictaBERT Sentiment | DictaBERT + fine-tune | Pre-trained sentiment head |
| Morphology | DictaBERT Joint | DictaBERT Morph (tagging) / DictaBERT Seg (prefix segmentation) | Joint covers segmentation, tagging, lemma and parse in one model |
| Hebrew QA | DictaBERT HeQ | DictaLM 3.0 24B | HeQ is extractive, DictaLM is generative |
| Embeddings / similarity | NeoDictaBERT Bilingual Embed | AlephBERT | NeoDictaBERT is the 2026 baseline |
| Speech-to-text | ivrit.ai Whisper v3 | ivrit.ai Whisper v3 Turbo CT2 | Turbo CT2 is smaller (809M vs 1.55B) and trained on a different subset |
| Translation | DictaLM 3.0 24B Base | DictaLM 3.0 Nemotron-12B Instruct | Use instruct variant with prompt |
| Summarization | DictaLM 3.0 Nemotron-12B Instruct | DictaLM 3.0 24B Base | Nemotron-12B is cheaper |

## Hebrew NLP Challenges Reference

### Morphological Complexity
Hebrew has a rich morphological system where prefixes attach to words:
- **b-** (in/at): בבית = ב + בית (in the house)
- **k-** (like/as): כבית = כ + בית (like a house)
- **l-** (to/for): לבית = ל + בית (to the house)
- **m-** (from): מהבית = מ + ה + בית (from the house)
- **sh-** (that/which): שהוא = ש + הוא (that he)
- **v-** (and): ובית = ו + בית (and a house)
- **h-** (the): הבית = ה + בית (the house)

### No Vowelization in Modern Text
Modern Hebrew text omits diacritics (niqqud), creating ambiguity:
- שמר can be "shamar" (guarded) or "shemer" (yeast)
- Context is essential for disambiguation
- Models trained on unvowelized text handle this naturally

### No Case Distinction
Hebrew has no upper/lowercase letters, making NER harder:
- English: "Apple released..." (capitalization hints at entity)
- Hebrew: "אפל השיקה..." (no capitalization cue)
- NER models must rely entirely on context
