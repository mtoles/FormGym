"""
Definitions of actions that an agent can take on a form
"""
import json
from typing import List, Dict
from copy import deepcopy

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
    
class Action(metaclass=ActionMeta):
    @staticmethod
    def act(doc_state, **kwargs):
        """
        Must always return doc_state. Use kwargs to update the doc state in some way.
        """
        raise NotImplementedError
        return doc_state
    
### Actions for image pdfs

class PlaceText(Action):
    """
    
    """

    documentation = """
    Place a text on an image or pdf. The center of the text will be placed at (x, y), where (0, 0) is the top left corner and (1, 1) is the bottom right. `Value` is the text to place.

    Args:
        doc_state: The form being interacted with. Can be a pdf or a website.
        x: The x position of the text relative to the top left corner of the screen
        y: The y position of the text relative to the top left corner of the screen
        value: The text to place on the pdf

    Example input:
        {"action": "PlaceText", "x": 0.5, "y": 0.5, "value": "Hello World!"}
    """

    def act(doc_state, x: float, y: float, value: str, **kwargs):
        doc_state.marks.append({"x": x, "y": y, "value": value})
        return doc_state


class Sign(Action):
    pass

### Actions for editable pdfs and websites

class Click(Action):
    pass

class ModifyText(Action):
    pass

class SelectFileUpload(Action):
    pass

class Terminate(Action):
    pass


def update_doc_state(doc_state, agent_generations: List[Dict]):
    doc_state = deepcopy(doc_state)
    assert isinstance(agent_generations, list)
    assert isinstance(agent_generations[0], dict)
    for ag in agent_generations:
        act_name = ag["action"]
        act = ActionMeta.registry[act_name]
        doc_state = act.act(doc_state, **ag)
    return doc_state
