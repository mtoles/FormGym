class DocState:
    """
    A class to represent the state of a form having been filled in by an agent.
    Agnostic to the actual fields in the empty form
    """

    def __init__(self, doc_fields):
        self.fields = doc_fields
        self.marks = []



