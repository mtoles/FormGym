import random
from typing import List

# seed
random.seed(0)

class DocState:
    """
    A class to represent the state of a form having been filled in by an agent.
    Agnostic to the actual fields in the empty form
    """

    def __init__(self, doc_fields, w, h):
        self.fields = doc_fields
        self.marks = []
        self.w = w
        self.h = h

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
            

    # def pop_random_k_deterministic(self, k):
    #     """Edits the doc state IN PLACE and pops/returns a random set of k fields"""
    #     def get_hashable(field):
    #         return field["field_name"] + str(field["bbox"]["x"]) + str(field["bbox"]["y"] + field["bbox"]["height"] + field["bbox"]["width"])
    #     hashed = sorted(self.fields, key=lambda x: hashlib.md5(get_hashable(x)).encode()).hexdigest()
    #     popped = hashed[-k:]
    #     self.marks = self.marks[:-k]
    #     return popped


