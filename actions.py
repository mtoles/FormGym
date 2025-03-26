"""
Definitions of actions that an agent can take on a form
"""

import json
from typing import List, Dict, Literal
from copy import deepcopy
from pydantic import BaseModel
from enum import Enum
from utils import *


class ActionMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name != "BaseAction":
            # check for duplicates
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr

    def all_documentation(available_actions: List[str]):
        docstring = ""
        for name, action in ActionMeta.registry.items():
            if name in available_actions:
                docstring += f"{name}: {action.documentation}\n\n"
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
        doc_state.marks.append(
            {
                "action": "PlaceText",
                "cx": cx,
                "cy": cy,
                "value": value,
                "creator": "agent",
            }
        )
        feedback = f"Placed text: {value} at ({cx}, {cy})"
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
        # doc_state.marks = [
        #     mark
        #     for mark in doc_state.marks
        #     if cx >= mark["bbox"]["x"]
        #     and cx <= mark["bbox"]["x"] + mark["bbox"]["width"]
        #     and cy >= mark["bbox"]["y"]
        #     and cy <= mark["bbox"]["y"] + mark["bbox"]["height"]
        # ]
        print(f"Marks deleted: {deleted_marks}")
        feedback = f"Marks deleted: {deleted_marks}"
        return doc_state, feedback


class SignOrInitial(BaseAction):
    documentation = """
    Sign or initial a document, image, or pdf. The center of the signature will be placed at (x, y), where (0, 0) is the top left corner and (1, 1) is the bottom right of the image. `Value` is the name or initials of the signer.

    Args:
        x: The x position of the center of the signature relative to the top left corner of the screen
        y: The y position of the center of thesignature relative to the top left corner of the screen
        value: The name or initials of the signer

    Example input:
        {"action": "SignOrInitial", "cx": 0.5, "cy": 0.5, "value": "John Doe"}
    """

    def act(doc_state, cx: float, cy: float, value: str, **kwargs):
        doc_state.marks.append(
            {"action": "Sign", "cx": cx, "cy": cy, "value": value, "creator": "agent"}
        )
        return doc_state

    class Schema(BaseModel):
        action: Literal["SignOrInitial"]
        cx: float
        cy: float
        value: str

class QuerySql(BaseAction):
    documentation = """
    Query a SQL database.
    Args:
        query: The SQL query to execute.
    
    Example input:
        {"action": "QuerySql", "query": "SELECT * FROM table_name WHERE column_name = 'value'"}
    """

    def act(doc_state, query: str, db, **kwargs):
        return doc_state, str(db)

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
        feedback = "Terminated"
        return doc_state, feedback
    



### Actions for editable pdfs and websites

# class Click(BaseAction):
#     pass

# class ModifyText(BaseAction):
#     pass

# class SelectFileUpload(BaseAction):
#     pass

# class Terminate(BaseAction):
#     pass


def update_doc_state(doc_state, agent_generations: List[Dict], db=None):
    doc_state = deepcopy(doc_state)
    assert isinstance(agent_generations, list)
    assert isinstance(agent_generations[0], dict)
    feedbacks = []
    for ag in agent_generations:
        act_name = ag["action"]
        act = ActionMeta.registry[act_name]
        doc_state, feedback = act.act(doc_state, **ag, db=db)
        feedbacks.append(feedback)

    # add bboxes to every mark
    for mark in doc_state.marks:
        mark["bbox"] = get_text_bbox(
            text=mark["value"],
            doc_width=doc_state.w,
            doc_height=doc_state.h,
            cx=mark["cx"],
            cy=mark["cy"],
        )
    return doc_state, feedbacks
