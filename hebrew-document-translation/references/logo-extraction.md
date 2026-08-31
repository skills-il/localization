# Extracting a logo/brand asset from a reference PDF

When a user wants a new translation to reuse the same branding as an existing PDF (their own
document, a previous translation, a company template), pull the actual embedded image out of the
PDF rather than recreating it - it'll be pixel-identical and saves a lot of guessing.

## 1. Extract all images from the relevant page

```bash
mkdir -p assets
pdfimages -all -f 1 -l 1 "/path/to/reference.pdf" assets/page1
```
```python
from PIL import Image
import glob
for path in sorted(glob.glob('assets/page1-*.png')):
    with Image.open(path) as im:
        print(path, im.mode, im.size)
```

`-all` preserves native format (usually gives you real `.png` files directly). If you only get
`.ppm` files, re-run with `-all` - plain `pdfimages` without flags sometimes falls back to a lossy
raw dump.

## 2. Recover transparency, if the logo looks wrong (solid black background, wrong colors)

PDFs often store a transparent logo as **two separate images**: a plain RGB color image, and a
separate grayscale image that's actually the alpha/soft mask. If the Pillow inspection above shows
two same-sized images where one is mode `RGB` and the other is `L` (grayscale), they're very likely
the base image + its mask. Recombine them:

```python
from PIL import Image
base = Image.open('assets/page1-000.png').convert('RGB')   # the color image
mask = Image.open('assets/page1-001.png').convert('L')      # the alpha mask
rgba = base.copy()
rgba.putalpha(mask)
rgba.save('assets/logo_transparent.png')
```

Then, since docx-js embeds images without needing transparency handling logic on your part, flatten
onto white for safe, predictable rendering in the Word doc:

```python
from PIL import Image
im = Image.open('assets/logo_transparent.png')
bg = Image.new('RGB', im.size, (255, 255, 255))
bg.paste(im, mask=im.split()[3])
bg.save('assets/logo_white.png')
```

## 3. Confirm you found the right image (not a background/watermark)

Check dominant colors - a real logo usually has 2-4 saturated brand colors plus white/transparent,
not a single flat color:

```python
from PIL import Image
im = Image.open('assets/logo_white.png').convert('RGB')
colors = im.getcolors(maxcolors=1000000)
colors.sort(reverse=True)
print(im.size, colors[:5])
```

If a page embeds the same image more than once (e.g. once large on the cover, once small in the
running header of every subsequent page - check by comparing file size/bytes across pages), that
confirms it's the single reusable logo asset; you don't need to hunt for a separate small icon.

## 4. Auto-crop excess whitespace

```python
from PIL import Image, ImageChops
im = Image.open('assets/logo_white.png').convert('RGB')
bg = Image.new('RGB', im.size, (255, 255, 255))
diff = ImageChops.difference(im, bg)
bbox = diff.getbbox()
if bbox:
    im.crop(bbox).save('assets/logo_final.png')
```

## 5. Extract brand colors for headings/titles

Reuse the exact hex values found in step 3 (e.g. the dominant non-white/non-black color) for
heading and title colors in the new document, rather than eyeballing a similar shade - see the
`BRAND_BLUE` constant in `../scripts/rtl_docx_helpers.js`.

## 6. Use the asset

Reference the final PNG path from `ImageRun` in the docx build script (see `logoImage()` in
`../scripts/rtl_docx_helpers.js`), sized smaller for the running header and larger for the cover
page, using the same aspect ratio (the `im.size` values printed by Pillow in step 1).
