import random
from typing import List
from PIL import Image, ImageDraw
from utils import *
# seed
random.seed(0)

class DocState:
    """
    A class to represent the state of a form having been filled in by an agent.
    Agnostic to the actual fields in the empty form
    """

    def __init__(self, doc_fields, blank_img: Image.Image):
        self.fields = doc_fields
        self.marks = []
        self.w = blank_img.width
        self.h = blank_img.height
        self.blank_img = blank_img

    def get_last_k_fields(self, k):
        # sort fields by y coordinate
        self.fields.sort(key=lambda x: x["bbox"]["y"])
        return self.fields[-k:]

    def pop_last_k_fields(self, k):
        """Edits the doc state IN PLACE and pops/returns the last k fields (sorted by y coordinate, ascending)"""
        self.fields.sort(key=lambda x: x["bbox"]["y"])
        popped = self.marks[-k:]
        self.marks = self.marks[:-k]
        return popped
    
    def pop_target_fields(self, targets: List[str]):
        """Edits the doc state IN PLACE and pops/returns the target fields"""
        remaining_fields = []
        target_fields = []
        targets = set(targets)
        for mark in self.marks:
            if mark["field_name"] in targets:
                target_fields.append(mark)
            else:
                remaining_fields.append(mark)
        self.marks = remaining_fields
        return target_fields
            
    def get_image_of_state(
        self, save_path: str = None
    ) -> Image.Image:
        new_img = self.blank_img.copy()
        text_draw = ImageDraw.Draw(new_img)
        preds = self.marks
        width, height = new_img.size

        color_map = {
            CreatorEnum.PREFILLED.value: "blue",
            CreatorEnum.AGENT.value: "green",
        }
        for pred in preds:
            x = pred["cx"] * width
            y = pred["cy"] * height

            field_name = pred["field_name"] if "field_name" in pred else ""
            text = str(pred["value"])

            text_draw.text(
                (x, y), text, fill=color_map[pred["creator"]], font=FILLER_FONT, anchor="mm"
            )

            # # Draw a rectangle based on the bbox
            # bbox = pred["bbox"]
            # text_draw.rectangle(
            #     (
            #         bbox["x"] * width,
            #         bbox["y"] * height,
            #         (bbox["x"] + bbox["width"]) * width,
            #         (bbox["y"] + bbox["height"]) * height,
            #     ),
            #     outline=(0, 0, 255),
            # )
        # save the image
        if save_path:
            new_img.save(save_path)
        return new_img  # drawn on

    # def pop_random_k_deterministic(self, k):
    #     """Edits the doc state IN PLACE and pops/returns a random set of k fields"""
    #     def get_hashable(field):
    #         return field["field_name"] + str(field["bbox"]["x"]) + str(field["bbox"]["y"] + field["bbox"]["height"] + field["bbox"]["width"])
    #     hashed = sorted(self.fields, key=lambda x: hashlib.md5(get_hashable(x)).encode()).hexdigest()
    #     popped = hashed[-k:]
    #     self.marks = self.marks[:-k]
    #     return popped


