import fields
from actions import ActionMeta
from openai import OpenAI
import base64
from PIL import Image, ImageDraw, ImageFont
import json
from joblib import Memory
import io
from typing import List, Dict, Union
from utils import *
import re
from pydantic import ValidationError

memory = Memory(".joblib_cache", verbose=0)

e2e_prompt_template = """Complete the attached form based on the following user profile:
        
{user_profile}

You have access to the following APIs:

{api_documentation}

Generate a sequence of actions that will fill out the form. 

Complete the form to the best of your abilites, leaving signatures blank. 
If you do not know value for a field, fill it with "[UNK]".
Fill checkboxes with a single "x".
Format all dates as "MM/DD/YYYY", including leading zeros.

{grid_subprompt}

Return a form-filling API call as a JSON list of dictionaries.
"""

grid_subprompt = "To assist you, the image has been overlaid with a 10x10 grid of red lines at intervals of 0.1 * the image width and height. This grid can be used to determine relative positions of text. Each intersection is labeled with the grid coordinates in green. Use these coordinates to help you fill out the form by interpolating between them."


def visualize_preds(doc_state, fields, img):
    # Open the image and prepare drawing context.
    """
    Visualizes prediction results on a document image by drawing text at specified coordinates.

    Parameters:
    preds (list): List of dictionaries containing predicted coordinates and value.
                  Expected keys are "x", "y", and "value", where "x" and "y" are
                  relative positions (0 to 1) and "value" is the text to be displayed.

    The function opens the specified image, calculates the absolute position for the
    text using the relative coordinates from `preds`, and draws the text centered at
    this position in blue color. The result is saved as 'output.png' in the current directory.
    """

    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))

    correctness_draw = ImageDraw.Draw(overlay)
    width, height = img.size

    # Calculate absolute coordinates.

    img = get_image_of_state(doc_state=doc_state, blank_img=img)

    # Draw correct text boxes in green and incorrect text boxes in red

    for field in fields:
        x = field["bbox"]["x"] * width
        y = field["bbox"]["y"] * height
        w = field["bbox"]["w"] * width
        h = field["bbox"]["h"] * height
        correctness_draw.rectangle(
            (x, y, x + w, y + h),
            fill=(0, 255, 0, 64) if field["correct"] else (255, 0, 0, 64),
        )
    # Save the image.
    # Combine the overlay with the base image
    result = Image.alpha_composite(img, overlay)

    result.save("output.png")


def get_image_of_state(
    doc_state, blank_img: Image.Image, save_path: str = None
) -> Image.Image:
    text_draw = ImageDraw.Draw(blank_img)
    preds = doc_state.marks
    width, height = blank_img.size

    color_map = {
        CreatorEnum.PREFILLED.value: "blue",
        CreatorEnum.AGENT.value: "green",
    }
    for pred in preds:
        x = pred["x"] * width
        y = pred["y"] * height

        # Load Times New Roman font, size 10.
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSerif.ttf", 20)
            pass
        except IOError:
            font = ImageFont.load_default()

        field_name = pred["field_name"] if "field_name" in pred else ""
        text = str(pred["value"])

        # Draw the text in blue.

        text_draw.text(
            (x, y), text, fill=color_map[pred["creator"]], font=font, anchor="mm"
        )
    # save the image
    if save_path:
        blank_img.save(save_path)
    return blank_img  # drawn on


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


def parse_and_reconstruct_fields(response_text):
    pattern = r"(\{[^}]*\})"
    matches = re.findall(pattern, response_text)

    passed_actions = []
    failed_actions = []
    for match in matches:
        try:
            match_dict = json.loads(match)
            action_name = match_dict["action"]
            action = ActionMeta.registry[action_name]
            action.Schema(**match_dict)
            passed_actions.append(match_dict)
        except ValidationError as e:
            print(f"Validation error for {match}: {e}")
            failed_actions.append(match)
    return passed_actions


class CheaterModel:
    def __init__(self, doc_state, user_profile):
        self.doc_state = doc_state
        self.user_profile = user_profile

    def forward(
        self,
        nl_profile: str,
        doc_image: Image.Image,
        available_actions: List[str],
        targets: List[str]=[],
    ) -> List[Dict]:
        """
        Give the model the ground truth annotated doc so it can cheat, for data validation
        """
        preds = []
        targets = set(targets)
        for field in self.doc_state.fields:
            if field["id"] in targets:
                continue
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
                    "action": "PlaceText",
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

    def forward(
        self,
        nl_profile: List[str],
        doc_image: List[Image.Image],
        available_actions: List[str],
        flow: List[str],
    ) -> List[Dict]:
        outputs = []
        for profile, image, action, f in zip(
            nl_profile, doc_image, available_actions, flow
        ):
            prompt = e2e_prompt_template.format(
                user_profile=profile,
                api_documentation=ActionMeta.all_documentation([action]),
                grid_subprompt=grid_subprompt if self.draw_grid else "",
            )

            if self.draw_grid:
                image = add_grid_overlay(image)

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            response = (
                forward_gpt(
                    self.model_name,
                    prompt,
                    image_b64,
                )
                .choices[0]
                .message.content
            )

            tool_params = parse_and_reconstruct_fields(response)
            if f == FlowEnum.ITERATIVE.value:
                tool_params = tool_params[:1]
            outputs.append(tool_params)
        return outputs


@memory.cache
def forward_gpt(model_name, prompt, base64_image):
    print("calling gpt uncached...")
    client = OpenAI()
    completion = client.chat.completions.create(
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
        # functions=[
        #     {
        #         "name": "extract_image_info",
        #         "description": "Writes a string `value` to the location (x, y) on the form.",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "result": {
        #                     "type": "array",
        #                     "items": {
        #                         "type": "object",
        #                         "properties": {
        #                             "action": {"type": "string"},
        #                             "x": {"type": "integer"},
        #                             "y": {"type": "integer"},
        #                             "value": {"type": "string"},
        #                         },
        #                         "required": ["x", "y", "value"],
        #                     },
        #                 }
        #             },
        #             "required": ["result"],
        #         },
        #     }
        # ],
        # function_call={"name": "extract_image_info"},
    )

    return completion
