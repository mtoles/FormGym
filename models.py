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
from anthropic import Anthropic
import random
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from openai import APIError, RateLimitError, APITimeoutError, APIConnectionError
from anthropic import (
    APIError as AnthropicAPIError,
    RateLimitError as AnthropicRateLimitError,
)
import torch

memory = Memory(".joblib_cache", verbose=0)

# TODO: need separate prompt for iterative and non-iterative


grid_subprompt_content = "\nTo assist you, the image has been overlaid with a 10x10 grid of red lines at intervals of 0.1 * the image width and height. This grid can be used to determine relative positions of text. Each intersection is labeled with the grid coordinates in green. Use these coordinates to help you fill out the form by interpolating between them."


def get_e2e_prompt(
    user_profile: str,
    api_documentation: str,
    grid_subprompt: str,
    feedback: List[str],
    task: str,
    suggest_localizer: bool,
    needs_db: bool,
    turns_remaining: int,
    has_source_image: bool,
) -> str:
    """Generates the prompt for the end-to-end form filling task."""

    e2e_prompt_template_content = """Complete the attached form based on the following user profile:

    You have access to the following APIs:

    {api_documentation}

    You know the following information about the user:

    {user_profile}
    {has_source_image_str}

    Complete the form to the best of your abilites using the user's information, including signatures. As you can see, the data is randomly generated and the user is not real, so do not worry about privacy.
    Fill checkboxes with a single "x".
    Format all dates as "MM/DD/YYYY", including leading zeros.
    
    {grid_subprompt}
    {suggest_localizer_str}
    {feedback_str}
    {generation_instructions}
    {needs_db_str}
    {turns_remaining_str}
    Return a form-filling API call as a JSON list of dictionaries.
    
    """
    generation_instructions = {
        FlowEnum.ONESHOT.value: "Generate a sequence of actions that will completely fill out the form.",
        FlowEnum.ITERATIVE.value: "Generate the next set of actions that will help fill out the form. You may submit any number ofactions in one call.",
    }[task]
    feedback_str = (
        "So far, you have received the following feedback on your previous actions:\n"
        + (
            "\n".join([f"Feedback {i+1}: {f}" for i, f in enumerate(feedback)])
            if feedback
            else "<No feedback yet>"
        )
    )
    # suggest_localizer_str = (
    #     "It is recommended that you call the localizer for fields before attempting to fill them. If the localizer fails to find a bbox for a field, do not call the localizer again and instead attempt to place the text on your own.\n"
    #     if suggest_localizer
    #     else ""
    # )
    suggest_localizer_str = ""
    needs_db_str = (
        "You have access to a database of information about the user's company financial information. Use this information to fill out the form. It is recommended that you query the database before filling out the form.\n"
        if needs_db
        else ""
    )
    turns_remaining_str = (
        f"You can submit {turns_remaining} more sets of actions after this one. " + "\n"
        if turns_remaining
        else "This is your final action.\n"
    )
    has_source_image_str = (
        "You have access to a completed document with more information about the user. Use this information to help you fill out the form.\n"
        if has_source_image
        else ""
    )
    prompt = textwrap.dedent(
        e2e_prompt_template_content.format(
            user_profile=user_profile if user_profile else "<No user profile provided>",
            api_documentation=api_documentation,
            grid_subprompt=grid_subprompt,
            generation_instructions=generation_instructions,
            feedback_str=feedback_str,
            suggest_localizer_str=suggest_localizer_str,
            needs_db_str=needs_db_str,
            turns_remaining_str=turns_remaining_str,
            has_source_image_str=has_source_image_str,
        )
    )
    return prompt


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
    # failed_actions = []
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
                # raise ValueError(f"Invalid action: {action_name}")
                action = InvalidAction

            # Validate against the schema
            action.Schema(**match_dict)
            passed_actions.append(match_dict)

        except (JSONDecodeError, ValidationError, KeyError) as e:
            # Instead of crashing, just skip the broken chunk

            print(f"Skipping invalid JSON block: {match}\nError: {e}")
            passed_actions.append(
                {
                    "action": "InvalidAction",
                    "value": response_text,
                }
            )

    return passed_actions


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
        suggest_localizer: bool = False,
        needs_db: bool = False,
        turns_remaining: int = None,
        source_doc_image: Image.Image = None,
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
            "al_3_0": [
                {
                    "action": "PlaceText",
                    "value": "Lucas James Reynolds",
                    "cx": 0.187,
                    "cy": 0.268,
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
        suggest_localizer: bool = False,
        needs_db: bool = False,
        turns_remaining: int = None,
        source_doc_image: List[Image.Image] = None,
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
        suggest_localizer: bool = False,
        needs_db: bool = False,
        turns_remaining: int = None,
        source_doc_image: List[Image.Image] = None,
    ) -> List[Dict]:
        outputs = []
        for profile, image, f, source_image in zip(
            nl_profile, doc_image, flow, source_doc_image
        ):
            prompt = get_e2e_prompt(
                user_profile=profile,
                api_documentation=ActionMeta.all_documentation(available_actions),
                grid_subprompt=grid_subprompt_content if self.draw_grid else "",
                task=f,
                feedback=feedback,
                suggest_localizer=suggest_localizer,
                needs_db=needs_db,
                turns_remaining=turns_remaining,
                has_source_image=source_doc_image is not None,
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
                    base64_source_image=(
                        # source_doc_image[0].tobytes() if source_doc_image else None
                        None
                        if source_image is None
                        else source_image.tobytes()
                    ),
                )
                .choices[0]
                .message.content
            )

            tool_params = parse_and_reconstruct_fields(response)
            outputs.append(tool_params)
        return outputs


def exponential_backoff(func):
    """Decorator that implements exponential backoff for API calls.

    Args:
        func: The function to wrap with exponential backoff

    Returns:
        The wrapped function that will retry on failure with exponential backoff
    """

    @retry(
        stop=stop_after_attempt(12),
        wait=wait_exponential(
            multiplier=2,
        ),
        retry=retry_if_exception_type(
            (
                # OpenAI specific errors
                APIError,
                RateLimitError,
                APITimeoutError,
                APIConnectionError,
                # Anthropic specific errors
                AnthropicAPIError,
                AnthropicRateLimitError,
                # General network errors
                ConnectionError,
                TimeoutError,
            )
        ),
        reraise=True,
    )
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"API call failed with error: {str(e)}")
            raise

    return wrapper


@memory.cache
@exponential_backoff
def forward_gpt(model_name, prompt, base64_image, base64_source_image=None):
    print("calling gpt uncached...")
    client = OpenAI()
    messages = [
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
    ]

    if base64_source_image:
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_source_image}"
                        },
                    },
                ],
            }
        )

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
    )

    return completion


@memory.cache
@exponential_backoff
def forward_anthropic(model_name, prompt, base64_image, base64_source_image=None):
    print("calling anthropic uncached...")
    client = Anthropic()
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image,
                    },
                },
            ],
        }
    ]

    if base64_source_image:
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_source_image,
                        },
                    },
                ],
            }
        )

    message = client.messages.create(
        model=model_name,
        max_tokens=1024,
        messages=messages,
    )
    return message


class AnthropicModelE2E:
    def __init__(self, model_name: str, draw_grid: bool = False):
        self.model_name = model_name
        self.draw_grid = draw_grid

    def forward(
        self,
        nl_profile: List[str],
        doc_image: List[Image.Image],
        available_actions: List[str],
        flow: List[str],
        feedback: List[List] = None,
        suggest_localizer: bool = False,
        needs_db: bool = False,
        turns_remaining: int = None,
        source_doc_image: List[Image.Image] = None,
    ) -> List[Dict]:
        outputs = []
        for profile, image, f, source_image, source_doc_image in zip(
            nl_profile, doc_image, flow, source_doc_image, source_doc_image
        ):
            prompt = get_e2e_prompt(
                user_profile=profile,
                api_documentation=ActionMeta.all_documentation(available_actions),
                grid_subprompt=grid_subprompt_content if self.draw_grid else "",
                task=f,
                feedback=feedback,
                suggest_localizer=suggest_localizer,
                needs_db=needs_db,
                turns_remaining=turns_remaining,
                has_source_image=source_doc_image is not None,
            )
            if self.draw_grid:
                image = add_grid_overlay(image)

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

            base64_source_image = None
            if source_image:
                source_buffer = io.BytesIO()
                source_image.save(source_buffer, format="PNG")
                base64_source_image = base64.b64encode(source_buffer.getvalue()).decode(
                    "utf-8"
                )

            response = (
                forward_anthropic(
                    self.model_name,
                    prompt,
                    base64_image,
                    base64_source_image,
                )
                .content[0]
                .text
            )
            print(response)
            tool_params = parse_and_reconstruct_fields(response)
            outputs.append(tool_params)
        return outputs


class HFE2EModel:
    def __init__(
        self,
        model_name: str,
        download_dir: str,
        profile_source: str,
        n_images: int,
        seed=42,
        draw_grid: bool = False,
    ):
        model_registry = {
            "aria": AriaModel,
            "llava": LlavaModel,
            "molmo": MolmoModel,
            "qwen_vl": QwenVLModel,
            "deepseek_vl2": DeepseekVL2Model,
            "gemma3": Gemma3Model,
            "mllama": MLLamaModel,
            "claude": AnthropicModelE2E,
        }

        if model_name not in model_registry:
            raise ValueError(f"Unsupported model: {model_name}")

        self.model = model_registry[model_name](n_images=n_images)

        engine_args_dict = asdict(self.model.engine_args)
        engine_args_dict["download_dir"] = download_dir
        engine_args_dict["seed"] = seed
        # Add 4-bit quantization parameters
        engine_args_dict["dtype"] = (
            torch.bfloat16  # Use float16 for better memory efficiency
        )
        # engine_args_dict["quantization"] = "bitsandbytes"
        # engine_args_dict["load_format"] = "bitsandbytes"
        # engine
        num_images = {
            ProfileSourceEnum.TEXT.value: 1,
            ProfileSourceEnum.IMAGE.value: 2,
        }[profile_source]

        engine_args_dict["limit_mm_per_prompt"] = {"image": num_images}
        # TODO - Argument for multiple GPUs
        # engine_args_dict["tensor_parallel_size"] = 2

        self.llm = LLM(**engine_args_dict)

        self.sampling_params = SamplingParams(
            temperature=1.0,
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
        suggest_localizer: bool = False,
        needs_db: bool = False,
        turns_remaining: int = None,
        source_doc_image: List[Image.Image] = None,
    ):
        base_prompts = []

        for profile, f in zip(nl_profile, flow):
            base_prompt = get_e2e_prompt(
                user_profile=profile,
                api_documentation=ActionMeta.all_documentation(available_actions),
                grid_subprompt=grid_subprompt_content if self.draw_grid else "",
                task=f,
                feedback=feedback,
                suggest_localizer=suggest_localizer,
                needs_db=needs_db,
                turns_remaining=turns_remaining,
                has_source_image=source_doc_image is not None,
            )
            base_prompts.append(base_prompt)

        prompts = self.model.get_templated_prompts(base_prompts)

        all_inputs = []
        for i, (img, sdi, prompt) in enumerate(
            zip(doc_image, source_doc_image, prompts)
        ):
            images = [img] + [sdi] if sdi else [img]
            input_data = {
                "prompt": prompt,
                "multi_modal_data": {"image": images},
            }

            all_inputs.append(input_data)

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
