#!/usr/bin/env python3
"""Preprocess scanned Israeli government forms for optimal Hebrew OCR.

This script takes a scanned image of an Israeli form and applies
preprocessing steps to maximize Hebrew OCR accuracy with Tesseract:
  - Grayscale conversion
  - Deskewing (corrects rotation from scanning)
  - Adaptive binarization (handles uneven lighting)
  - Noise removal via morphological operations

Usage:
    python preprocess_image.py input.png output.png
    python preprocess_image.py input.jpg output.png --block-size 31 --c-value 10

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


def preprocess_for_hebrew_ocr(image_path, block_size=31, c_value=10):
    """Preprocess a scanned Israeli form for optimal Hebrew OCR.

    Args:
        image_path: Path to the scanned image file.
        block_size: Block size for adaptive thresholding (must be odd).
        c_value: Constant subtracted from adaptive threshold mean.

    Returns:
        Preprocessed image as a numpy array (grayscale, binarized).
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Deskew -- Israeli forms are often slightly rotated from scanning
    gray = deskew_image(gray)

    # Binarize with adaptive threshold -- handles uneven lighting
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, block_size, c_value
    )

    # Remove noise with morphological close operation
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return cleaned


def deskew_image(gray):
    """Correct slight rotation in scanned documents.

    Args:
        gray: Grayscale image as numpy array.

    Returns:
        Deskewed grayscale image.
    """
    coords = np.column_stack(np.where(gray < 128))
    if len(coords) < 100:
        return gray

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

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
        binary: Binarized image as numpy array.
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
        "--remove-borders", action="store_true",
        help="Remove dark scanner borders"
    )
    args = parser.parse_args()

    print(f"Preprocessing: {args.input}")

    processed = preprocess_for_hebrew_ocr(
        args.input,
        block_size=args.block_size,
        c_value=args.c_value
    )

    if args.remove_borders:
        processed = remove_borders(processed)
        print("  Removed borders")

    cv2.imwrite(args.output, processed)
    print(f"Saved preprocessed image: {args.output}")


if __name__ == "__main__":
    main()
