#!/usr/bin/env python3
"""Generate images using Gemini/Imagen API.

Usage:
    python generate_image.py "A futuristic city at sunset"
    python generate_image.py "Robot with skateboard" --model imagen-4.0-generate-001
    python generate_image.py "Mountain landscape" --aspect 16:9 --size 2K
    python generate_image.py "Portrait" --num 4 --output-dir ./my-images/ --name portrait
    python generate_image.py "Custom folder" --no-timestamp

Requirements:
    pip install google-genai pillow
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

# Load .env file if present
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def get_client():
    """Get Gemini API client."""
    try:
        from google import genai
    except ImportError:
        print("Error: google-genai not installed. Run: pip install google-genai")
        sys.exit(1)

    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        sys.exit(1)

    return genai.Client(api_key=api_key)


def generate_image(
    prompt: str,
    model: str = "imagen-4.0-generate-001",
    output_dir: str = "images/",
    output_name: str = "generated_image",
    aspect_ratio: str = "1:1",
    image_size: str = "1K",
    num_images: int = 1,
    person_generation: str = "allow_adult",
    use_timestamp: bool = True,
) -> list[str]:
    """Generate images using Imagen or Gemini models.

    Args:
        prompt: Text description of the image
        model: Model ID (imagen-4.0-generate-001, gemini-3-pro-image-preview)
        output_dir: Directory to save images
        output_name: Base name for output files
        aspect_ratio: Aspect ratio (1:1, 16:9, 9:16, etc.)
        image_size: Resolution (1K, 2K, 4K for gemini-3-pro)
        num_images: Number of images to generate (1-4)
        person_generation: Person policy (dont_allow, allow_adult, allow_all)
        use_timestamp: Add timestamp to filename

    Returns:
        List of saved file paths
    """
    from google.genai import types

    client = get_client()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files = []

    if use_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{output_name}_{timestamp}"
    else:
        base_filename = output_name

    if model.startswith("imagen"):
        # Use Imagen API
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=num_images,
                aspect_ratio=aspect_ratio,
                image_size=image_size,
                person_generation=person_generation,
            ),
        )

        for i, generated_image in enumerate(response.generated_images):
            suffix = f"_{i}" if num_images > 1 else ""
            filename = output_path / f"{base_filename}{suffix}.png"
            with open(filename, "wb") as f:
                f.write(generated_image.image.image_bytes)
            saved_files.append(str(filename))
            print(f"Saved: {filename}")

    elif model.startswith("gemini"):
        # Use Gemini generateContent API for image generation
        config = types.GenerateContentConfig(
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            )
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

        if response.candidates and response.candidates[0].content.parts:
            for i, part in enumerate(response.candidates[0].content.parts):
                if hasattr(part, "inline_data") and part.inline_data:
                    suffix = (
                        f"_{i}" if len(response.candidates[0].content.parts) > 1 else ""
                    )
                    filename = output_path / f"{base_filename}{suffix}.png"

                    import base64

                    image_data = part.inline_data.data
                    if isinstance(image_data, str):
                        image_data = base64.b64decode(image_data)

                    with open(filename, "wb") as f:
                        f.write(image_data)
                    saved_files.append(str(filename))
                    print(f"Saved: {filename}")
    else:
        print(f"Error: Unknown model {model}")
        sys.exit(1)

    return saved_files


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini/Imagen API"
    )
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument(
        "--model",
        "-m",
        default="gemini-3-pro-image-preview",
        help="Model ID (default: gemini-3-pro-image-preview). Options: gemini-3-pro-image-preview, gemini-2.5-flash-image, imagen-4.0-generate-001",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="images/",
        help="Output directory for images (default: images/)",
    )
    parser.add_argument(
        "--name",
        "-n",
        default="generated_image",
        help="Base name for output files (default: generated_image). Timestamp will be appended automatically",
    )
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Disable automatic timestamp in filename",
    )
    parser.add_argument(
        "--aspect",
        "-a",
        default="1:1",
        help="Aspect ratio (default: 1:1). Options: 1:1, 3:4, 4:3, 9:16, 16:9, 21:9",
    )
    parser.add_argument(
        "--size",
        "-s",
        default="1K",
        help="Image size (default: 1K). Options: 1K, 2K, 4K (4K only for gemini-3-pro)",
    )
    parser.add_argument(
        "--num",
        type=int,
        default=1,
        help="Number of images to generate (1-4, default: 1)",
    )
    parser.add_argument(
        "--person",
        default="allow_adult",
        choices=["dont_allow", "allow_adult", "allow_all"],
        help="Person generation policy (default: allow_adult)",
    )

    args = parser.parse_args()

    try:
        files = generate_image(
            prompt=args.prompt,
            model=args.model,
            output_dir=args.output_dir,
            output_name=args.name,
            aspect_ratio=args.aspect,
            image_size=args.size,
            num_images=args.num,
            person_generation=args.person,
            use_timestamp=not args.no_timestamp,
        )
        print(f"\nGenerated {len(files)} image(s)")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
