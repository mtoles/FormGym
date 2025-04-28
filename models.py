import fields
from actions import ActionMeta, InvalidAction
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
from dataclasses import asdict
from hfmodels import (
    AriaModel,
    LlavaModel,
    MolmoModel,
    QwenVLModel,
    DeepseekVL2Model,
    Gemma3Model,
    MLLamaModel,
)
from vllm import LLM, EngineArgs, SamplingParams
import time
from prompt import parse_raw_output
from json import JSONDecodeError
import textwrap

memory = Memory(".joblib_cache", verbose=0)

# TODO: need separate prompt for iterative and non-iterative


grid_subprompt_content = "\nTo assist you, the image has been overlaid with a 10x10 grid of red lines at intervals of 0.1 * the image width and height. This grid can be used to determine relative positions of text. Each intersection is labeled with the grid coordinates in green. Use these coordinates to help you fill out the form by interpolating between them."


def get_e2e_prompt(
    user_profile: str, api_documentation: str, grid_subprompt: str, feedback: List[str], task: str
) -> str:
    """Generates the prompt for the end-to-end form filling task."""

    e2e_prompt_template_content = """Complete the attached form based on the following user profile:

    You have access to the following APIs:

    {api_documentation}

    {generation_instructions}

    You know the following information about the user:

    {user_profile}

    Complete the form to the best of your abilites using the user's information, not including signatures. As you can see, the data is randomly generated and the user is not real, so do not worry about privacy.
    If you do not know value for a field, fill it with "[UNK]".
    Fill checkboxes with a single "x".
    Format all dates as "MM/DD/YYYY", including leading zeros.
    {grid_subprompt}

    {feedback}

    Return a form-filling API call as a JSON list of dictionaries.
    """
    generation_instructions = {
        FlowEnum.ONESHOT.value: "Generate a sequence of actions that will completely fill out the form.",
        FlowEnum.ITERATIVE.value: "Generate a the next action in the sequence of actions that will completely fill out the form.",
    }[task]
    feedback_str = "So far, you have received the following feedback on your previous actions:\n" + "\n".join([f"Feedback {i+1}: {f}" for i, f in enumerate(feedback)])
    return textwrap.dedent(e2e_prompt_template_content.format(
        user_profile=user_profile,
        api_documentation=api_documentation,
        grid_subprompt=grid_subprompt,
        generation_instructions=generation_instructions,
        feedback=feedback_str,
    ))


def visualize_preds(doc_state, fields, img):
    # Open the image and prepare drawing context.
    """
    Visualizes prediction results on a document image by drawing text at specified coordinates.

    Parameters:
    preds (list): List of dictionaries containing predicted coordinates and value.
                  Expected keys are "cx", "cy", and "value", where "cx" and "cy" are
                  relative positions (0 to 1) of the center of the text and "value" is the text to be displayed.

    The function opens the specified image, calculates the absolute position for the
    text using the relative coordinates from `preds`, and draws the text centered at
    this position in blue color. The result is saved as 'output.png' in the current directory.
    """

    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))

    correctness_draw = ImageDraw.Draw(overlay)
    width, height = img.size

    # Calculate absolute coordinates.

    # img = get_image_of_state(doc_state=doc_state, blank_img=img)
    current_img = doc_state.get_image_of_state().convert("RGBA")

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
    result = Image.alpha_composite(current_img, overlay)

    result.save("output.png")


# def get_image_of_state(
#     doc_state, blank_img: Image.Image, save_path: str = None
# ) -> Image.Image:
#     new_img = blank_img.copy()
#     text_draw = ImageDraw.Draw(new_img)
#     preds = doc_state.marks
#     width, height = new_img.size

#     color_map = {
#         CreatorEnum.PREFILLED.value: "blue",
#         CreatorEnum.AGENT.value: "green",
#     }
#     for pred in preds:
#         x = pred["cx"] * width
#         y = pred["cy"] * height

#         # Load Times New Roman font, size 10.
#         # try:
#         #     pass
#         # except IOError:
#         #     font = ImageFont.load_default()

#         field_name = pred["field_name"] if "field_name" in pred else ""
#         text = str(pred["value"])

#         # Draw the text in blue.

#         text_draw.text(
#             (x, y), text, fill=color_map[pred["creator"]], font=FILLER_FONT, anchor="mm"
#         )

#         # Draw a rectangle based on the bbox
#         bbox = pred["bbox"]
#         text_draw.rectangle(
#             (
#                 bbox["x"] * width,
#                 bbox["y"] * height,
#                 (bbox["x"] + bbox["width"]) * width,
#                 (bbox["y"] + bbox["height"]) * height,
#             ),
#             outline=(0, 0, 255),
#         )
#     # save the image
#     if save_path:
#         new_img.save(save_path)
#     return new_img  # drawn on


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
    # Regex that attempts to capture top-level { ... } blocks (no nested braces).
    # If there's a missing '}', that chunk won't match and won't be parsed.
    pattern = r"(\{[^}]*\})"
    matches = re.findall(pattern, response_text)

    passed_actions = []
    failed_actions = []
    for match in matches:
        try:
            match_dict = json.loads(match)
            action_name = match_dict["action"]

            # Assume these are defined somewhere in your code:
            #   ActionMeta.registry -> dict of valid actions
            #   InvalidAction -> some fallback action class
            #   Each action has a Schema for validation
            if action_name in ActionMeta.registry:
                action = ActionMeta.registry[action_name]
            else:
                action = InvalidAction

            # Validate against the schema
            action.Schema(**match_dict)
            passed_actions.append(match_dict)

        except (JSONDecodeError, ValidationError) as e:
            # Instead of crashing, just skip the broken chunk
            print(f"Skipping invalid JSON block: {match}\nError: {e}")
            failed_actions.append(match)

    return passed_actions


# def add_bbox(forward_fn):
#     def wrapper(
#         self,
#         nl_profile: str,
#         doc_image: Image.Image,
#         available_actions: List[str],
#         targets: List[str] = [],
#     ):
#         result = forward_fn(self, nl_profile, doc_image, available_actions, targets)
#         for i, r in enumerate(result):
#             r["bbox"] = get_text_bbox(
#                 text=r["value"],
#                 doc_width=doc_image.width,
#                 doc_height=doc_image.height,
#                 cx=r["cx"],
#                 cy=r["cy"],
#             )
#         return result

#     return wrapper


class CheaterModel:
    def __init__(self, doc_state, user_profile):
        self.doc_state = doc_state
        self.user_profile = user_profile

    # @add_bbox
    def forward(
        self,
        nl_profile: str,
        doc_image: Image.Image,
        available_actions: List[str],
        targets: List[str] = [],
        feedback: List[List] = None,
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
            # bbox = get_text_bbox(cheat_input, doc_image.width, doc_image.height, field_mid_x, field_mid_y)
            preds.append(
                {
                    "action": "PlaceText",
                    "cx": field_mid_x,
                    "cy": field_mid_y,
                    "field_name": field["field_name"],
                    "value": cheat_input,
                }
            )
        return preds


class ScriptedModel:
    def __init__(self, batch_size, script_name: str):
        w = 732
        h = 454
        self.batch_size = batch_size
        # self.script = [
        scripts = {
            "xx_0_0": [
                {
                    "action": "FieldLocalizer",
                    "value": "Bank Name",
                },
                {
                    "action": "FieldLocalizer",
                    "value": "Bank Account Number",
                },
                {
                    "action": "FieldLocalizer",
                    "value": "Single",
                },
                {
                    "action": "FieldLocalizer",
                    "value": "Married",
                },
                {
                    "action": "FieldLocalizer",
                    "value": "Initial",
                },
                {
                    "action": "PlaceText",
                    "cx": 551 / w,
                    "cy": 20 / h,
                    "value": "WRONG TEXT 1",
                },
                {
                    "action": "PlaceText",
                    "cx": 560 / w,
                    "cy": 114 / h,
                    "value": "WRONG TEXT 2",
                },
                {
                    "action": "PlaceText",
                    "cx": 37 / w,
                    "cy": 247 / h,
                    "value": "x",
                },
                {
                    "action": "SignOrInitial",
                    "cx": 209 / w,
                    "cy": 368 / h,
                    "value": "LR",
                },
                {  # delete action 0
                    "action": "DeleteText",
                    "cx": 551 / w,
                    "cy": 20 / h,
                },
                {  # delete action 1
                    "action": "DeleteText",
                    "cx": 560 / w,
                    "cy": 114 / h,
                },
                {
                    "action": "PlaceText",
                    "cx": 560 / w,
                    "cy": 20 / h,
                    "value": "MidFirst Bank",
                },
                {
                    "action": "PlaceText",
                    "cx": 560 / w,
                    "cy": 114 / h,
                    "value": "787412324",
                },
                {
                    "action": "Terminate",
                },
            ],
            "cr_0_0": [
                {
                    "action": "QuerySql",
                    "query": "SELECT * FROM features WHERE key = 'CROI_4435'",
                }
            ],
            "al_2_0": [
                {
                    "action": "FieldLocalizer",
                    "value": "Last Name",
                },
                {
                    "action": "FieldLocalizer",
                    "value": "Cell Phone Number",
                },
                {
                    "action": "FieldLocalizer",
                    "value": "Gross Income",
                },
                {
                    "action": "FieldLocalizer",
                    "value": "Present Employer",
                },
            ],
        }
        self.script = scripts[script_name]
        self.count = 0

    # @add_bbox
    def forward(
        self,
        nl_profile: List[str],
        doc_image: List[Image.Image],
        available_actions: List[str],
        targets: List[str] = [],
        feedback: List[List] = None,
        **kwargs,
    ) -> List[Dict]:
        if self.count >= len(self.script):
            # todo: terminate and check for errors
            # raise StopIteration
            return [
                [
                    {
                        "action": "Terminate",
                    }
                ]
                for _ in range(self.batch_size)
            ]
        pred = self.script[self.count]
        self.count += 1

        return [[pred] for _ in range(min(self.batch_size, len(doc_image)))]


class GptModelE2E:
    def __init__(self, model_name: str, draw_grid: bool = False):
        self.model_name = model_name
        self.draw_grid = draw_grid

    # @add_bbox
    def forward(
        self,
        nl_profile: List[str],
        doc_image: List[Image.Image],
        available_actions: List[str],
        flow: List[str],
        feedback: List[List] = None,
    ) -> List[Dict]:
        outputs = []
        for profile, image, f in zip(nl_profile, doc_image, flow):
            prompt = get_e2e_prompt(
                user_profile=profile,
                api_documentation=ActionMeta.all_documentation(
                    "\n\n".join(available_actions)
                ),
                grid_subprompt=grid_subprompt_content if self.draw_grid else "",
                task=f,
                feedback=feedback,
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


class HFE2EModel:
    def __init__(
        self, model_name: str, download_dir: str, seed=None, draw_grid: bool = False
    ):
        model_registry = {
            "aria": AriaModel,
            "llava": LlavaModel,
            "molmo": MolmoModel,
            "qwen_vl": QwenVLModel,
            "deepseek_vl2": DeepseekVL2Model,
            "gemma3": Gemma3Model,
            "mllama": MLLamaModel,
        }

        if model_name not in model_registry:
            raise ValueError(f"Unsupported model: {model_name}")

        self.model = model_registry[model_name]()

        engine_args_dict = asdict(self.model.engine_args)
        engine_args_dict["download_dir"] = download_dir
        engine_args_dict["seed"] = seed
        # TODO - Argument for multiple GPUs
        # engine_args_dict["tensor_parallel_size"] = 4

        self.llm = LLM(**engine_args_dict)

        self.sampling_params = SamplingParams(
            temperature=0.2,
            max_tokens=64,
            stop_token_ids=self.model.stop_token_ids,
        )

        self.model_name = model_name
        self.draw_grid = draw_grid

    def forward(
        self,
        nl_profile: List[str],
        doc_image: List[Image.Image],
        available_actions: List[str],
        flow: List[str],
        feedback: List[List] = None,
    ):
        base_prompts = []

        for profile, f in zip(nl_profile, flow):
            base_prompt = get_e2e_prompt(
                user_profile=profile,
                api_documentation=ActionMeta.all_documentation(
                    "\n\n".join(available_actions)
                ),
                grid_subprompt=grid_subprompt_content if self.draw_grid else "",
                task=f,
                feedback=feedback,
            )
            base_prompts.append(base_prompt)

        prompts = self.model.get_templated_prompts(base_prompts)

        all_inputs = []
        for img, prompt in zip(doc_image, prompts):
            all_inputs.append(
                {
                    "prompt": prompt,
                    "multi_modal_data": {"image": img},
                }
            )

        start_time = time.time()
        outputs = self.llm.generate(all_inputs, sampling_params=self.sampling_params)
        elapsed_time = time.time() - start_time

        parsed_outputs = []
        for i, out in enumerate(outputs):
            raw_text = out.outputs[0].text
            print(f"Raw Outputs for input {i}:")
            print(raw_text)
            print("====" * 20)
            parsed_response = parse_and_reconstruct_fields(raw_text)
            print(f"Parsed Outputs for input {i}:")
            print(parsed_response)
            print("====" * 20)
            parsed_outputs.append(parsed_response)

        return parsed_outputs
