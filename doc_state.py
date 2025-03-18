class DocState:
    """
    A class to represent the state of a form having been filled in by an agent.
    Agnostic to the actual fields in the empty form
    """

    def __init__(self, doc_fields):
        self.fields = doc_fields
        self.marks = []

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
