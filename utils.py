from enum import Enum
from PIL import ImageFont, Image, ImageDraw
from typing import List


class TaskEnum(Enum):
    MULTISHOT = "iterative"
    ONESHOT = "oneshot"
    UPDATE = "update"


class FlowEnum(Enum):
    ONESHOT = "oneshot"
    ITERATIVE = "iterative"


class CreatorEnum(Enum):
    AGENT = "agent"
    PREFILLED = "prefilled"


class DatasetEnum(Enum):
    AL = "al"  # auto loans
    CR = "cr"  # consolidated report of income


class AvailableActionsEnum(Enum):
    BASELINE_MULTISHOT = ["PlaceText", "DeleteText", "SignOrInitial", "Terminate"]
    BASELINE_ONESHOT = ["PlaceText", "SignOrInitial"]
    EXPERIMENTAL_MULTISHOT = [
        "PlaceWithLocalizer",
        "DeleteText",
        "SignOrInitial",
        "Terminate",
    ]
    EXPERIMENTAL_ONESHOT = ["PlaceWithLocalizer", "SignOrInitial"]


class StudyConditionEnum(Enum):
    BASELINE = "baseline"
    EXPERIMENTAL = "ours"

class ProfileSourceEnum(Enum):
    TEXT = "text"
    IMAGE = "image"

FILLER_FONT = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSerif.ttf", 12)


def get_text_bbox(
    text: str, doc_width: int, doc_height: int, cx: float, cy: float
) -> List:
    bbox = FILLER_FONT.getbbox(text)
    text_width = (bbox[2] - bbox[0]) / doc_width
    text_height = (bbox[3] - bbox[1]) / doc_height
    return {
        "x": cx - text_width / 2,
        "y": cy - text_height / 2,
        "width": text_width,
        "height": text_height,
    }
