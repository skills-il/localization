# Localization Skills

AI agent skills for Hebrew language, RTL layout, NLP, and cultural adaptation.

Part of [Skills IL](https://github.com/skills-il) — curated AI agent skills for Israeli developers.

## Skills

| Skill | Description | Scripts | References |
|-------|-------------|---------|------------|
| [hebrew-rtl-best-practices](./hebrew-rtl-best-practices/) | RTL layout for Hebrew web and mobile apps. CSS logical properties, Tailwind RTL, React/Vue RTL, Hebrew typography. | -- | 1 |
| [hebrew-nlp-toolkit](./hebrew-nlp-toolkit/) | Hebrew NLP model selection and usage: DictaLM, DictaBERT, AlephBERT, ivrit.ai. Preprocessing, tokenization, NER. | `preprocess_hebrew.py` | 1 |
| [hebrew-content-writer](./hebrew-content-writer/) | Write professional Hebrew content. Grammar rules, formal/informal register, gendered language, Hebrew SEO. | -- | 1 |
| [hebrew-ocr-forms](./hebrew-ocr-forms/) | OCR Israeli government forms: Tabu extracts, tax forms, Bituach Leumi documents. Image preprocessing and field extraction. | `preprocess_image.py`, `extract_form_fields.py` | 1 |
| [shabbat-aware-scheduler](./shabbat-aware-scheduler/) | Schedule around Shabbat, Israeli holidays (chagim), and Hebrew calendar. HebCal API, Israeli business hours (Sun-Thu). | `check_shabbat.py` | 1 |

## Install

```bash
# Claude Code - install a specific skill
claude install github:skills-il/localization/hebrew-rtl-best-practices

# Or clone the full repo
git clone https://github.com/skills-il/localization.git
```

## Contributing

See the org-level [Contributing Guide](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md).

## License

MIT

---

Built with care in Israel.
