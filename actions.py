"""
Definitions of actions that an agent can take on a form
"""
import json
from typing import List, Dict, Literal
from copy import deepcopy
from pydantic import BaseModel
from enum import Enum

class CreatorEnum(Enum):
    agent = "agent"
    prefilled = "prefilled"

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
        x: The x position of the text relative to the top left corner of the screen
        y: The y position of the text relative to the top left corner of the screen
        value: The text to place on the pdf

    Example input:
        {"action": "PlaceText", "x": 0.5, "y": 0.5, "value": "Hello World!"}
    """

    def act(doc_state, x: float, y: float, value: str, **kwargs):
        doc_state.marks.append({"action": "PlaceText", "x": x, "y": y, "value": value, "creator": "agent"})
        return doc_state
    

    class Schema(BaseModel):
        action: Literal["PlaceText"]
        x: float
        y: float
        value: str

    

class SignOrInitial(BaseAction):
    documentation = """
    Sign or initial a document, image, or pdf. The center of the signature will be placed at (x, y), where (0, 0) is the top left corner and (1, 1) is the bottom right of the image. `Value` is the name or initials of the signer.

    Args:
        x: The x position of the signature relative to the top left corner of the screen
        y: The y position of the signature relative to the top left corner of the screen
        value: The name or initials of the signer

    Example input:
        {"action": "SignOrInitial", "x": 0.5, "y": 0.5, "value": "John Doe"}
    """

    def act(doc_state, x: float, y: float, value: str, **kwargs):
        doc_state.marks.append({"action": "Sign", "x": x, "y": y, "value": value, "creator": "agent"})
        return doc_state
    
    class Schema(BaseModel):
        action: Literal["SignOrInitial"]
        x: float
        y: float
        value: str


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
        return doc_state

### Actions for editable pdfs and websites

# class Click(BaseAction):
#     pass

# class ModifyText(BaseAction):
#     pass

# class SelectFileUpload(BaseAction):
#     pass

# class Terminate(BaseAction):
#     pass


def update_doc_state(doc_state, agent_generations: List[Dict]):
    doc_state = deepcopy(doc_state)
    assert isinstance(agent_generations, list)
    assert isinstance(agent_generations[0], dict)
    for ag in agent_generations:
        act_name = ag["action"]
        act = ActionMeta.registry[act_name]
        doc_state = act.act(doc_state, **ag)
    return doc_state
