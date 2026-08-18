# Hebrew Fonts Reference

## Recommended Fonts by Document Type

### Sans-Serif (Modern Documents, Web, Invoices)

| Font | Weight Range | Google Fonts | Notes |
|------|-------------|--------------|-------|
| Heebo | 100-900 | [Link](https://fonts.google.com/specimen/Heebo) | Most popular Hebrew web font, excellent readability |
| Rubik | 300-900 | [Link](https://fonts.google.com/specimen/Rubik) | Slightly rounded, friendly appearance |
| Assistant | 200-800 | [Link](https://fonts.google.com/specimen/Assistant) | Clean, professional, good for business docs |
| Open Sans Hebrew | 300-800 | Bundled with Open Sans | Widely available, neutral style |
| Noto Sans Hebrew | 100-900 | [Link](https://fonts.google.com/noto/specimen/Noto+Sans+Hebrew) | Part of Google Noto family, maximum language coverage |

### Serif (Formal Documents, Contracts, Legal)

| Font | Weight Range | Google Fonts | Notes |
|------|-------------|--------------|-------|
| Frank Ruhl Libre | 300-900 | [Link](https://fonts.google.com/specimen/Frank+Ruhl+Libre) | Classic Hebrew serif, ideal for legal/formal |
| David Libre | 400-700 | [Link](https://fonts.google.com/specimen/David+Libre) | Based on classic David font, elegant |
| Noto Serif Hebrew | 100-900 | [Link](https://fonts.google.com/noto/specimen/Noto+Serif+Hebrew) | Full Unicode coverage |

### System Fonts (No Installation Required)

| Font | Available On | Style |
|------|-------------|-------|
| David | Windows, macOS (with Office) | Classic serif |
| Narkisim | Windows | Elegant serif |
| Arial Hebrew | macOS | Sans-serif |
| Courier New (Hebrew) | Windows, macOS | Monospace |

## Font Pairing Recommendations

| Use Case | Primary (Headings) | Secondary (Body) |
|----------|-------------------|-----------------|
| Business docs | Heebo Bold | Heebo Regular |
| Legal contracts | Frank Ruhl Libre Bold | David Libre Regular |
| Marketing material | Rubik Bold | Assistant Regular |
| Technical docs | Assistant SemiBold | Noto Sans Hebrew Regular |
| Presentations | Heebo Black | Heebo Light |

## Font Stack CSS Examples

```css
/* Modern business documents */
font-family: 'Heebo', 'Assistant', 'Arial Hebrew', sans-serif;

/* Formal/legal documents */
font-family: 'Frank Ruhl Libre', 'David Libre', 'David', serif;

/* Code with Hebrew comments */
font-family: 'Cousine', 'Noto Sans Mono', 'Courier New', monospace;
```

## Installation Instructions

### macOS
```bash
# Via Homebrew (installs Google Fonts collection)
brew install --cask font-heebo font-rubik font-assistant

# Manual: Download TTF from Google Fonts, double-click to install
```

### Linux (Ubuntu/Debian)
```bash
# Noto fonts (includes Hebrew)
sudo apt-get install fonts-noto fonts-noto-extra

# Manual: Copy TTF files to ~/.local/share/fonts/ then run
fc-cache -fv
```

### Windows
Download TTF from Google Fonts, right-click and select "Install" or "Install for all users."

### Python reportlab Registration
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Heebo', '/path/to/Heebo-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Heebo-Bold', '/path/to/Heebo-Bold.ttf'))
```

## Typography Settings for Hebrew

- **Font size:** Use 12-14pt for body text (Hebrew needs slightly larger than Latin)
- **Line height:** 1.6-1.8 for body text
- **Letter spacing:** Never add letter-spacing to Hebrew text
- **Word spacing:** 0.03-0.05em can improve readability
- **Paragraph spacing:** 1.2-1.5em between paragraphs
