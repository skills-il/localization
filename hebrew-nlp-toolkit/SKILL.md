---
name: hebrew-nlp-toolkit
description: Guide developers in using Hebrew NLP models and tools including DictaLM, DictaBERT, AlephBERT, and ivrit.ai. Use when user asks about Hebrew text processing, Hebrew NLP, "ivrit", Hebrew tokenization, Hebrew NER, Hebrew sentiment analysis, Hebrew speech-to-text, or needs to process Hebrew language text programmatically. Covers model selection, preprocessing, and Hebrew-specific NLP challenges. Do NOT use for Arabic NLP (different tools) or general English NLP tasks.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*)
compatibility: Requires Python and transformers library for model usage. GPU recommended for large models.
---

# Hebrew NLP Toolkit

## Instructions

### Step 1: Identify the NLP Task
| Task | Recommended Model | HuggingFace ID | Size | Notes |
|------|-------------------|---------------|------|-------|
| Text generation (large) | DictaLM 3.0 24B Base | `dicta-il/DictaLM-3.0-24B-Base` | 24B | Best Hebrew generation, built on Mistral-Small-3.1-24B |
| Text generation (small) | DictaLM 3.0 Nemotron Instruct | `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` | 12B | Instruction-tuned, smaller footprint |
| Reasoning / chain-of-thought | DictaLM 3.0 24B Thinking | `dicta-il/DictaLM-3.0-24B-Thinking` | 24B | Emits explicit thinking blocks before answering |
| Lightweight / edge | DictaLM 3.0 1.7B Thinking (GGUF) | `dicta-il/DictaLM-3.0-1.7B-Thinking-GGUF` | 1.7B | Runs on laptop / CPU via llama.cpp |
| Classification / fill-mask | DictaBERT | `dicta-il/dictabert` | 184M | Fast, good accuracy |
| NER | DictaBERT NER | `dicta-il/dictabert-ner` | 184M | Recognizes PER, GPE, TIMEX, TTL |
| Sentiment | DictaBERT Sentiment | `dicta-il/dictabert-sentiment` | 184M | Hebrew sentiment classification |
| Morphology | DictaBERT Morph | `dicta-il/dictabert-morph` | 184M | Prefix segmentation and POS |
| Hebrew QA | DictaBERT HeQ | `dicta-il/dictabert-heq` | 184M | Extractive question answering |
| Embeddings (modern) | NeoDictaBERT Bilingual Embed | `dicta-il/neodictabert-bilingual-embed` | 400M | Hebrew-English sentence embeddings |
| Embeddings (legacy) | AlephBERT | `onlplab/alephbert-base` | 110M | Older baseline for similarity |
| Speech-to-text | ivrit.ai Whisper v3 | `ivrit-ai/whisper-large-v3` | 1.55B | Fine-tuned on the ivrit.ai Hebrew speech corpus (a 22K+ hour dataset) |
| Speech-to-text (fast) | ivrit.ai Whisper v3 Turbo CT2 | `ivrit-ai/whisper-large-v3-turbo-ct2` | 809M | CTranslate2, ~3x faster inference |

### Step 2: Install and Load Model

**DictaBERT (base model, fill-mask):**
```python
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert")
model = AutoModelForMaskedLM.from_pretrained("dicta-il/dictabert")
```
`dicta-il/dictabert` is a masked-LM base with NO classification head. Do not load it with `AutoModelForSequenceClassification` and run inference, that instantiates a randomly-initialised head and returns meaningless predictions. For classification, either fine-tune it on labeled data first, or use a ready task-specific model such as `dicta-il/dictabert-sentiment` (sentiment) or `dicta-il/dictabert-ner` (NER).

**DictaLM 3.0 (generation, 12B instruct):**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/DictaLM-3.0-Nemotron-12B-Instruct")
model = AutoModelForCausalLM.from_pretrained("dicta-il/DictaLM-3.0-Nemotron-12B-Instruct")
```

For the strongest quality, swap to `dicta-il/DictaLM-3.0-24B-Base`. For reasoning tasks (math, multi-step logic), use `dicta-il/DictaLM-3.0-24B-Thinking`, which writes its chain of thought inside an explicit thinking block before the final answer.

**ivrit.ai Whisper (speech-to-text):**
```python
from transformers import pipeline
# ivrit.ai fine-tuned Hebrew ASR, based on openai/whisper-large-v3
pipe = pipeline("automatic-speech-recognition", model="ivrit-ai/whisper-large-v3")
result = pipe("audio.wav", generate_kwargs={"language": "he"})
```
For lower latency, use `ivrit-ai/whisper-large-v3-turbo-ct2` via `faster-whisper` (CTranslate2 backend, roughly 3x faster on GPU).

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

### Step 4: Nikud Restoration (Diacritization)

The preprocessing above *removes* nikud. The opposite task, *adding* nikud back to unvocalized text, is called diacritization and is its own core Hebrew NLP problem (useful for text-to-speech, language learning, liturgical text, and disambiguation).

Dicta's Nakdan is the standard tool. The character-level model is published on HuggingFace:

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-large-char-menaked')
model = AutoModel.from_pretrained('dicta-il/dictabert-large-char-menaked', trust_remote_code=True)
model.eval()

# The model exposes a `predict` helper that returns vocalized text
vocalized = model.predict(['שלום עולם'], tokenizer)
```

Notes:
- `trust_remote_code=True` is required because the model ships a custom `predict` head. Review the model card before enabling it.
- Diacritization is ambiguous: the same consonantal text can have multiple valid vocalizations depending on context. Treat output as a best guess, not ground truth.
- For full sentence-level vocalization with morphological context, Dicta's hosted Nakdan (see Step 6) generally outperforms a raw character model.

### Step 5: Hosted Dicta REST APIs

If you do not want to run models locally, Dicta exposes its tools (Nakdan, morphology, and more) as hosted web services. This suits low-volume use, prototyping, or environments without a GPU.

- Nakdan (diacritization): https://nakdan.dicta.org.il/
- Developer access and API details: https://dicta.org.il/developers

Verify the current endpoint shape, request format, rate limits, and terms of use on the developer page before integrating, as hosted API contracts change. Do not assume an endpoint URL or payload schema, consult the official developer docs.

### Step 6: Alternative NLP Entry Points

Dicta and ivrit.ai are the primary Hebrew-specific stacks, but two general NLP frameworks also ship Hebrew pipelines:

- **HebSpacy** (https://github.com/8400TheHealthNetwork/HebSpacy): a spaCy pipeline for Hebrew with tokenization, POS, lemmatization, and NER. Good when you already use spaCy and want a single API.
- **Stanza** (https://stanfordnlp.github.io/stanza/): Stanford's NLP toolkit ships a Hebrew model with tokenization, morphology, lemmatization, and dependency parsing. Good for academic / cross-lingual pipelines.

For best Hebrew accuracy, Dicta models still lead. Use these frameworks when integration convenience outweighs raw quality.

### Step 7: Handle Hebrew-Specific Challenges
- **Morphological analysis:** Use Dicta morphological analyzer for accurate word segmentation
- **No capital letters:** Hebrew has no upper/lowercase distinction -- NER is harder
- **Right-to-left in code:** Ensure proper bidi handling in string operations
- **Mixed Hebrew-English:** Common in tech text, may need separate processing

## Examples

### Example 1: Hebrew Text Classification
User says: "I need to classify Hebrew customer reviews as positive or negative"
Result: Guide to use DictaBERT-Sentiment with fine-tuning on domain data.

### Example 2: Hebrew Named Entity Recognition
User says: "Extract company and person names from Hebrew articles"
Result: Use DictaBERT-NER model, demonstrate with example text.

## Bundled Resources

### Scripts
- `scripts/preprocess_hebrew.py`: Normalize Hebrew text before feeding it to NLP models (DictaBERT, DictaLM, AlephBERT). Handles Unicode NFC normalization, niqqud removal, whitespace cleanup, URL stripping, shekel symbol normalization, and mixed Hebrew-English text segmentation. Run: `python scripts/preprocess_hebrew.py --help`

### References
- `references/model-comparison.md`: Side-by-side comparison of Hebrew NLP models (DictaLM 3.0, DictaBERT, AlephBERT, NeoDictaBERT, ivrit.ai Whisper) with VRAM requirements, HuggingFace IDs, and a task-to-model mapping table. Consult when choosing which model to use for a specific Hebrew NLP task.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| DICTA Israel Center for Text Analysis (HuggingFace) | https://huggingface.co/dicta-il | Latest DictaLM and DictaBERT model variants, IDs, release notes |
| ivrit.ai (HuggingFace) | https://huggingface.co/ivrit-ai | Current Whisper fine-tunes for Hebrew ASR, dataset versions |
| AlephBERT on HuggingFace | https://huggingface.co/onlplab/alephbert-base | AlephBERT model card and usage |
| ivrit.ai project site | https://www.ivrit.ai/en/ | Dataset size, license, research papers |
| NNLP-IL (Israeli NLP community) | https://github.com/NNLP-IL | Curated list of Hebrew NLP resources and benchmarks |
| DictaLM 3.0 Technical Report (Dicta) | https://dicta.org.il/publications/DictaLM_3_0___Techincal_Report.pdf | Architecture, base-model lineage, training data, eval results |
| Dicta Nakdan (diacritization) | https://nakdan.dicta.org.il/ | Hosted nikud restoration tool |
| Dicta developer access | https://dicta.org.il/developers | Hosted REST API details and terms |
| HebSpacy (spaCy for Hebrew) | https://github.com/8400TheHealthNetwork/HebSpacy | spaCy Hebrew pipeline, install instructions |
| Stanza (Hebrew model) | https://stanfordnlp.github.io/stanza/ | Hebrew tokenization, morphology, parsing |

## Gotchas
- Hebrew has no capital letters, so agents cannot use capitalization-based NER (Named Entity Recognition) heuristics that work for English. Hebrew NER requires morphological analysis or trained models.
- Hebrew words can be prefixed with multiple particles (prepositions, conjunctions, articles) that are written as part of the word. The string "ובבית" (u-va-bayit) is "and in the house" as a single token. Agents may treat it as one word.
- The Hebrew letter system has five final forms (sofit): kaf, mem, nun, pe, tsadi. Agents may normalize these to their non-final forms, breaking word matching and search.
- Nikud (vowel diacritics) is almost never present in modern Hebrew text. Agents trained on nikud-annotated text may fail on standard unvocalized Hebrew. Always design for nikud-less input.

## Troubleshooting

### Error: "Tokenization produces unexpected results"
Cause: Hebrew morphology splitting prefixes (b-, k-, l-, m-, sh-, v-)
Solution: This is expected behavior. Hebrew words like "bveit" (in the house) are split into morphemes.

### Error: "GPU out of memory"
Cause: DictaLM 3.0 24B needs roughly 48GB VRAM in BF16, and the Nemotron-12B variant needs roughly 24GB.
Solution: Drop to `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` (12B), the 1.7B Thinking GGUF variant, or use the FP8 / W4A16 quantized checkpoints published under the same org (e.g., `DictaLM-3.0-24B-Base-FP8`). For laptop-class hardware, run the 1.7B GGUF via llama.cpp.