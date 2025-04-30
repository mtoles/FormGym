import user_profile_attributes
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

def numerize(s: str) -> str:
    """Extract only numeric characters from a string."""
    ls = list(s)
    valid = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    return str([x for x in ls if x in valid])


def remove_punctuation(s: str) -> str:
    """Remove punctuation and normalize whitespace in a string."""
    # replace punctuation with space
    s = "".join(
        " " if c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c" else c
        for c in s
    )
    # replace all whitespace with spaces
    s = " ".join(s.split())
    return s


def concat_agent_generations(agent_generations: List[Dict[str, Any]]) -> str:
    """Concatenate agent generations in order of their coordinates."""
    return " ".join(
        [
            x["value"]
            for x in sorted(
                agent_generations, key=lambda item: (item["cy"], item["cx"])
            )
        ]
    )


def get_inputs_inside_field(field: 'FormBaseField', agent_generations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get all agent generations that fall within a field's boundaries."""
    return [
        ag
        for ag in agent_generations
        if (
            ag["cx"] >= field.x
            and ag["cx"] <= field.x + field.w
            and ag["cy"] >= field.y
            and ag["cy"] <= field.y + field.h
        )
    ]


class FormFieldMeta(type):
    """
    Metaclass for possible form fields.
    Maintains a registry of all form field classes.
    """
    registry: Dict[str, type] = {}

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        new_p_attr = super().__new__(cls, name, bases, attrs)
        base_classes = ["FormBaseField", "FormBaseNumericField", "FormBaseStringField", 
                       "FormBaseCheckboxField", "FormAnnotatedField", "FormSignOrInitial", 
                       "FormSignature", "FormInitials"]
        if name not in base_classes:
            # check for duplicates
            assert name not in cls.registry, f"Form field {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class FormBaseField(metaclass=FormFieldMeta):
    """Base class for all form fields."""
    
    def __init__(self, x: float, y: float, w: float, h: float):
        """
        Initialize a form field with its position and dimensions.
        
        Args:
            x: x-coordinate of the field
            y: y-coordinate of the field
            w: width of the field
            h: height of the field
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abstractmethod
    def is_correct(self, agent_generation: List[Dict[str, Any]], user_profile: 'user_profile_attributes.FormUserProfile') -> bool:
        """Check if the agent's generation matches the user profile for this field."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_profile_info(cls, user_profile: 'user_profile_attributes.FormUserProfile') -> Any:
        """Get the relevant information from the user profile for this field."""
        raise NotImplementedError


class FormBaseNumericField(FormBaseField):
    """Base class for numeric form fields."""
    
    def is_correct(self, agent_generation: List[Dict[str, Any]], user_profile: 'user_profile_attributes.FormUserProfile') -> bool:
        """Check if the numeric input matches the user profile."""
        agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        profile_info = self.get_profile_info(user_profile)
        return numerize(str(profile_info)) == numerize(concatted_input)


class FormBaseStringField(FormBaseField):
    """Base class for string form fields."""
    
    def is_correct(self, agent_generation: List[Dict[str, Any]], user_profile: 'user_profile_attributes.FormUserProfile') -> bool:
        """Check if the string input matches the user profile."""
        agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        profile_info = self.get_profile_info(user_profile)
        return remove_punctuation(str(profile_info)) == remove_punctuation(concatted_input)


class FormBaseCheckboxField(FormBaseField):
    """Base class for checkbox form fields."""
    
    def is_correct(self, agent_generation: List[Dict[str, Any]], user_profile: 'user_profile_attributes.FormUserProfile') -> bool:
        """Check if the checkbox state matches the user profile."""
        agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        profile_info = self.get_profile_info(user_profile)
        assert isinstance(profile_info, bool), f"Checkbox field {self.__class__.__name__} must return a boolean"
        if profile_info:
            return concatted_input.lower() in ["x", "✓", "☑", "⬛", "✓"]
        else:
            return concatted_input.strip() == ""


class FormAnnotatedField(FormBaseField):
    """Base class for annotated form fields."""
    pass