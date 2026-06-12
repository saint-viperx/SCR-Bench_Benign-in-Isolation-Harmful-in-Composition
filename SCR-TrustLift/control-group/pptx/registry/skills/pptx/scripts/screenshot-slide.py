#!/usr/bin/env python3
"""Generate high-resolution screenshot of a single PPTX slide.

This script provides higher resolution output than the grid-based thumbnail.py,
making it suitable for detailed validation of individual slides.

Usage:
    python screenshot-slide.py input.pptx output.jpg [--slide 0] [--dpi 200]

Examples:
    # Screenshot of first slide at default 200 DPI
    python screenshot-slide.py presentation.pptx slide-0.jpg

    # Screenshot of third slide (0-indexed) at 300 DPI
    python screenshot-slide.py presentation.pptx slide-2.jpg --slide 2 --dpi 300

    # Save to specific directory
    python screenshot-slide.py presentation.pptx workspace/slide-0.jpg --slide 0
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def screenshot_slide(pptx_path: str, output_path: str, slide_index: int = 0, dpi: int = 200):
    """
    Generate a high-resolution screenshot of a single slide.

    Args:
        pptx_path: Path to PPTX file
        output_path: Output image path (jpg/png)
        slide_index: 0-based slide index
        dpi: Resolution (default 200 for clear viewing)
    """
    pptx_path = Path(pptx_path).resolve()
    output_path = Path(output_path).resolve()

    if not pptx_path.exists():
        print(f"Error: Input file not found: {pptx_path}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine output format from extension
    ext = output_path.suffix.lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        print(f"Error: Output format must be .jpg, .jpeg, or .png (got {ext})", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Convert PPTX to PDF using LibreOffice
        try:
            subprocess.run([
                'soffice', '--headless', '--convert-to', 'pdf',
                '--outdir', str(tmpdir), str(pptx_path)
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting to PDF: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: LibreOffice (soffice) not found. Please install LibreOffice.", file=sys.stderr)
            sys.exit(1)

        pdf_path = tmpdir / (pptx_path.stem + '.pdf')
        if not pdf_path.exists():
            print(f"Error: PDF conversion failed - output file not found", file=sys.stderr)
            sys.exit(1)

        # Convert specific page to image at high DPI using pdftoppm
        # Page numbers are 1-indexed for pdftoppm
        page_num = slide_index + 1
        output_prefix = tmpdir / 'slide'

        try:
            # Determine format flag for pdftoppm
            if ext in ['.jpg', '.jpeg']:
                fmt_flag = '-jpeg'
            else:
                fmt_flag = '-png'

            subprocess.run([
                'pdftoppm', fmt_flag, '-r', str(dpi),
                '-f', str(page_num), '-l', str(page_num),
                str(pdf_path), str(output_prefix)
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting PDF to image: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: pdftoppm not found. Please install Poppler.", file=sys.stderr)
            sys.exit(1)

        # Find the generated image (pdftoppm adds page number suffix)
        pattern = f'slide-*.{ext[1:]}' if ext in ['.jpg', '.jpeg'] else 'slide-*.png'
        results = list(tmpdir.glob('slide-*'))
        if not results:
            print(f"Error: No output image generated. Slide index {slide_index} may be out of range.", file=sys.stderr)
            sys.exit(1)

        result_file = results[0]

        # Move result to output path
        import shutil
        shutil.move(str(result_file), str(output_path))

    print(f'Screenshot saved: {output_path}')
    print(f'  Slide: {slide_index} (0-indexed)')
    print(f'  DPI: {dpi}')


def main():
    parser = argparse.ArgumentParser(
        description='Generate high-resolution screenshot of a single PPTX slide.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s presentation.pptx slide-0.jpg
    %(prog)s presentation.pptx slide-2.jpg --slide 2 --dpi 300
    %(prog)s presentation.pptx workspace/slide.png --slide 0
        """
    )
    parser.add_argument('input', help='Input PPTX file')
    parser.add_argument('output', help='Output image path (.jpg or .png)')
    parser.add_argument('--slide', type=int, default=0,
                        help='Slide index (0-based, default: 0)')
    parser.add_argument('--dpi', type=int, default=200,
                        help='Resolution in DPI (default: 200)')

    args = parser.parse_args()
    screenshot_slide(args.input, args.output, args.slide, args.dpi)


if __name__ == '__main__':
    main()
