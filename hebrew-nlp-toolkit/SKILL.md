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
| Text generation (large) | DictaLM 3.0 24B Base | `dicta-il/DictaLM-3.0-24B-Base` | 24B | Best Hebrew generation, built on Mistral-Small-3.1-24B. Apache-2.0 |
| Text generation (small) | DictaLM 3.0 Nemotron Instruct | `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` | 12B | Instruction-tuned. NVIDIA Open Model License, not Apache |
| Reasoning / chain-of-thought | DictaLM 3.0 24B Thinking | `dicta-il/DictaLM-3.0-24B-Thinking` | 24B | Emits explicit thinking blocks before answering |
| Lightweight / edge | DictaLM 3.0 1.7B Thinking (GGUF) | `dicta-il/DictaLM-3.0-1.7B-Thinking-GGUF` | 1.7B | Runs on laptop / CPU via llama.cpp |
| Classification / fill-mask | DictaBERT | `dicta-il/dictabert` | 184M | Base model, fine-tune for classification |
| NER | DictaBERT NER | `dicta-il/dictabert-ner` | 184M | 13 entity types incl. PER, ORG, LOC, GPE, FAC, TIMEX, TTL |
| Sentiment | DictaBERT Sentiment | `dicta-il/dictabert-sentiment` | 184M | Works out of the box, returns Positive / Negative / Neutral style labels |
| Morphology / segmentation | DictaBERT Joint | `dicta-il/dictabert-joint` | 184M | Prefix segmentation, POS, lemma, dependency parse |
| Hebrew QA | DictaBERT HeQ | `dicta-il/dictabert-heq` | 184M | Extractive question answering |
| Embeddings (modern) | NeoDictaBERT Bilingual Embed | `dicta-il/neodictabert-bilingual-embed` | ~363M | Hebrew-English sentence embeddings, 768 dimensions |
| Embeddings (legacy) | AlephBERT | `onlplab/alephbert-base` | BERT-base | Older baseline for similarity |
| Speech-to-text | ivrit.ai Whisper v3 | `ivrit-ai/whisper-large-v3` | 1.55B | Trained on about 5,000 hours drawn from the ivrit.ai corpus (Knesset plenums, crowd transcriptions, recitals) |
| Speech-to-text (fast) | ivrit.ai Whisper v3 Turbo CT2 | `ivrit-ai/whisper-large-v3-turbo-ct2` | 809M | CTranslate2 build for `faster-whisper` |

The full ivrit.ai Hebrew audio corpus is over 22,000 hours. Each checkpoint lists its own training data on its model card, and the numbers differ: whisper-large-v3 lists about 5,000 hours, while the turbo-ct2 build lists 295 hours of crowd transcriptions plus 93 hours of professionally transcribed speech from other sources.

Several of these models ship custom code and need `trust_remote_code=True` (Nemotron, `dictabert-joint`, `dictabert-large-char-menaked`, `neodictabert-bilingual-embed`). That flag runs Python from the model repo on your machine, so read the model card and pin a revision in production.

### Step 2: Install, Load and Run

**Sentiment (ready to use, no fine-tuning):**
```python
from transformers import pipeline

oracle = pipeline('sentiment-analysis', model='dicta-il/dictabert-sentiment')
print(oracle(['אני אוהב את השירות']))
```

**NER (grouped entities):**
```python
from transformers import pipeline
from tokenizers.decoders import WordPiece

oracle = pipeline('ner', model='dicta-il/dictabert-ner', aggregation_strategy='simple')
# with aggregation_strategy='simple' the tokenizer needs a decoder, per the model card
oracle.tokenizer.backend_tokenizer.decoder = WordPiece()
print(oracle('דוד בן-גוריון נולד בפולין'))
```
Without the decoder line, grouped entities come back as broken `##` word-piece fragments.

**DictaBERT (base model, fill-mask):**
```python
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert")
model = AutoModelForMaskedLM.from_pretrained("dicta-il/dictabert")
```
`dicta-il/dictabert` is a masked-LM base with NO classification head. Do not load it with `AutoModelForSequenceClassification` and run inference, that instantiates a randomly-initialised head and returns meaningless predictions. For classification, fine-tune it on labeled data first, or use a ready task-specific model such as `dicta-il/dictabert-sentiment` or `dicta-il/dictabert-ner`.

**Morphology and prefix segmentation (dictabert-joint):**
```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-joint')
model = AutoModel.from_pretrained('dicta-il/dictabert-joint', trust_remote_code=True)
model.eval()
print(model.predict(['ובבית הספר למדנו'], tokenizer, output_style='json'))
```

**Sentence embeddings (NeoDictaBERT):**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("dicta-il/neodictabert-bilingual-embed", trust_remote_code=True)
query_embeddings = model.encode_query(["query: מתכון לעוגת שוקולד"])
document_embeddings = model.encode_document(["עוגת שוקולד פשוטה בעשר דקות"])
```
Keep the `query: ` prefix on queries as the model card shows; dropping it degrades retrieval.

**DictaLM 3.0 (generation, 12B instruct):**
```python
from transformers import pipeline

generator = pipeline('text-generation', model="dicta-il/DictaLM-3.0-Nemotron-12B-Instruct", trust_remote_code=True)
```
For serving, the model card recommends vLLM (`vllm serve dicta-il/DictaLM-3.0-Nemotron-12B-Instruct --enable-auto-tool-choice --tool-call-parser hermes --trust-remote-code`). For the strongest quality, and an Apache-2.0 license, use `dicta-il/DictaLM-3.0-24B-Base`. For reasoning tasks, use `dicta-il/DictaLM-3.0-24B-Thinking`, which writes its chain of thought inside an explicit thinking block before the final answer.

**ivrit.ai Whisper (speech-to-text, faster-whisper):**
```python
import faster_whisper

model = faster_whisper.WhisperModel('ivrit-ai/whisper-large-v3-turbo-ct2')
segs, _ = model.transcribe('media-file', language='he')
print(' '.join(s.text for s in segs))
```
`segs` is a generator, so transcription only runs when you iterate it. On CPU pass `device="cpu", compute_type="int8"`; `vad_filter=True` skips silence, and `word_timestamps=True` gives per-word timing for subtitles. To use plain transformers instead, load `ivrit-ai/whisper-large-v3` with `pipeline("automatic-speech-recognition", ...)` and `generate_kwargs={"language": "he"}`.

### Step 3: Hebrew Text Preprocessing
Before feeding text to models:
1. **Normalize:** Remove extra whitespace, normalize Unicode (NFC)
2. **Handle niqqud:** Remove diacritics unless specifically needed
3. **Handle English:** Decide whether to keep, translate, or mark English tokens
4. **Tokenization:** DictaBERT and AlephBERT tokenizers split words into WordPiece sub-units, not morphemes. If you need real prefix segmentation (for search indexing, counting, lemmas) run `dictabert-joint` from Step 2

```python
import re
import unicodedata

def preprocess_hebrew(text):
    # Normalize Unicode
    text = unicodedata.normalize('NFC', text)
    # Remove niqqud and cantillation, but keep maqaf U+05BE and other punctuation in the block
    text = re.sub(r'[֑-ׇֽֿׁׂׅׄ]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```
Stripping the whole U+0591 to U+05C7 range is a common bug: it deletes the maqaf and fuses hyphenated words (`עולם־גדול` becomes `עולםגדול`).

### Step 4: Nikud Restoration (Diacritization)

The preprocessing above *removes* nikud. The opposite task, *adding* nikud back to unvocalized text, is called diacritization and is its own core Hebrew NLP problem (useful for text-to-speech, language learning, and disambiguation).

Dicta's Nakdan is the standard tool. The character-level model is published on HuggingFace:

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-large-char-menaked')
model = AutoModel.from_pretrained('dicta-il/dictabert-large-char-menaked', trust_remote_code=True)
model.eval()

# predict takes a list of sentences and returns a list of vocalized sentences
vocalized = model.predict(['שלום עולם'], tokenizer)
```

Notes:
- `trust_remote_code=True` is required because the model ships a custom `predict` head. Review the model card before enabling it.
- The model card says it targets modern Hebrew prose and is not intended for Biblical, Rabbinic, premodern or poetic texts.
- Diacritization is ambiguous: the same consonantal text can have multiple valid vocalizations depending on context. Treat output as a best guess, not ground truth.
- For full sentence-level vocalization with morphological context, Dicta's hosted Nakdan (see Step 5) generally outperforms a raw character model.

### Step 5: Hosted Dicta REST APIs

If you do not want to run models locally, Dicta exposes its tools (Nakdan, morphology, and more) as hosted web services. This suits low-volume use, prototyping, or environments without a GPU.

- Nakdan (diacritization): https://nakdan.dicta.org.il/
- Developer access and API details: https://dicta.org.il/developers

Verify the current endpoint shape, request format, rate limits, and terms of use on the developer page before integrating, as hosted API contracts change. Do not assume an endpoint URL or payload schema, consult the official developer docs.

### Step 6: Alternative NLP Entry Points

Dicta and ivrit.ai are the primary Hebrew-specific stacks, but two general NLP frameworks also ship Hebrew pipelines:

- **HebSpacy** (https://github.com/8400TheHealthNetwork/HebSpacy): a spaCy pipeline whose published model, `he_ner_news_trf`, is an AlephBERT-based NER model with 16 entity types. It does not ship POS tagging or lemmatization. Good when you already use spaCy and need Hebrew NER. Check the repository's last commit date and pin your spaCy version before adopting it.
- **Stanza** (https://stanfordnlp.github.io/stanza/): Stanford's NLP toolkit ships a Hebrew model with tokenization, morphology, lemmatization, and dependency parsing. Good for academic / cross-lingual pipelines.

For best Hebrew accuracy, Dicta models still lead. Use these frameworks when integration convenience outweighs raw quality.

### Step 7: Handle Hebrew-Specific Challenges
- **Morphological analysis:** Use `dictabert-joint` (or Dicta's hosted tools) for accurate word segmentation
- **No capital letters:** Hebrew has no upper/lowercase distinction -- NER is harder
- **Right-to-left in code:** Ensure proper bidi handling in string operations
- **Mixed Hebrew-English:** Common in tech text, may need separate processing
- **Licenses differ per model:** DictaBERT models are CC-BY-4.0, DictaLM 24B is Apache-2.0, the Nemotron 12B variant is under the NVIDIA Open Model License. Check before shipping commercially

## Examples

### Example 1: Hebrew Text Classification
User says: "I need to classify Hebrew customer reviews as positive or negative"
Result: Run `dicta-il/dictabert-sentiment` through the `sentiment-analysis` pipeline first (it works without training). Fine-tune it on labeled domain reviews only if its accuracy on a sample of your data is not good enough.

### Example 2: Hebrew Named Entity Recognition
User says: "Extract company and person names from Hebrew articles"
Result: Use the `dicta-il/dictabert-ner` pipeline with `aggregation_strategy='simple'` and the WordPiece decoder, then keep the `ORG` and `PER` entities.

### Example 3: Transcribe a Hebrew Recording
User says: "Transcribe a one-hour Hebrew podcast to text"
Result: Use `faster-whisper` with `ivrit-ai/whisper-large-v3-turbo-ct2`, `language='he'`, and `vad_filter=True`; iterate the segments generator and write each segment's text with its timestamps.

## Bundled Resources

### Scripts
- `scripts/preprocess_hebrew.py`: Normalize Hebrew text before feeding it to NLP models (DictaBERT, DictaLM, AlephBERT). Handles Unicode NFC normalization, niqqud removal (keeping the maqaf), whitespace cleanup, URL stripping, thousands-separator and shekel-abbreviation normalization, and mixed Hebrew-English text segmentation. Run: `python scripts/preprocess_hebrew.py --help`

### References
- `references/model-comparison.md`: Side-by-side comparison of Hebrew NLP models (DictaLM 3.0, DictaBERT, AlephBERT, NeoDictaBERT, ivrit.ai Whisper) with VRAM requirements, HuggingFace IDs, licenses, and a task-to-model mapping table. Consult when choosing which model to use for a specific Hebrew NLP task.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| DICTA Israel Center for Text Analysis (HuggingFace) | https://huggingface.co/dicta-il | Latest DictaLM and DictaBERT model variants, IDs, licenses |
| ivrit.ai (HuggingFace) | https://huggingface.co/ivrit-ai | Current Whisper fine-tunes for Hebrew ASR, dataset versions |
| AlephBERT on HuggingFace | https://huggingface.co/onlplab/alephbert-base | AlephBERT model card and usage |
| ivrit.ai project site | https://www.ivrit.ai/en/ivrit-ai-2/ | Corpus size, license |
| NNLP-IL (Israeli NLP community) | https://github.com/NNLP-IL | Curated list of Hebrew NLP resources and benchmarks |
| DictaLM 3.0 Technical Report (Dicta) | https://dicta.org.il/publications/DictaLM_3_0___Techincal_Report.pdf | Architecture, base-model lineage, training data, eval results |
| Dicta Nakdan (diacritization) | https://nakdan.dicta.org.il/ | Hosted nikud restoration tool |
| Dicta developer access | https://dicta.org.il/developers | Hosted REST API details and terms |
| faster-whisper | https://github.com/SYSTRAN/faster-whisper | `WhisperModel`, `compute_type`, VAD and word timestamps |
| Stanza (Hebrew model) | https://stanfordnlp.github.io/stanza/ | Hebrew tokenization, morphology, parsing |

## Gotchas
- Hebrew has no capital letters, so agents cannot use capitalization-based NER (Named Entity Recognition) heuristics that work for English. Hebrew NER requires morphological analysis or trained models.
- Hebrew words can be prefixed with multiple particles (prepositions, conjunctions, articles) that are written as part of the word. The string "ובבית" (u-va-bayit) is "and in the house" as a single token. Agents may treat it as one word.
- The Hebrew letter system has five final forms (sofit): kaf, mem, nun, pe, tsadi. Agents may normalize these to their non-final forms, breaking word matching and search.
- Nikud (vowel diacritics) is almost never present in modern Hebrew text. Agents trained on nikud-annotated text may fail on standard unvocalized Hebrew. Always design for nikud-less input.
- Agents often "normalize" the shekel abbreviation with a plain substring replace of ש and ח, which also rewrites ordinary words such as שחר and משחק. Match it only as a standalone token.

## Troubleshooting

### Error: "Tokens look like fragments with ## in them"
Cause: DictaBERT and AlephBERT use WordPiece tokenization, which splits rare words into sub-word pieces. These are not morphemes.
Solution: For NER, set `aggregation_strategy='simple'` plus the WordPiece decoder shown in Step 2. For real prefix segmentation, use `dictabert-joint`.

### Error: "GPU out of memory"
Cause: in BF16 the weights alone take about 2 bytes per parameter, so roughly 48GB for DictaLM 3.0 24B and roughly 24GB for the Nemotron-12B variant, before KV cache and activations.
Solution: Drop to `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` (12B), the 1.7B Thinking GGUF variant, or use the FP8 / W4A16 quantized checkpoints published under the same org (e.g., `DictaLM-3.0-24B-Base-FP8`). For laptop-class hardware, run a GGUF build via llama.cpp.
