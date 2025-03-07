import fields
from openai import OpenAI
import base64
from PIL import Image, ImageDraw, ImageFont
import json
from joblib import Memory

memory = Memory(".joblib_cache", verbose=0)


def visualize_preds(preds, doc_image_path):
    # Open the image and prepare drawing context.
    """
    Visualizes prediction results on a document image by drawing text at specified coordinates.

    Parameters:
    preds (list): List of dictionaries containing predicted coordinates and value.
                  Expected keys are "x", "y", and "value", where "x" and "y" are
                  relative positions (0 to 1) and "value" is the text to be displayed.
    doc_image_path (str): File path to the document image on which predictions are to be visualized.

    The function opens the specified image, calculates the absolute position for the
    text using the relative coordinates from `preds`, and draws the text centered at
    this position in blue color. The result is saved as 'output.png' in the current directory.
    """

    img = Image.open(doc_image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Calculate absolute coordinates.
    for pred in preds:
        x = pred["x"] * width
        y = pred["y"] * height

        # Load Times New Roman font, size 10.
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/DejaVuSerif.ttf", 30
            )  # BROKEN
            pass
        except IOError:
            font = ImageFont.load_default()

        field_name = pred["field_name"] if "field_name" in pred else ""
        text = ":\n".join([field_name, str(pred["value"])])
        text_x, text_y, text_w, text_h = font.getbbox(text)
        # Compute position so that the text is centered at (x, y)
        text_x = x - text_w / 2
        text_y = y - text_h / 2

        # Draw the text in blue.
        draw.text((text_x, text_y), text, fill="blue", font=font)
    # Save the image.
    img.save("output.png")


class CheaterModel:
    def __init__(self):
        pass

    def forward(self, user_profile, annotated_doc, doc_image_path):
        """
        Give the model the ground truth annotated doc so it can cheat, for data validation
        """
        preds = []
        for field in annotated_doc.fields:
            cheat_input = field["field"].get_profile_info(user_profile)
            field_mid_x = field["bbox"]["x"] + field["bbox"]["w"] / 2
            field_mid_y = field["bbox"]["y"] + field["bbox"]["h"] / 2
            preds.append(
                {
                    "x": field_mid_x,
                    "y": field_mid_y,
                    "field_name": field["field_name"],
                    "value": cheat_input,
                }
            )
        visualize_preds(preds, doc_image_path)
        return preds


class GptModelE2E:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.e2e_prompt = """Complete the attached form based on the following user profile:
        
{}

You have access to a form-filling API that takes input in the form {{x: float, y: float, value: str}}, which will place text on the form at the coordinate (x, y). (0,0) represents the top left corner of the form. (1,1) represents the bottom left. 

Complete the form to the best of your abiliites, leaving signatures blank. If you do not know value for a field, fill it with "[UNK]".

Fill checkboxes with a single "x".
Format all dates as "MM/DD/YYYY", including leading zeros.

Generate a form-filling API call as a JSON list of dictionaries, e.g.:

[
    {{0.1, 0.1, "John Doe"}},
    {{0.2, 0.2, "123 Main St."}},
]

"""

    def forward(self, user_profile: str, doc_image_path: str):
        # Fill in the prompt with the user profile.
        prompt = self.e2e_prompt.format(user_profile)
        # Read the image file in binary mode.
        with open(doc_image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Call the OpenAI ChatCompletion API with both text and image.
        # Note: This assumes the model supports multimodal input where an "image" key can be added.
        response = forward_gpt(
            self.model_name,
            prompt,
            base64_image,
        )
        return json.loads(response.choices[0].message.function_call.arguments)["result"]


@memory.cache
def forward_gpt(model_name, prompt, base64_image):
    print("calling gpt...")
    client = OpenAI()
    return client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        functions=[
            {
                "name": "extract_image_info",
                "description": "Writes a string `value` to the location (x, y) on the form.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "result": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "x": {"type": "integer"},
                                    "y": {"type": "integer"},
                                    "value": {"type": "string"},
                                },
                                "required": ["x", "y", "value"],
                            },
                        }
                    },
                    "required": ["result"],
                },
            }
        ],
        function_call={"name": "extract_image_info"},
    )
