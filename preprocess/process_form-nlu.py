"""
Form-NLU pngs are available in the `annotations/form-nlu/images` directory.
We need to extract key-value pairs from the images of the financial documents.
Use the GPT-5 model to extract the key-value pairs.
"""

import os
import json
import base64
from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI()
from PIL import Image
import io
import time
from tqdm import tqdm

# Configuration
IMAGES_DIR = "annotations/form-nlu/images"
OUTPUT_DIR = "tool/dataset/form-nlu"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"
# MODEL_NAME = "gpt-5-mini"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def encode_image_to_base64(image_path: str) -> str:
    """Encode image to base64 string for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_kv_pairs_with_gpt5(image_path: str) -> List[Dict[str, str]]:
    """Extract key-value pairs from an image using GPT-5 Vision."""

    # Encode image
    base64_image = encode_image_to_base64(image_path)

    # System prompt for extraction
    system_prompt = """You are an expert at extracting key-value pairs from financial documents. 
    
    Keys are text written by the creator of the form indicating information to be filled in.
    Values are the text written by the user filling in the form.
    Not all values may be present in the form if it is incomplete.
    "section" indicates the header of the section a KV pair belongs to.

    There are two types of KV pairs.

    Pairs written in text, paragraphs, or on lines should include the section, key, value:


    {
        "section": "section1",
        "key": "key1",
        "value": "value1",
    },


    For table pairs, extract the section, row, column and value. Do not include a key:

    {
        "section": "section1",
        "row": "row1",
        "column": "column1",
        "value": "value1",
    },

    DO NOT include any row or column headers as values.
    DO NOT include any non-header cells as keys.
    If there is no row or column header, use the number of the row or column, starting from 1, including any header(s).
    
    Return ONLY a JSON array of objects with this exact format:
    [
        {
            "section": "section1",
            "key": "key1",
            "value": "value1",
        },
        ...
        {
            "section": "section2",
            "row": "row_header",
            "column": "column_header",
            "value": "value2",
        },
        ...
    ]
    
    """

    # User prompt
    user_prompt = "Please extract all key-value pairs from this financial document image. Return only the JSON array."

    try:
        for attempt in range(5):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                },
                            },
                        ],
                    },
                ],
            )

            # Extract the response content
            content = response.choices[0].message.content

            # Find JSON array in the response
            start_idx = content.find("[")
            end_idx = content.rfind("]") + 1

            if start_idx == -1 or end_idx <= 0:
                if attempt < 4:
                    time.sleep(0.5)
                    continue
                raise ValueError(
                    f"No JSON array found in response after 5 attempts: {content}"
                )

            json_str = content[start_idx:end_idx]

            try:
                kv_pairs = json.loads(json_str)
            except json.JSONDecodeError as e:
                if attempt < 4:
                    time.sleep(0.5)
                    continue
                raise ValueError(
                    f"Failed to parse JSON response after 5 attempts: {e}. Response content: {content}"
                )

            # Validate the structure
            if isinstance(kv_pairs, list):
                validated_pairs = []
                for pair in kv_pairs:
                    if isinstance(pair, dict) and "value" in pair:
                        # Validate required fields based on structure
                        if "key" in pair:
                            # Key-value pair: has key and value
                            if not isinstance(pair["key"], str):
                                raise ValueError(
                                    f"Key must be a string, got {type(pair['key']).__name__}: {pair['key']}"
                                )
                        elif "row" in pair and "column" in pair:
                            # Table pair: has row, column, value
                            if not isinstance(pair["row"], str):
                                raise ValueError(
                                    f"Row must be a string, got {type(pair['row']).__name__}: {pair['row']}"
                                )
                            if not isinstance(pair["column"], str):
                                raise ValueError(
                                    f"Column must be a string, got {type(pair['column']).__name__}: {pair['column']}"
                                )
                        else:
                            raise ValueError(
                                f"Invalid pair structure. Must have either (key+value) or (row+column+value): {pair}"
                            )

                        # Validate value is a string
                        if not isinstance(pair["value"], str):
                            raise ValueError(
                                f"Value must be a string, got {type(pair['value']).__name__}: {pair['value']}"
                            )

                        validated_pairs.append(pair)
                return validated_pairs
            else:
                raise ValueError(f"Response is not a list: {content}")

    except Exception as e:
        if "OpenAI API" in str(e):
            raise RuntimeError(f"OpenAI API error: {e}")
        raise


def process_single_image(image_path: str) -> Dict[str, Any]:
    """Process a single image and return the extracted data."""
    print(f"Processing: {image_path}")

    # Extract key-value pairs
    kv_pairs = extract_kv_pairs_with_gpt5(image_path)

    return {"kv_pairs": kv_pairs}


def save_to_jsonl(data: Dict[str, Any], output_path: str):
    """Save data to JSONL format with one kv pair per line."""
    # Validate data structure before saving
    if "kv_pairs" not in data:
        raise ValueError("Data missing 'kv_pairs' field")
    if not isinstance(data["kv_pairs"], list):
        raise ValueError("'kv_pairs' must be a list")

    with open(output_path, "w", encoding="utf-8") as f:

        # Write each kv pair on a separate line
        for kv_pair in data["kv_pairs"]:
            # Validate kv_pair structure
            if not isinstance(kv_pair, dict):
                raise ValueError(
                    f"Each kv_pair must be a dict, got {type(kv_pair).__name__}"
                )
            if "value" not in kv_pair:
                raise ValueError(f"Each kv_pair must have 'value' field: {kv_pair}")

            # Validate based on structure
            if "key" in kv_pair:
                # Key-value pair: has key and value
                if not isinstance(kv_pair["key"], str):
                    raise ValueError(f"Key must be a string: {kv_pair}")
            elif "row" in kv_pair and "column" in kv_pair:
                # Table pair: has row, column, value
                if not isinstance(kv_pair["row"], str) or not isinstance(
                    kv_pair["column"], str
                ):
                    raise ValueError(f"Row and column must be strings: {kv_pair}")
            else:
                raise ValueError(
                    f"Invalid pair structure. Must have either (key+value) or (row+column+value): {kv_pair}"
                )

            if not isinstance(kv_pair["value"], str):
                raise ValueError(f"Value must be a string: {kv_pair}")

            json.dump(kv_pair, f, ensure_ascii=False)
            f.write("\n")


def main():
    """Main processing function."""
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        return

    # Get list of PNG images
    image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(".png")]

    if not image_files:
        print(f"No PNG files found in {IMAGES_DIR}")
        return

    print(f"Found {len(image_files)} PNG files to process")

    # Process each image
    for i, image_file in enumerate(tqdm(image_files, desc="Processing images")):
        # Determine output path for this image and skip if it already exists
        base_name = os.path.splitext(image_file)[0]
        output_filename = f"{base_name}_synthetic.jsonl"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        if os.path.exists(output_path):
            print(f"Skipping {image_file}: {output_filename} already exists")
            continue

        image_path = os.path.join(IMAGES_DIR, image_file)

        # Process the image
        result = process_single_image(image_path)

        # Save to JSONL (one kv pair per line)
        save_to_jsonl(result, output_path)

        print(
            f"Saved: {output_filename} with {len(result['kv_pairs'])} key-value pairs (JSONL format)"
        )

        # Add delay to avoid rate limiting
        if i < len(image_files) - 1:  # Don't delay after the last image
            time.sleep(1)

    print(f"\nProcessing complete! Results saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
