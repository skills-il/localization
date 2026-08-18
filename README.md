# Localization Skills

AI agent skills for Hebrew language, RTL layout, NLP, and cultural adaptation.

Part of [Skills IL](https://github.com/skills-il) — curated AI agent skills for Israeli developers.

## Skills

| Skill | Description | Scripts | References |
|-------|-------------|---------|------------|
| [hebrew-content-writer](./hebrew-content-writer/) | Write professional Hebrew content. Grammar rules, formal/informal register, gendered language, Hebrew SEO. | -- | `hebrew-grammar-quick-ref.md` |
| [hebrew-document-generator](./hebrew-document-generator/) | Generate Hebrew PDF, DOCX, and PPTX with RTL support. reportlab, WeasyPrint, python-docx, pptxgenjs. Israeli business templates. | `generate_doc.py` | `hebrew-fonts.md`, `templates.md` |
| [hebrew-i18n](./hebrew-i18n/) | Hebrew internationalization patterns. Plural forms, date/number formatting, RTL CSS, bidi text, React/Vue/Angular integration. | `generate_i18n.py` | `pluralization.md`, `bidi.md` |
| [hebrew-nlp-toolkit](./hebrew-nlp-toolkit/) | Hebrew NLP model selection and usage: DictaLM, DictaBERT, AlephBERT, ivrit.ai. Preprocessing, tokenization, NER. | `preprocess_hebrew.py` | `model-comparison.md` |
| [hebrew-ocr-forms](./hebrew-ocr-forms/) | OCR Israeli government forms: Tabu extracts, tax forms, Bituach Leumi documents. Image preprocessing and field extraction. | `preprocess_image.py`, `extract_form_fields.py` | `israeli-form-types.md` |
| [hebrew-rtl-best-practices](./hebrew-rtl-best-practices/) | RTL layout for Hebrew web and mobile apps. CSS logical properties, Tailwind RTL, React/Vue RTL, Hebrew typography. | -- | `css-logical-properties.md` |
| [hebrew-tailwind-preset](./hebrew-tailwind-preset/) | Tailwind CSS v4 RTL configuration. Dir variants, Hebrew font stacks, logical property utilities (ms-/me-). | -- | `rtl-config.md` |
| [israeli-accessibility-compliance](./israeli-accessibility-compliance/) | Israeli web accessibility per IS 5568 standard and WCAG 2.1 AA. Hebrew screen readers, RTL ARIA patterns, legal requirements. | `audit_a11y.py` | `is-5568.md` |
| [israeli-ui-design-system](./israeli-ui-design-system/) | RTL-first UI components and design tokens. Hebrew font pairings, gov.il design patterns, Israeli form layouts. | -- | `hebrew-typography.md` |
| [shabbat-aware-scheduler](./shabbat-aware-scheduler/) | Schedule around Shabbat, Israeli holidays (chagim), and Hebrew calendar. HebCal API, Israeli business hours (Sun-Thu). | `check_shabbat.py` | `israeli-holiday-calendar.md` |

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
