import fields
from openai import OpenAI
import base64
from PIL import Image, ImageDraw, ImageFont
import json
from joblib import Memory
import io

memory = Memory(".joblib_cache", verbose=0)

e2e_prompt_template = """Complete the attached form based on the following user profile:
        
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

{}
"""

grid_subprompt = "To assist you, the image has been overlaid with a 10x10 grid of red lines at intervals of 0.1 * the image width and height. This grid can be used to determine relative positions of text. Each intersection is labeled with the grid coordinates in green. Use these coordinates to help you fill out the form by interpolating between them."
def visualize_preds(preds, fields, doc_image_path):
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

    img = Image.open(doc_image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))

    correctness_draw = ImageDraw.Draw(overlay)
    text_draw = ImageDraw.Draw(img)
    width, height = img.size

    # Calculate absolute coordinates.
    for pred in preds:
        x = pred["x"] * width
        y = pred["y"] * height

        # Load Times New Roman font, size 10.
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/DejaVuSerif.ttf", 20
            )  # BROKEN
            pass
        except IOError:
            font = ImageFont.load_default()

        field_name = pred["field_name"] if "field_name" in pred else ""
        text = str(pred["value"])
        # text = ":\n".join([field_name, str(pred["value"])])
        # text = "x"

        # text_l, text_t, text_, text_h = font.getbbox(text)
        # Compute position so that the text is centered at (x, y)
        # text_x = x + text_w / 2
        # text_y = y + text_h / 2

        # Draw the text in blue.
        text_draw.text((x, y), text, fill="blue", font=font, anchor="mm")
    # Draw correct text boxes in green and incorrect text boxes in red

    for field in fields:
        x = field["bbox"]["x"] * width
        y = field["bbox"]["y"] * height
        w = field["bbox"]["w"] * width
        h = field["bbox"]["h"] * height
        correctness_draw.rectangle(
            (x, y, x + w, y + h), fill=(0, 255, 0, 64) if field["correct"] else (255, 0, 0, 64)
        )
    # Save the image.
    # Combine the overlay with the base image
    result = Image.alpha_composite(img, overlay)

    result.save("output.png")


def add_grid_overlay(img):
    """
    Add a 10x10 grid overlay to an image with coordinates and dots at intersections.

    Args:
        img (PIL.Image.Image): The image to which the grid overlay will be added.

    Returns:
        PIL.Image.Image: The image with the grid overlay.
    """
    # Ensure the image is in RGB mode
    if img.mode != "RGB":
        img = img.convert("RGB")

    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Calculate grid spacing
    x_spacing = width / 10
    y_spacing = height / 10

    # Draw vertical and horizontal grid lines
    for i in range(11):
        # Calculate x position for vertical lines
        x = i * x_spacing
        # Draw vertical line
        draw.line([(x, 0), (x, height)], fill="red", width=2)

        # Calculate y position for horizontal lines
        y = i * y_spacing
        # Draw horizontal line
        draw.line([(0, y), (width, y)], fill="red", width=2)

        # Add dots and coordinates at intersections
        for j in range(11):
            # Recalculate positions for intersections
            x = i * x_spacing
            y = j * y_spacing
            # Draw a filled circle (dot) at the intersection
            dot_radius = 5
            draw.ellipse(
                [(x - dot_radius, y - dot_radius), (x + dot_radius, y + dot_radius)],
                fill="blue",
            )

            # Add coordinate text near the intersection, if within grid bounds
            if i < 10 and j < 10:
                coord_x = round(i / 10, 1)
                coord_y = round(j / 10, 1)
                text = f"({coord_x}, {coord_y})"
                # Position text slightly offset from the intersection for visibility
                draw.text((x + 10, y + 10), text, fill="green")

    return img


class CheaterModel:
    def __init__(self, doc, user_profile):
        self.doc = doc
        self.user_profile = user_profile

    def forward(self, nl_profile, doc_image_path):
        """
        Give the model the ground truth annotated doc so it can cheat, for data validation
        """
        preds = []
        for field in self.doc.fields:
            cheat_input = field["field"].get_profile_info(self.user_profile)
            if cheat_input == True:
                cheat_input = "x"
            elif cheat_input == False:
                cheat_input = ""
            else:
                pass
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
        return preds


class GptModelE2E:
    def __init__(self, model_name: str, draw_grid: bool = False):
        self.model_name = model_name
        self.draw_grid = draw_grid

    def forward(self, nl_profile: str, doc_image_path: str):
        # Fill in the prompt with the user profile.
        prompt = e2e_prompt_template.format(nl_profile, grid_subprompt if self.draw_grid else "")
        # Read the image file in binary mode.
        img = Image.open(doc_image_path)
        if self.draw_grid:
            img = Image.open(doc_image_path)
            img = add_grid_overlay(img)

        with open(doc_image_path, "rb") as image_file:
            # base64_image = base64.b64encode(image_file.read()).decode("utf-8") # rewrite this line
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
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
    print("calling gpt uncached...")
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
