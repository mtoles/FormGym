import fields
from actions import ActionMeta
from openai import OpenAI
import base64
from PIL import Image, ImageDraw, ImageFont
import json
from joblib import Memory
import io
from typing import List, Dict
from utils import *

memory = Memory(".joblib_cache", verbose=0)


def construct_prompt(
    nl_profile: str, available_actions: List[str], draw_grid: bool, flow: str
) -> str:
    if flow == FlowEnum.iterative.value:
        flow_instruction = "Generate a single action that will help you fill out the first empty field in the form. If the form is already complete, use an action to mark it as complete. Do not call more than one action at a time."
        additional_instructions = ""
    elif flow == FlowEnum.full.value:
        flow_instruction = "Generate a sequence of actions that will fill out the entire form. Call multiple actions at a time if necessary."
        additional_instructions = "Complete the form to the best of your abilities, leaving signatures blank.\nIf you do not know value for a field, fill it with [UNK]."
    else:
        raise NotImplementedError

    """
    Constructs the prompt string with the necessary details.
    """
    api_documentation = ActionMeta.all_documentation(available_actions)
    grid_subprompt = (
        """
    To assist you, the image has been overlaid with a 10x10 grid of red lines at intervals of 0.1 * the image width and height. 
    This grid can be used to determine relative positions of text. Each intersection is labeled with the grid coordinates in green. 
    Use these coordinates to help you fill out the form by interpolating between them.
    """
        if draw_grid
        else ""
    )

    output = f"""Complete the attached form based on the following user profile:
    
{nl_profile}

You have access to the following APIs:

{api_documentation}

{flow_instruction}

{additional_instructions}
To fill a checkbox, place an "x" inside it.
Format all dates as "MM/DD/YYYY", including leading zeros.

{grid_subprompt}

Return a form-filling API call as a JSON list of dictionaries. 
"""

    return output


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
            font = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSerif.ttf", 20)
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
            (x, y, x + w, y + h),
            fill=(0, 255, 0, 64) if field["correct"] else (255, 0, 0, 64),
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
    def __init__(self, doc_state, user_profile):
        self.doc_state = doc_state
        self.user_profile = user_profile

    def forward(
        self, nl_profile, doc_image_path, available_actions: List[str], flow: str
    ) -> List[Dict]:
        """
        Give the model the ground truth annotated doc so it can cheat, for data validation
        """
        preds = []
        missing_attributes = []
        for field in self.doc_state.fields:
            try:
                cheat_input = field["field"].get_profile_info(self.user_profile)
            except AttributeError as e:
                print(e)
                missing_attributes.append(field["field_name"])
                cheat_input = "MISSING ATTRIBUTE"

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

        if missing_attributes:
            print(f"Missing attributes:\n{"\n".join(missing_attributes)}")
            raise ValueError("Missing attributes")
        return preds


class GptModelE2E:
    def __init__(self, model_name: str, draw_grid: bool = False):
        self.model_name = model_name
        self.draw_grid = draw_grid

    def forward(
        self,
        nl_profile: str,
        doc_image_path: str,
        available_actions: List[str],
        flow: str,
    ) -> List[Dict]:
        # Construct the prompt using the dedicated function
        prompt = construct_prompt(
            nl_profile=nl_profile,
            available_actions=available_actions,
            draw_grid=self.draw_grid,
            flow=flow,
        )

        # Read the image file in binary mode
        img = Image.open(doc_image_path)
        if self.draw_grid:
            img = add_grid_overlay(img)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Call the OpenAI ChatCompletion API with both text and image
        response = forward_gpt(
            model_name=self.model_name,
            prompt=prompt,
            base64_image=base64_image,
            flow=flow,
        )
        tool_params = [
            json.loads(tc.function.arguments)
            for tc in response.choices[0].message.tool_calls
        ]  # [0]["result"]
        if flow == FlowEnum.iterative.value:
            tool_params = tool_params[0]
        print(tool_params)
        # raise NotImplementedError
        tool_params = [tp["result"] for tp in tool_params]
        return tool_params


# [json.loads(tc.function.arguments) for tc in response.choices[0].message.tool_calls for x in tc]


@memory.cache
def forward_gpt(model_name, prompt, base64_image, flow: str):
    print("calling gpt uncached...")
    client = OpenAI()
    single_call = flow == FlowEnum.full.value
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "write_string_on_image",
                    "description": "Writes a string `value` to the location (x, y) on the form.",
                    "strict": True,
                    # "parallel_tool_calls": parallel_tool_calls,
                    "parallel_tool_calls": False,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "result": {
                                # "type": "array" if parallel_tool_calls else "object",
                                "type": "object",
                                # "items": {
                                #     "type": "object",
                                "properties": {
                                    "action": {"type": "string"},
                                    "x": {"type": "integer"},
                                    "y": {"type": "integer"},
                                    "value": {"type": "string"},
                                },
                                "required": ["x", "y", "action", "value"],
                                "additionalProperties": False,
                                # },
                                # "additionalProperties": False,
                            }
                        },
                        "required": ["result"],
                        "additionalProperties": False,
                    },
                },
            }
        ],
        # function_call={"name": "write_string_on_image"},
    )
    return completion
