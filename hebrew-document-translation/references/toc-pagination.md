# Building a Table of Contents with real, verified page numbers

Word's live `TableOfContents` field (from docx-js) is not recalculated by LibreOffice's headless
PDF conversion, which is what this environment uses to render/verify a `.docx`. If you insert a
live TOC field and convert straight to PDF for a check, it will render **blank** - that's an
artifact of the unattended conversion, not proof the field is broken, but it also means you can't
verify correctness that way. For documents with more than a handful of sections, a **static TOC
with numbers you've actually verified** is the most reliable option - it looks and works correctly
in Word, LibreOffice, and any PDF viewer, with zero dependency on the reader updating a field.

## The recipe

1. **Build the full document once**, with placeholder page numbers in the TOC (anything, e.g. all
   pointing at the same page - they just need to exist so the layout/table renders).
2. **Render it to PDF** and get the true page count:
   ```bash
   python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf draft.docx
   pdfinfo draft.pdf | grep Pages
   ```
3. **Find which page each heading/section actually starts on.** The most reliable way is to dump
   each PDF page's text separately and search for a short, unique string from each heading:
   ```python
   import subprocess, re
   n_pages = 17  # from pdfinfo above
   mapping = {}
   for i in range(1, n_pages + 1):
       out = subprocess.run(
           ['pdftotext', '-layout', '-f', str(i), '-l', str(i), 'draft.pdf', '-'],
           capture_output=True, text=True
       ).stdout
       for line in out.split('\n'):
           if 'שאלה' in line and 'נקוד' in line:   # adjust the marker text to your own heading pattern
               nums = re.findall(r'\d+', line)
               if nums:
                   qnum = int(nums[-1])
                   if qnum not in mapping:   # keep the FIRST page a heading appears on
                       mapping[qnum] = i
   print(mapping)
   ```
   Pick a marker substring that appears **only** in the heading paragraph itself (not in body text,
   option lists, or elsewhere) - e.g. a fixed label you always put in the heading, like
   `"נקודה"`/`"נקודות"` next to a question number, or a distinctive section title. Cross-check by
   printing the first ~400 characters of every page and reading through once, in case your
   substring match is too loose or too strict.
4. **Hardcode these verified numbers** into a plain two-column TOC table (title cell + page-number
   cell, right-to-left, with a dotted bottom border to mimic a leader line) - see `tocRow()` /
   `buildTocTable()` in `../scripts/rtl_docx_helpers.js`.
5. **Rebuild and re-render.** Inserting real numbers (which may have different digit counts than
   your placeholders, e.g. "7" vs "17") can occasionally nudge later content by a line. Re-run step
   3's extraction again on the new PDF and confirm the mapping is unchanged before treating the TOC
   as final. If anything shifted, update the TOC numbers again and repeat until stable (this
   converges in one or two passes in practice).

## Running header/footer page numbers are different - use live fields

Simple "page X of Y" numbers in a running footer (as opposed to a TOC) update correctly with plain
docx-js field codes in *both* Word and LibreOffice, so there's no need for the static workaround
there:
```js
new TextRun({ children: [PageNumber.CURRENT] })
new TextRun({ children: [PageNumber.TOTAL_PAGES] })
```
Only the multi-entry `TableOfContents` field is the problem case.
