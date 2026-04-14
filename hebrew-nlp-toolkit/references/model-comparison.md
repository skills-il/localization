# Hebrew NLP Model Comparison Guide

## Model Overview

### DictaLM 3.0 (DICTA, released Dec 2025)
DictaLM 3.0 is the current Hebrew LLM family from the Dicta Institute. The 24B variants are initialized from Mistral-Small-3.1-24B-Base-2503; the Nemotron 12B variant is initialized from an NVIDIA Nemotron base.
- **Variants published on HuggingFace:**
  - `dicta-il/DictaLM-3.0-24B-Base` (24B, BF16) -- strongest open Hebrew model
  - `dicta-il/DictaLM-3.0-24B-Thinking` (24B) -- reasoning model, emits explicit thinking block
  - `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` (12B) -- instruction-tuned, smaller footprint
  - `dicta-il/DictaLM-3.0-Nemotron-12B-Base` (12B, base)
  - `dicta-il/DictaLM-3.0-1.7B-Thinking-GGUF` (1.7B, GGUF) -- runs on laptop via llama.cpp
  - Quantized: `DictaLM-3.0-24B-Base-FP8`, `DictaLM-3.0-24B-Thinking-FP8`, `DictaLM-3.0-24B-Thinking-W4A16`, `DictaLM-3.0-Nemotron-12B-Instruct-FP8`, `DictaLM-3.0-Nemotron-12B-Instruct-W4A16`
- **Use for:** Text generation, translation, summarization, chat, reasoning, tool calling
- **Hardware (BF16):** 24B ≈ 48GB VRAM, Nemotron-12B ≈ 24GB VRAM, 1.7B ≈ 3.5GB VRAM. FP8 halves the requirement; W4A16 quarters it.

### DictaBERT family (DICTA)
- **Size:** ~184M parameters (BERT-base)
- **Variants and model IDs:**
  - `dicta-il/dictabert` -- fill-mask base model
  - `dicta-il/dictabert-ner` -- Hebrew NER (PER, GPE, TIMEX, TTL), also `dicta-il/dictabert-large-ner`
  - `dicta-il/dictabert-sentiment` -- Hebrew sentiment classification
  - `dicta-il/dictabert-morph` -- morphological segmentation and POS
  - `dicta-il/dictabert-seg` -- segmentation
  - `dicta-il/dictabert-joint` -- joint morphology pipeline
  - `dicta-il/dictabert-heq` -- Hebrew extractive QA
  - `dicta-il/dictabert-parse` / `dicta-il/dictabert-large-parse` / `dicta-il/dictabert-tiny-parse` -- dependency parsing
- **Use for:** Classification, NER, sentiment analysis, morphological analysis, QA
- **Hardware:** Runs on CPU with ~1GB RAM; GPU gives a significant batch speedup

### NeoDictaBERT Bilingual Embed (DICTA, 2026)
- **Model ID:** `dicta-il/neodictabert-bilingual-embed`
- **Size:** ~400M parameters
- **Strengths:** Modern Hebrew-English sentence embedding model, better similarity than AlephBERT for new projects
- **Use for:** Semantic search, clustering, cross-lingual retrieval

### AlephBERT (Bar-Ilan University, legacy)
- **Size:** ~110M parameters (BERT-base)
- **HuggingFace:** `onlplab/alephbert-base`
- **Use for:** Similarity baselines and research; for new projects prefer NeoDictaBERT
- **Hardware:** Runs on CPU, ~500MB RAM

### ivrit.ai Whisper Models
- **Base:** Fine-tunes of OpenAI Whisper on 22K+ hours of Hebrew audio, published under a permissive license
- **Key variants:**
  - `ivrit-ai/whisper-large-v3` (1.55B) -- standard accuracy target
  - `ivrit-ai/whisper-large-v3-turbo-ct2` (809M, CTranslate2) -- fast inference via `faster-whisper`
  - `ivrit-ai/whisper-large-v2-tuned`, `ivrit-ai/faster-whisper-v2-d4` -- older baselines
- **Use for:** Speech-to-text, audio transcription, voice interfaces
- **Hardware:** large-v3 needs ~10GB VRAM; turbo-ct2 runs lighter and roughly 3x faster

## Task-to-Model Mapping

| Task | First Choice | Alternative | Notes |
|------|-------------|-------------|-------|
| Text generation (best) | DictaLM 3.0 24B Base | DictaLM 3.0 Nemotron-12B Instruct | 24B for quality, 12B for cost |
| Reasoning / math | DictaLM 3.0 24B Thinking | DictaLM 3.0 24B Base | Thinking model emits an explicit chain-of-thought block |
| Laptop / edge LLM | DictaLM 3.0 1.7B Thinking GGUF | DictaLM 3.0 Nemotron-12B W4A16 | Run via llama.cpp |
| Classification | DictaBERT | Fine-tuned DictaBERT | Fine-tune on your data |
| NER | DictaBERT NER | DictaBERT Large NER | Pre-trained NER variant |
| Sentiment | DictaBERT Sentiment | DictaBERT + fine-tune | Pre-trained sentiment head |
| Morphology | DictaBERT Morph | DictaBERT Joint | Handles prefixes well |
| Hebrew QA | DictaBERT HeQ | DictaLM 3.0 24B | HeQ is extractive, DictaLM is generative |
| Embeddings / similarity | NeoDictaBERT Bilingual Embed | AlephBERT | NeoDictaBERT is the 2026 baseline |
| Speech-to-text | ivrit.ai Whisper v3 | ivrit.ai Whisper v3 Turbo CT2 | Turbo CT2 is ~3x faster |
| Translation | DictaLM 3.0 24B Base | DictaLM 3.0 Nemotron-12B Instruct | Use instruct variant with prompt |
| Summarization | DictaLM 3.0 Nemotron-12B Instruct | DictaLM 3.0 24B Base | Nemotron-12B is cheaper |

## Hebrew NLP Challenges Reference

### Morphological Complexity
Hebrew has a rich morphological system where prefixes attach to words:
- **b-** (in/at): בבית = ב + בית (in the house)
- **k-** (like/as): כמו = כ + מו
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
