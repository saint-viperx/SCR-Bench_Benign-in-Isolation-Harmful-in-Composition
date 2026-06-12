#!/usr/bin/env python3
"""
Image Generator using Google Gemini's Image Generation API

Generates branded images for blog posts, social media, and other content.
Supports multiple formats (LinkedIn, Medium, Square, Vertical).

Usage:
    python generate_image.py --prompt "Your detailed prompt" --output "filename.png"
    python generate_image.py --prompt "..." --output "name.png" --output-dir "assets/images"
    python generate_image.py --prompt "..." --output "name.png" --image-type linkedin
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from google import genai
    from PIL import Image
except ImportError as e:
    print(f"Error: Required package not found: {e}")
    print("Install dependencies with: pip install google-genai pillow")
    sys.exit(1)


# Image format specifications
IMAGE_FORMATS = {
    "linkedin": {
        "dimensions": "1200x630",
        "aspect": "16:9",
        "description": "horizontal, social sharing"
    },
    "medium": {
        "dimensions": "1200x400",
        "aspect": "3:1",
        "description": "wide banner, newsletter header"
    },
    "square": {
        "dimensions": "1080x1080",
        "aspect": "1:1",
        "description": "centered, concept card"
    },
    "vertical": {
        "dimensions": "1080x1920",
        "aspect": "9:16",
        "description": "stories, mobile-first"
    }
}


def generate_image(prompt: str, output_path: str, model: str = "gemini-2.5-flash-image") -> bool:
    """
    Generate an image using Gemini's image generation API.

    Args:
        prompt: The detailed prompt describing the desired image
        output_path: Full path where the generated image should be saved
        model: Gemini model to use (default: gemini-2.5-flash-image)

    Returns:
        bool: True if successful, False otherwise
    """
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Get an API key at: https://aistudio.google.com/apikey")
        print("Then set it with: export GEMINI_API_KEY='your-key-here'")
        return False

    try:
        # Initialize the Gemini client with API key
        client = genai.Client(api_key=api_key)

        # Generate the image
        print(f"Generating image with {model}...")
        print(f"Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Prompt: {prompt}")

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        # Extract and save the image
        if not response.parts:
            print("Error: No image data in response")
            return False

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Get the image from the first part with inline_data
        image_saved = False
        for part in response.parts:
            if part.inline_data:
                # Convert to PIL Image and save
                image = part.as_image()
                image.save(output_file)
                print(f"✓ Image saved successfully to: {output_path}")
                image_saved = True
                break

        if not image_saved:
            print("Error: Could not extract image data from response")
            return False

        return True

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate branded images using Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --prompt "Modern tech illustration..." --output header.png
  %(prog)s --prompt "..." --output hero.png --output-dir assets/images
  %(prog)s --prompt "..." --output card.png --image-type square

Image Types:
  linkedin  - 1200x630 (16:9) - Social sharing, blog headers
  medium    - 1200x400 (3:1)  - Newsletter, Substack headers
  square    - 1080x1080 (1:1) - Instagram, concept cards
  vertical  - 1080x1920 (9:16) - Stories, mobile content
        """
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Detailed prompt describing the desired image"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output filename (e.g., 'header.png')"
    )
    parser.add_argument(
        "--output-dir",
        default="assets/images",
        help="Output directory (default: assets/images)"
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash-image",
        choices=["gemini-2.5-flash-image", "gemini-3-pro-image-preview"],
        help="Gemini model to use (default: gemini-2.5-flash-image)"
    )
    parser.add_argument(
        "--image-type",
        choices=list(IMAGE_FORMATS.keys()),
        help="Image type preset (shows dimension reminder)"
    )

    args = parser.parse_args()

    # Show dimension reminder if image type specified
    if args.image_type:
        fmt = IMAGE_FORMATS[args.image_type]
        print(f"📐 Format: {args.image_type.title()}")
        print(f"   Dimensions: {fmt['dimensions']} ({fmt['aspect']})")
        print(f"   Best for: {fmt['description']}")
        print(f"   ⚠️  Make sure your prompt specifies these dimensions!\n")

    # Construct full output path
    output_dir = Path(args.output_dir)
    output_filename = Path(args.output).name  # Extract just filename
    output_path = output_dir / output_filename

    # Generate the image
    success = generate_image(args.prompt, str(output_path), args.model)

    if success:
        # Show relative path for markdown
        print(f"\nMarkdown snippet:")
        print(f"![Image]({output_path})")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
