# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

This is a Skills IL category repository containing AI agent skills for Hebrew localization, RTL layout, and cultural adaptation. Each subdirectory is a self-contained skill following the open Agent Skills standard.

## Repository Structure

```
localization/
├── .github/                        # CI workflows, issue/PR templates
├── hebrew-rtl-best-practices/      # Skill: Hebrew RTL Best Practices
│   ├── SKILL.md                   # Required skill definition
│   └── references/                # Optional documentation
├── hebrew-nlp-toolkit/            # Skill: Hebrew NLP Toolkit
│   └── SKILL.md
├── CLAUDE.md                       # This file
├── LICENSE                         # MIT
└── README.md                       # Category overview
```

## Skill Format (CRITICAL)

Every skill is a folder containing a `SKILL.md` file. The folder name MUST be kebab-case.

### SKILL.md Structure

```yaml
---
name: skill-name-in-kebab-case        # Required, must match folder name
description: >-                        # Required, <1024 chars, no XML tags
  [What it does]. [When to use it — include trigger phrases].
  [Key capabilities]. [Optional: Do NOT use for X].
license: MIT                           # Optional
metadata:                              # Optional
  author: github-username
  version: 1.0.0
  category: localization
  tags: [hebrew, rtl, nlp]
---
```

### Validation Rules

These rules are enforced by CI on every PR:

1. File must be exactly `SKILL.md` (case-sensitive)
2. YAML frontmatter must have `---` delimiters on both sides
3. `name` field: kebab-case only, must match folder name
4. `description` field: present, under 1024 chars, no XML angle brackets, must include WHAT + WHEN
5. SKILL.md body must be under 5,000 words
6. No `README.md` inside skill folders
7. No skill names containing "claude" or "anthropic"
8. No hardcoded secrets

See [CONTRIBUTING.md](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md) for the full guide.

## Commands

```bash
./scripts/validate-skill.sh <skill-folder>/SKILL.md
```

## Conventions

- All skill folders use kebab-case naming
- Bilingual content should use `{ he: "...", en: "..." }` when applicable
- Israeli-specific context should reference official sources
- Org-level files are inherited from skills-il/.github
