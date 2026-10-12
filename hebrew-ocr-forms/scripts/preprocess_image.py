#!/usr/bin/env python3
"""Preprocess scanned Israeli government forms for optimal Hebrew OCR.

This script takes a scanned image of an Israeli form and applies
preprocessing steps to maximize Hebrew OCR accuracy with Tesseract:
  - Grayscale conversion
  - Deskewing (corrects rotation from scanning)
  - Denoising (non-local means) to remove scanner grain
  - Optional adaptive binarization (--binarize). Off by default: Tesseract
    binarizes internally, and on grainy scans an adaptive threshold turns the
    grain into speckle that Tesseract reads as letters.

Usage:
    python preprocess_image.py input.png output.png
    python preprocess_image.py input.jpg output.png --block-size 31 --c-value 10
    python preprocess_image.py uneven_light.jpg out.png --binarize --denoise-strength 20

Requirements:
    pip install opencv-python numpy
"""

import argparse
import sys

try:
    import cv2
    import numpy as np
except ImportError:
    print("Missing required dependencies. Install with:", file=sys.stderr)
    print("  pip install opencv-python numpy", file=sys.stderr)
    sys.exit(1)


def preprocess_for_hebrew_ocr(image_path, block_size=31, c_value=10,
                              enhance=False, denoise_strength=15,
                              binarize=False, border_margin=0, deskew=True):
    """Preprocess a scanned Israeli form for optimal Hebrew OCR.

    Args:
        image_path: Path to the scanned image file.
        block_size: Block size for adaptive thresholding (must be odd).
        c_value: Constant subtracted from adaptive threshold mean.
        enhance: If True, apply CLAHE contrast enhancement before
            binarization (helps low-quality or faded scans).
        denoise_strength: Non-local-means filter strength applied to the
            grayscale image before thresholding. 0 disables it. Adaptive
            thresholding amplifies scanner grain into speckle that Tesseract
            reads as letters, so denoise first. Use about 20 together with
            binarize=True; 10-15 is enough for grayscale output.
        binarize: If True, apply an adaptive threshold (for strongly uneven
            lighting). If False (default), return the denoised grayscale image
            and let Tesseract binarize it.
        border_margin: Pixels to crop from each edge BEFORE deskewing, so a
            dark scanner frame does not dominate the skew estimate.
        deskew: If False, skip rotation. The estimate uses all ink, so a large
            stamp or signature on a straight page can rotate it by 1-3 degrees.

    Returns:
        Preprocessed image as a numpy array (grayscale, or binary if binarize).
    """
    with open(image_path, 'rb') as fh:
        if fh.read(5) == b'%PDF-':
            raise ValueError(f"{image_path} is a PDF. Rasterize each page first "
                             "(pdftoppm -r 300 -png in.pdf page), or, if it has a "
                             "text layer, skip OCR and use pdftotext.")
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    # A full A4 page scanned at 300 DPI is 2480 x 3508 px. Much smaller usually means a
    # low-DPI scan or a phone photo; neither is corrected here (no perspective warp).
    h, w = img.shape[:2]
    if max(h, w) < 2400:
        print(f"  Warning: image is {w}x{h} px. If this is a full A4 page it is well under "
              "300 DPI; rescan at 300 DPI or use a scanner app that flattens the page.",
              file=sys.stderr)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if border_margin:
        gray = remove_borders(gray, border_margin)

    # Deskew -- Israeli forms are often slightly rotated from scanning
    if deskew:
        gray = deskew_image(gray)

    # Optional CLAHE contrast enhancement -- helps faded / low-contrast scans
    if enhance:
        gray = enhance_contrast(gray)

    if denoise_strength > 0:
        gray = cv2.fastNlMeansDenoising(gray, None, h=denoise_strength)

    if not binarize:
        return gray

    # Binarize with adaptive threshold -- handles uneven lighting
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, block_size, c_value
    )


def deskew_image(gray, max_angle=15.0):
    """Correct slight rotation in scanned documents.

    The angle is estimated from text pixels found by Otsu thresholding a
    median-blurred copy, so scanner grain does not dominate the estimate.
    Estimates beyond max_angle are treated as unreliable and ignored (a scan
    tilted that far needs manual rotation, not a silent guess).

    Args:
        gray: Grayscale image as numpy array.
        max_angle: Largest correction, in degrees, that will be applied.

    Returns:
        Deskewed grayscale image.
    """
    mask = cv2.threshold(cv2.medianBlur(gray, 5), 0, 255,
                         cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(mask > 0))
    if len(coords) < 100:
        return gray

    angle = cv2.minAreaRect(coords.astype(np.float32))[-1]
    # minAreaRect's angle convention changed in OpenCV 4.5.1; fold any value
    # into (-45, 45] so both conventions give the same small correction.
    while angle > 45:
        angle -= 90
    while angle <= -45:
        angle += 90
    angle = -angle

    if abs(angle) > max_angle:
        print(f"  Skew estimate {angle:.1f} deg is implausible, not rotating",
              file=sys.stderr)
        return gray
    if abs(angle) > 0.5:
        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        gray = cv2.warpAffine(
            gray, rotation_matrix, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

    return gray


def enhance_contrast(gray, clip_limit=2.0, tile_size=8):
    """Apply CLAHE contrast enhancement for low-quality scans.

    Args:
        gray: Grayscale image as numpy array.
        clip_limit: CLAHE clip limit.
        tile_size: CLAHE tile grid size.

    Returns:
        Contrast-enhanced grayscale image.
    """
    clahe = cv2.createCLAHE(
        clipLimit=clip_limit,
        tileGridSize=(tile_size, tile_size)
    )
    return clahe.apply(gray)


def remove_borders(binary, margin=10):
    """Remove dark borders that scanners sometimes add.

    Args:
        binary: Grayscale or binarized image as numpy array.
        margin: Pixels to crop from each edge.

    Returns:
        Border-removed image.
    """
    h, w = binary.shape[:2]
    if h > 2 * margin and w > 2 * margin:
        return binary[margin:h - margin, margin:w - margin]
    return binary


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess scanned Israeli forms for Hebrew OCR"
    )
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Path to output preprocessed image")
    parser.add_argument(
        "--block-size", type=int, default=31,
        help="Adaptive threshold block size (default: 31)"
    )
    parser.add_argument(
        "--c-value", type=int, default=10,
        help="Adaptive threshold constant (default: 10)"
    )
    parser.add_argument(
        "--enhance-contrast", action="store_true",
        help="Apply CLAHE contrast enhancement before binarization"
    )
    parser.add_argument(
        "--remove-borders", type=int, nargs='?', const=10, default=0, metavar="PX",
        help="Crop PX pixels (default 10) from each edge before deskewing, for dark scanner frames"
    )
    parser.add_argument(
        "--denoise-strength", type=int, default=15,
        help="Non-local-means denoise strength before thresholding (default 15, 0 = off)"
    )
    parser.add_argument(
        "--binarize", action="store_true",
        help="Apply adaptive thresholding (strongly uneven lighting). Off by default; "
             "pair it with --denoise-strength 20 on grainy scans"
    )
    parser.add_argument(
        "--no-deskew", action="store_true",
        help="Skip rotation (use on straight pages with large stamps or signatures)"
    )
    args = parser.parse_args()
    if args.block_size < 3 or args.block_size % 2 == 0:
        parser.error("--block-size must be an odd number >= 3")

    print(f"Preprocessing: {args.input}")

    try:
        processed = preprocess_for_hebrew_ocr(
            args.input,
            block_size=args.block_size,
            c_value=args.c_value,
            enhance=args.enhance_contrast,
            denoise_strength=args.denoise_strength,
            binarize=args.binarize,
            border_margin=args.remove_borders,
            deskew=not args.no_deskew,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if args.enhance_contrast:
        print("  Applied CLAHE contrast enhancement")
    if args.remove_borders:
        print("  Removed borders")

    cv2.imwrite(args.output, processed)
    print(f"Saved preprocessed image: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
