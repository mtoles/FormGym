"""
Definitions of actions that an agent can take on a form
"""

import json
from typing import List, Dict, Literal
from copy import deepcopy
from pydantic import BaseModel
from enum import Enum
from utils import *
from transformers import AutoProcessor, AutoModelForCausalLM
import torch
from pathlib import Path
import yaml
from tool.train_florence import (
    load_from_checkpoint,
    TEXT_INPUT_PROMPT_TEMPLATE,
    TASK_NAME_PREFIX,
)
from utils import *
from PIL import Image, ImageDraw
from datetime import datetime


class ActionMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name not in ["BaseAction"]:
            # check for duplicates
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr

    def all_documentation(available_actions: List[str]):
        docstring = ""
        # for name, action in ActionMeta.registry.items():
        #     if name in available_actions:
        #         docstring += f"{name}: {action.documentation}\n\n"
        for act in available_actions:
            docstring += f"{act}: {ActionMeta.registry[act].documentation}\n\n"
        return docstring


class BaseAction(metaclass=ActionMeta):
    @staticmethod
    def act(doc_state, **kwargs):
        """
        Must always return doc_state. Use kwargs to update the doc state in some way.
        """
        print("Subclasses must implement this method")
        raise NotImplementedError

    class Schema(BaseModel):
        """
        A pydantic schema defining valid input for this action. The schema should always be a subclass of pydantic.BaseModel and contain an `action` field whose value is the action name, as a literal.
        """

        def __call__(self, *args, **kwds):
            print("Subclasses must implement this method")
            raise NotImplementedError


### Actions for image pdfs


class PlaceText(BaseAction):
    documentation = """
    Place a text on a document, image, or pdf. The center of the text will be placed at (x, y), where (0, 0) is the top left corner and (1, 1) is the bottom right of the image. `Value` is the text to place.

    Args:
        cx: The x position of the center of the text relative to the top left corner of the screen
        cy: The y position of the center of the text relative to the top left corner of the screen
        value: The text to place on the pdf

    Example input:
        {"action": "PlaceText", "cx": 0.5, "cy": 0.5, "value": "Hello World!"}
    """

    def act(doc_state, cx: float, cy: float, value: str, **kwargs):
        mark = {
            "action": "PlaceText",
            "cx": cx,
            "cy": cy,
            "value": value,
            "creator": "agent",
        }

        mark["bbox"] = get_text_bbox(
            text=value,
            doc_width=doc_state.w,
            doc_height=doc_state.h,
            cx=cx,
            cy=cy,
        )

        doc_state.marks.append(mark)

        feedback = f"Action: 'PlaceText'\nText placed: <`{value}` at ({cx}, {cy})>"
        return doc_state, feedback

    class Schema(BaseModel):
        action: Literal["PlaceText"]
        cx: float
        cy: float
        value: str


class DeleteText(BaseAction):
    documentation = """
    Delete all text at a point on a document, image, or pdf. Any textbox intersecting with the point (x, y), where (0,0) is the top left corner and (1,1) is the bottom right corner of the image, will be deleted. 

    Args:
        x: The x position of the center of the text relative to the top left corner of the screen
        y: The y position of the center of thetext relative to the top left corner of the screen

    Example input:
        {"action": "DeleteText", "cx": 0.5, "cy": 0.5}
    """

    def act(doc_state, cx: float, cy: float, **kwargs):
        # Find all marks in doc_state.marks that intersect with (x, y)
        retained_marks = []
        deleted_marks = []

        # Add a check to see if there are no marks to delete then skip
        if not doc_state.marks:
            feedback = "Action: 'DeleteText'\nNo marks to delete."
            return doc_state, feedback

        for mark in doc_state.marks:
            if (
                (cx >= mark["bbox"]["x"])
                and (cx <= mark["bbox"]["x"] + mark["bbox"]["width"])
                and (cy >= mark["bbox"]["y"])
                and (cy <= mark["bbox"]["y"] + mark["bbox"]["height"])
            ):
                deleted_marks.append(mark)
            else:
                retained_marks.append(mark)
        doc_state.marks = retained_marks
        print(f"Marks deleted: {deleted_marks}")
        feedback = f"Action: 'DeleteText'\nMarks deleted: {deleted_marks}"
        return doc_state, feedback

    class Schema(BaseModel):
        action: Literal["DeleteText"]
        cx: float
        cy: float


class SignOrInitial(BaseAction):
    documentation = """
    Sign or initial a document, image, or pdf. The center of the signature will be placed at (x, y), where (0, 0) is the top left corner and (1, 1) is the bottom right of the image. `Value` is the name or initials of the signer. When signing a document, sign with the user's first name and last name, nothing else.

    Args:
        x: The x position of the center of the signature relative to the top left corner of the screen
        y: The y position of the center of thesignature relative to the top left corner of the screen
        value: The name or initials of the signer

    Example input:
        {"action": "SignOrInitial", "cx": 0.5, "cy": 0.5, "value": "John Doe"}
    """

    def act(doc_state, cx: float, cy: float, value: str, **kwargs):
        mark = {
            "action": "Sign",
            "cx": cx,
            "cy": cy,
            "value": value,
            "creator": "agent",
        }

        mark["bbox"] = get_text_bbox(
            text=value,
            doc_width=doc_state.w,
            doc_height=doc_state.h,
            cx=cx,
            cy=cy,
        )

        doc_state.marks.append(mark)

        feedback = (
            f"Action: 'SignOrInitial'\nSignature placed: <`{value}` at ({cx}, {cy})>"
        )
        return doc_state, feedback

    class Schema(BaseModel):
        action: Literal["SignOrInitial"]
        cx: float
        cy: float
        value: str


class QuerySql(BaseAction):
    documentation = """
    Query a SQL database.
    Args:
        query: The SQL query to execute. The table is called "features".
    
    Example input:
        {"action": "QuerySql", "query": "SELECT value FROM features where key='CROI_0093'"}
    """

    def act(doc_state, query: str, db, **kwargs):
        assert db is not None
        try:
            output = db.query(query)
            feedback = (
                f"Action: 'QuerySql'\nQuery executed successfully. Output: {output}"
            )
        except Exception as e:
            feedback = f"Action: 'QuerySql'\nError executing query: {str(e)}"
            print(feedback)
        return doc_state, feedback


class Terminate(BaseAction):
    documentation = """
    Terminate the document generation process.
    Args:
        None
    
    Example input:
        {"action": "Terminate"}
    """

    class Schema(BaseModel):
        action: Literal["Terminate"]

    def act(doc_state, **kwargs):
        feedback = "Action: 'Terminate'\nDocument generation process terminated."
        return doc_state, feedback


class InvalidAction(BaseAction):
    class Schema(BaseModel):
        pass
        # allow anything

    def act(doc_state, **kwargs):
        feedback = "Action: 'InvalidAction'\nDocument returned unchanged."
        return doc_state, feedback


class FieldLocalizer(BaseAction):
    documentation = """
    Given a string of question in a document, image, or pdf, return the center of the textbox, line, or cell related to the question.
    Args:
        value: The string of question in a document, image, or pdf

    Example input:
        {"action": "FieldLocalizer", "value": "First Name"}
    """
    PROD_TOOL_CHECKPOINT_PATH = "tool/prod_tool_checkpoint"
    device = torch.device(
        "cuda:1"
        if torch.cuda.is_available() and torch.cuda.device_count() >= 2
        else "cuda:0" if torch.cuda.is_available() else "cpu"
    )
    processor, model = load_from_checkpoint(PROD_TOOL_CHECKPOINT_PATH, device)

    @classmethod
    def _visualize_localizer(
        cls,
        img,
        value: str,
        pred_bboxes: List[List[int]],
        save_path: str = "field_localizer_output.png",
    ):
        """Helper method to visualize predictions with bounding boxes and labels.

        Args:
            img: PIL Image to draw on
            value: The input value to use as label
            pred_bboxes: List of predicted bounding boxes
            save_path: Where to save the visualization
        """
        vis_img = img.copy()
        draw = ImageDraw.Draw(vis_img)

        for bbox in pred_bboxes:
            # Draw the bounding box
            draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline="red", width=2)
            # Draw the label
            draw.text((bbox[0], bbox[1] - 20), value, fill="red")

        # Save the visualization
        vis_img.save(save_path)
        return save_path

    @classmethod
    def act(cls, doc_state, value: str, return_bboxes: bool = False, **kwargs):
        img = doc_state.get_image_of_state()
        w = img.width
        h = img.height
        prompt = TEXT_INPUT_PROMPT_TEMPLATE.format(target=value)
        inputs = cls.processor(text=prompt, images=img, return_tensors="pt").to(
            cls.device
        )
        generated_ids = cls.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=512,
            num_beams=3,
            do_sample=False,
        )
        generated_text = cls.processor.batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]

        parsed_answer = cls.processor.post_process_generation(
            generated_text, task=TASK_NAME_PREFIX, image_size=(img.width, img.height)
        )

        pred_bboxes = parsed_answer[TASK_NAME_PREFIX]["bboxes"]
        # Round bbox coordinates to 3 decimal points
        pred_bboxes = [[round(coord, 3) for coord in bbox] for bbox in pred_bboxes]

        if len(pred_bboxes) == 0:
            feedback = f"Action: 'FieldLocalizer'\nNo bbox found for {value}"
            if return_bboxes:
                return doc_state, feedback, None
            else:
                return doc_state, feedback
        else:
            all_bboxes = []
            for bbox in pred_bboxes:
                bbox = [int(b) for b in bbox]
                x1 = bbox[0] / w
                y1 = bbox[1] / h
                x2 = bbox[2] / w
                y2 = bbox[3] / h
                all_bboxes.append(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")

            # Visualize predictions
            # save_path = cls._visualize_localizer(
            #     img,
            #     value,
            #     pred_bboxes,
            #     save_path=f"tmp/{doc_state.doc_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            # )

            feedback = (
                f"Action: 'FieldLocalizer'\nPredicted bboxes for {value}:\n"
                + "\n".join(all_bboxes)
                # + f"\nVisualization saved to {save_path}"
            )

            if return_bboxes:
                return doc_state, feedback, pred_bboxes
            else:
                return doc_state, feedback, None


class PlaceWithLocalizer(BaseAction):
    documentation = """
    Place a piece of text in a target field on a document, image, or pdf. This tool will automatically find the target field and place the text there. If the target field needs to be described with additional specificity (e.g., section headers, table columns), list them from highest to lowest in the hierarchy, separated by | as in: "Section Header | Table Column | Table Row" or "User 1 | First Name.
    Args:
        target: The name of the field as it appears in the document
        value: The text to place in the target field

    Example input:
        {"action": "PlaceWithLocalizer", "target": "First Name", "value": "John"}
    """

    def act(doc_state, target: str, value: str, **kwargs):
        localizer_doc_state, localizer_feedback, localizer_bboxes = FieldLocalizer.act(
            doc_state, target, return_bboxes=True
        )
        # Get center coordinates from first predicted bbox

        if localizer_bboxes is None:
            return doc_state, localizer_feedback
        else:
            first_bbox = localizer_bboxes[0]
            x1, y1, x2, y2 = first_bbox
            cx = (x1 + x2) / (2 * doc_state.w)
            cy = (y1 + y2) / (2 * doc_state.h)
            doc_state, feedback = PlaceText.act(doc_state, cx, cy, value)
            print(f"Placed text for {target} as {value} at {cx}, {cy}")
            return doc_state, feedback


class SignOrInitialWithLocalizer(BaseAction):
    documentation = """
    Sign or initial a target field on a document, image, or pdf. This tool will automatically find the target field and place the signature there. If the target field needs to be described with additional specificity (e.g., section headers, table columns), list them from highest to lowest in the hierarchy, separated by | as in: "Section Header | Table Column | Table Row" or "User 1 | Signature". When signing a document, sign with the user's first name and last name, nothing else.
    Args:
        target: The name of the field as it appears in the document
        value: The text to place in the target field

    Example input:
        {"action": "SignOrInitialWithLocalizer", "target": "Signature", "value": "John Doe"}
    """

    def act(doc_state, target: str, value: str, **kwargs):
        localizer_doc_state, localizer_feedback, localizer_bboxes = FieldLocalizer.act(
            doc_state, target, return_bboxes=True
        )
        # Get center coordinates from first predicted bbox

        if localizer_bboxes is None:
            return doc_state, localizer_feedback
        else:
            first_bbox = localizer_bboxes[0]
            x1, y1, x2, y2 = first_bbox
            cx = (x1 + x2) / (2 * doc_state.w)
            cy = (y1 + y2) / (2 * doc_state.h)
            doc_state, feedback = SignOrInitial.act(doc_state, cx, cy, value)
            print(f"Placed signature for {target} as {value} at {cx}, {cy}")
            return doc_state, feedback


def update_doc_state(doc_state, agent_generations: List[Dict], db=None):
    print("Updating doc state with agent generations")
    doc_state = deepcopy(doc_state)
    assert isinstance(agent_generations, list)
    if agent_generations:
        assert isinstance(agent_generations[0], dict)
    feedbacks = []
    for ag in agent_generations:
        act_name = ag["action"]
        # if act_name in ActionMeta.registry:
        try:
            act = ActionMeta.registry[act_name]
        except KeyError as e:
            print(f"Error with action:\n{ag}\n{e}")
            act = InvalidAction
        try:
            doc_state, feedback = act.act(doc_state, **ag, db=db)
        except (TypeError, ValueError) as e:
            print(f"Error with action:\n{ag}\n{e}")
            act = InvalidAction
            doc_state, feedback = act.act(doc_state, **ag, db=db)
        feedbacks.append(feedback)

    # # add bboxes to every mark
    # for mark in doc_state.marks:
    #     mark["bbox"] = get_text_bbox(
    #         text=mark["value"],
    #         doc_width=doc_state.w,
    #         doc_height=doc_state.h,
    #         cx=mark["cx"],
    #         cy=mark["cy"],
    #     )

    return doc_state, feedbacks
