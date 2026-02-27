---
name: hebrew-nlp-toolkit
description: >-
  Guide developers in using Hebrew NLP models and tools including DictaLM,
  DictaBERT, AlephBERT, and ivrit.ai. Use when user asks about Hebrew text
  processing, Hebrew NLP, "ivrit", Hebrew tokenization, Hebrew NER, Hebrew
  sentiment analysis, Hebrew speech-to-text, or needs to process Hebrew language
  text programmatically. Covers model selection, preprocessing, and
  Hebrew-specific NLP challenges. Do NOT use for Arabic NLP (different tools) or
  general English NLP tasks.
license: MIT
allowed-tools: 'Bash(python:*) Bash(pip:*)'
compatibility: >-
  Requires Python and transformers library for model usage. GPU recommended for
  large models.
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags:
    he:
      - עיבוד-שפה-טבעית
      - עברית
      - DictaLM
      - DictaBERT
      - עברית-AI
      - למידת-מכונה
    en:
      - nlp
      - hebrew
      - dictalm
      - dictabert
      - ivrit-ai
      - machine-learning
  display_name:
    he: ערכת כלי NLP לעברית
    en: Hebrew Nlp Toolkit
  display_description:
    he: 'עיבוד שפה טבעית בעברית — ניתוח מורפולוגי, זיהוי ישויות ועוד'
    en: >-
      Guide developers in using Hebrew NLP models and tools including DictaLM,
      DictaBERT, AlephBERT, and ivrit.ai. Use when user asks about Hebrew text
      processing, Hebrew NLP, "ivrit", Hebrew tokenization, Hebrew NER, Hebrew
      sentiment analysis, Hebrew speech-to-text, or needs to process Hebrew
      language text programmatically. Covers model selection, preprocessing, and
      Hebrew-specific NLP challenges. Do NOT use for Arabic NLP (different
      tools) or general English NLP tasks.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
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
| Translation | DictaLM 3.0 (7B) | 7B | Hebrew to/from English |
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
    text = re.sub(r'[֑-ׇ]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### Step 4: Handle Hebrew-Specific Challenges
- **Morphological analysis:** Use Dicta morphological analyzer for accurate word segmentation
- **No capital letters:** Hebrew has no upper/lowercase distinction -- NER is harder
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

## Bundled Resources

### Scripts
- `scripts/preprocess_hebrew.py` — Normalize Hebrew text before feeding it to NLP models (DictaBERT, DictaLM, AlephBERT). Handles Unicode NFC normalization, niqqud removal, whitespace cleanup, URL stripping, shekel symbol normalization, and mixed Hebrew-English text segmentation. Run: `python scripts/preprocess_hebrew.py --help`

### References
- `references/model-comparison.md` — Side-by-side comparison of Hebrew NLP models (DictaLM 3.0, DictaBERT, AlephBERT, ivrit.ai Whisper, Hebrew-Gemma) with VRAM requirements, HuggingFace IDs, and a task-to-model mapping table. Consult when choosing which model to use for a specific Hebrew NLP task.

## Troubleshooting

### Error: "Tokenization produces unexpected results"
Cause: Hebrew morphology splitting prefixes (b-, k-, l-, m-, sh-, v-)
Solution: This is expected behavior. Hebrew words like "bveit" (in the house) are split into morphemes.

### Error: "GPU out of memory"
Cause: DictaLM 14B requires ~28GB VRAM
Solution: Use the 7B or 1.7B variant, or quantize with bitsandbytes (4-bit).