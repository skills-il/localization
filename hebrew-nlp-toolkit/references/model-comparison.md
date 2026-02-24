# Hebrew NLP Model Comparison Guide

## Model Overview

### DictaLM 3.0 (Dicta Institute, 2025)
- **Sizes:** 1.7B, 7B, 14B parameters
- **Training data:** ~100B Hebrew tokens
- **Strengths:** Best Hebrew text generation, supports tool-calling, chat fine-tuned
- **HuggingFace:** `dicta-il/dictalm-3.0-7b-chat`, `dicta-il/dictalm-3.0-14b`
- **Use for:** Text generation, translation, summarization, chat applications
- **Hardware:** 7B needs ~14GB VRAM, 14B needs ~28GB VRAM (FP16)

### DictaBERT (Dicta Institute)
- **Size:** ~110M parameters (BERT-base)
- **Variants:** Base, NER, Sentiment, Morphological
- **Strengths:** Fast inference, good for classification tasks, domain-adapted variants
- **HuggingFace:** `dicta-il/dictabert`, `dicta-il/dictabert-ner`
- **Use for:** Classification, NER, sentiment analysis, morphological analysis
- **Hardware:** Runs on CPU, ~500MB RAM

### AlephBERT (Bar-Ilan University)
- **Size:** ~110M parameters (BERT-base)
- **Strengths:** Good for embedding/similarity tasks, research-grade
- **HuggingFace:** `onlplab/alephbert-base`
- **Use for:** Semantic similarity, text embeddings, research
- **Hardware:** Runs on CPU, ~500MB RAM

### ivrit.ai Whisper Models
- **Base:** Fine-tuned OpenAI Whisper on 22K+ hours of Hebrew audio
- **Strengths:** Best Hebrew speech-to-text accuracy
- **HuggingFace:** `ivrit-ai/whisper-large-v3-he`
- **Use for:** Speech-to-text, audio transcription, voice interfaces
- **Hardware:** Large model needs ~10GB VRAM

### Hebrew-Gemma-11B (Yam Peleg)
- **Size:** 11B parameters
- **Strengths:** Multilingual with strong Hebrew, good for code + Hebrew
- **Use for:** Code generation with Hebrew comments, multilingual tasks

## Task-to-Model Mapping

| Task | First Choice | Alternative | Notes |
|------|-------------|-------------|-------|
| Text generation | DictaLM 3.0 14B | DictaLM 3.0 7B | Use 7B for speed |
| Classification | DictaBERT | AlephBERT | Fine-tune on your data |
| NER | DictaBERT-NER | DictaBERT + fine-tune | Pre-trained NER variant |
| Sentiment | DictaBERT-Sentiment | DictaBERT + fine-tune | Pre-trained sentiment |
| Embeddings | AlephBERT | DictaBERT | AlephBERT better for similarity |
| Speech-to-text | ivrit.ai Whisper | OpenAI Whisper | ivrit.ai is fine-tuned |
| Translation | DictaLM 3.0 7B | DictaLM 3.0 14B | Chat variant recommended |
| Summarization | DictaLM 3.0 7B | DictaLM 3.0 14B | Good at Hebrew summaries |
| Morphology | DictaBERT-Morph | Custom pipeline | Handles prefixes well |

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
