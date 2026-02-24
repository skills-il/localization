# Hebrew NLP Toolkit Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill that guides developers in using Hebrew NLP tools — DictaLM, DictaBERT, AlephBERT, ivrit.ai, and NNLP-IL resources for Hebrew text processing.

**Architecture:** Domain-Specific Intelligence skill. Embeds knowledge of Hebrew NLP ecosystem, model capabilities, and best practices for Hebrew text processing tasks.

**Tech Stack:** SKILL.md, references for model comparisons and usage guides.

---

## Research

### Hebrew NLP Models
- **DictaLM 3.0** (2025): 1.7B/7B/14B params, ~100B Hebrew tokens, tool-calling support, state of the art
- **DictaBERT**: Hebrew BERT models for understanding tasks (NER, sentiment, classification)
- **AlephBERT** (Bar-Ilan): Alternative Hebrew BERT, good for research
- **Hebrew-Gemma-11B** (Yam Peleg): Multilingual with strong Hebrew
- **ivrit.ai**: Hebrew Whisper models (22K+ hours audio), speech-to-text
- **NNLP-IL**: National NLP initiative, comprehensive resource ecosystem

### Hebrew NLP Challenges
- Rich morphology: Words have multiple valid analyses
- No diacritics (niqqud) in modern text: Ambiguity in vowelization
- Affixes: Prepositions, articles, possessives attach to words
- Gender and number agreement: Complex grammatical system
- Code-switching: Israeli text frequently mixes Hebrew and English

### Use Cases
1. **Model selection** — Choose the right Hebrew NLP model for a task
2. **Text preprocessing** — Tokenization, normalization for Hebrew text
3. **NER for Hebrew** — Named entity recognition in Hebrew documents
4. **Sentiment analysis** — Hebrew sentiment classification
5. **Speech-to-text** — Hebrew audio transcription setup

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: hebrew-nlp-toolkit
description: >-
  Guide developers in using Hebrew NLP models and tools including DictaLM,
  DictaBERT, AlephBERT, and ivrit.ai. Use when user asks about Hebrew text
  processing, Hebrew NLP, "ivrit", Hebrew tokenization, Hebrew NER, Hebrew
  sentiment analysis, Hebrew speech-to-text, or needs to process Hebrew
  language text programmatically. Covers model selection, preprocessing,
  and Hebrew-specific NLP challenges. Do NOT use for Arabic NLP (different
  tools) or general English NLP tasks.
license: MIT
allowed-tools: "Bash(python:*) Bash(pip:*)"
compatibility: "Requires Python and transformers library for model usage. GPU recommended for large models."
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags: [nlp, hebrew, dictalm, dictabert, ivrit-ai, machine-learning]
---

# Hebrew NLP Toolkit

## Instructions

### Step 1: Identify the NLP Task
| Task | Recommended Model | Size | Notes |
|------|-------------------|------|-------|
| Text generation | DictaLM 3.0 (14B) | 14B | Best Hebrew generation |
| Classification | DictaBERT | 110M | Fast, good accuracy |
| NER | DictaBERT-NER | 110M | Trained on Hebrew NER dataset |
| Sentiment | DictaBERT-Sentiment | 110M | Hebrew sentiment classification |
| Embedding/Search | AlephBERT | 110M | Good for similarity tasks |
| Speech-to-text | ivrit.ai Whisper | Various | 22K+ hours training data |
| Translation | DictaLM 3.0 (7B) | 7B | Hebrew<->English |
| Tool calling | DictaLM 3.0 Chat | 7B/14B | Supports function calling |

### Step 2: Install and Load Model

**DictaBERT (classification tasks):**
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert")
model = AutoModelForSequenceClassification.from_pretrained("dicta-il/dictabert")
```

**DictaLM 3.0 (generation):**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictalm-3.0-7b-chat")
model = AutoModelForCausalLM.from_pretrained("dicta-il/dictalm-3.0-7b-chat")
```

**ivrit.ai Whisper (speech-to-text):**
```python
import whisper
# Use ivrit.ai fine-tuned model
model = whisper.load_model("ivrit-ai/whisper-large-v3-he")
```

### Step 3: Hebrew Text Preprocessing
Before feeding text to models:
1. **Normalize:** Remove extra whitespace, normalize Unicode (NFC)
2. **Handle niqqud:** Remove diacritics unless specifically needed
3. **Handle English:** Decide whether to keep, translate, or mark English tokens
4. **Tokenization:** Hebrew tokenizers handle morphological splitting

```python
import re
import unicodedata

def preprocess_hebrew(text):
    # Normalize Unicode
    text = unicodedata.normalize('NFC', text)
    # Remove niqqud (diacritics) - range U+0591 to U+05C7
    text = re.sub(r'[\u0591-\u05C7]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### Step 4: Handle Hebrew-Specific Challenges
- **Morphological analysis:** Use Dicta morphological analyzer for accurate word segmentation
- **No capital letters:** Hebrew has no upper/lowercase distinction — NER is harder
- **Right-to-left in code:** Ensure proper bidi handling in string operations
- **Mixed Hebrew-English:** Common in tech text, may need separate processing

## Resources
- Dicta models: `https://huggingface.co/dicta-il`
- ivrit.ai: `https://huggingface.co/ivrit-ai`
- AlephBERT: `https://huggingface.co/onlplab/alephbert-base`
- NNLP-IL resources: Hebrew NLP community resources

## Examples

### Example 1: Hebrew Text Classification
User says: "I need to classify Hebrew customer reviews as positive or negative"
Result: Guide to use DictaBERT-Sentiment with fine-tuning on domain data.

### Example 2: Hebrew Named Entity Recognition
User says: "Extract company and person names from Hebrew articles"
Result: Use DictaBERT-NER model, demonstrate with example text.

## Troubleshooting

### Error: "Tokenization produces unexpected results"
Cause: Hebrew morphology splitting prefixes (b-, k-, l-, m-, sh-, v-)
Solution: This is expected behavior. Hebrew words like "bveit" (in the house) are split into morphemes.

### Error: "GPU out of memory"
Cause: DictaLM 14B requires ~28GB VRAM
Solution: Use the 7B or 1.7B variant, or quantize with bitsandbytes (4-bit).
```
