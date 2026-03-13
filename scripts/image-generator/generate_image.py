#!/usr/bin/env python3
"""Generate images via OpenRouter API using Gemini image generation models."""

import argparse
import base64
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv
import os


OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-3.1-flash-image-preview"


def find_env_file(start_dir: Path) -> Path | None:
    """Walk up from start_dir to find a .env file."""
    current = start_dir.resolve()
    for _ in range(10):  # limit traversal depth
        env_path = current / ".env"
        if env_path.is_file():
            return env_path
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def parse_image_size(size_str: str) -> tuple[str, str]:
    """Parse image size string like '1024x1024' or '1K' into width/height."""
    presets = {
        "1K": ("1024", "1024"),
        "2K": ("2048", "2048"),
        "512": ("512", "512"),
    }
    if size_str.upper() in presets:
        return presets[size_str.upper()]
    if "x" in size_str.lower():
        parts = size_str.lower().split("x")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return (parts[0], parts[1])
    print(f"Warning: unrecognized size '{size_str}', using 1024x1024", file=sys.stderr)
    return ("1024", "1024")


def build_aspect_ratio_instruction(aspect_ratio: str) -> str:
    """Build an instruction string for the desired aspect ratio."""
    if aspect_ratio == "1:1":
        return ""
    return f" The image should have a {aspect_ratio} aspect ratio."


def generate_image(
    prompt: str,
    output_path: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = "1:1",
    image_size: str = "1K",
) -> None:
    """Call OpenRouter API to generate an image and save it."""
    width, height = parse_image_size(image_size)
    aspect_instruction = build_aspect_ratio_instruction(aspect_ratio)

    full_prompt = f"{prompt}{aspect_instruction}"

    payload = {
        "model": model,
        "modalities": ["image", "text"],
        "messages": [
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
        "provider": {
            "sort": "throughput",
        },
    }

    # Add image_config if non-default aspect ratio
    if aspect_ratio != "1:1":
        payload["image_config"] = {"aspect_ratio": aspect_ratio}


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://hjnnjh.github.io/Agents-are-the-future-of-academic-research/",
        "X-Title": "Blog Image Generator",
    }

    print(f"Model: {model}")
    print(f"Prompt: {full_prompt}")
    print(f"Target size: {width}x{height}")
    print(f"Output: {output_path}")
    print("Generating image...")

    with httpx.Client(timeout=180.0) as client:
        response = client.post(OPENROUTER_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"API error (HTTP {response.status_code}):", file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)

    data = response.json()

    # Check for API-level errors
    if "error" in data:
        print(f"API error: {data['error']}", file=sys.stderr)
        sys.exit(1)

    # Extract image from response
    image_data = None
    choices = data.get("choices", [])
    for choice in choices:
        message = choice.get("message", {})

        # Check for images in the dedicated "images" field
        images = message.get("images", [])
        for img in images:
            if isinstance(img, dict):
                url = ""
                if img.get("type") == "image_url":
                    url = img.get("image_url", {}).get("url", "")
                elif "url" in img:
                    url = img["url"]
                if url.startswith("data:"):
                    _, encoded = url.split(",", 1)
                    image_data = base64.b64decode(encoded)
                    break
                elif url.startswith("http"):
                    print("Downloading image from URL...")
                    with httpx.Client(timeout=60.0) as dl_client:
                        img_resp = dl_client.get(url)
                        if img_resp.status_code == 200:
                            image_data = img_resp.content
                    break
        if image_data:
            break

        # Fallback: check content array for image parts
        content = message.get("content", [])
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:"):
                        _, encoded = url.split(",", 1)
                        image_data = base64.b64decode(encoded)
                        break
                    elif url.startswith("http"):
                        print("Downloading image from URL...")
                        with httpx.Client(timeout=60.0) as dl_client:
                            img_resp = dl_client.get(url)
                            if img_resp.status_code == 200:
                                image_data = img_resp.content
                        break
                elif isinstance(part, dict) and part.get("type") == "inline_data":
                    image_data = base64.b64decode(part.get("data", ""))
                    break
        if image_data:
            break

    if not image_data:
        print("No image found in API response.", file=sys.stderr)
        print("Response:", file=sys.stderr)
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False)[:2000], file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(image_data)

    print(f"Image saved to {out} ({len(image_data)} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate images via OpenRouter API (Gemini)",
    )
    parser.add_argument("--prompt", required=True, help="Image generation prompt (English recommended)")
    parser.add_argument("--output", required=True, help="Output file path (e.g. docs/public/img/logo.png)")
    parser.add_argument("--aspect-ratio", default="1:1", help="Aspect ratio (default: 1:1, e.g. 16:9, 4:3)")
    parser.add_argument("--image-size", default="1K", help="Image size (default: 1K, e.g. 512, 1K, 2K, 1024x768)")
    parser.add_argument("--env-file", default=None, help="Path to .env file (auto-detected if not specified)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")

    args = parser.parse_args()

    # Load .env
    if args.env_file:
        env_path = Path(args.env_file)
        if not env_path.is_file():
            print(f"Error: specified .env file not found: {args.env_file}", file=sys.stderr)
            sys.exit(1)
        load_dotenv(env_path)
    else:
        env_path = find_env_file(Path(__file__).parent)
        if env_path:
            load_dotenv(env_path)
            print(f"Loaded .env from {env_path}")
        else:
            print("Warning: no .env file found, relying on environment variables", file=sys.stderr)

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key or api_key == "sk-or-v1-your-key-here":
        print("Error: OPENROUTER_API_KEY not set or still placeholder.", file=sys.stderr)
        print("Please set it in your .env file or environment.", file=sys.stderr)
        sys.exit(1)

    generate_image(
        prompt=args.prompt,
        output_path=args.output,
        api_key=api_key,
        model=args.model,
        aspect_ratio=args.aspect_ratio,
        image_size=args.image_size,
    )


if __name__ == "__main__":
    main()
