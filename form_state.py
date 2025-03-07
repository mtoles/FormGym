class FormState:
    """
    A class to represent the state of a form having been filled in by an agent.
    Agnostic to the actual fields in the empty form
    """

    def __init__(self):
        self.state = [] # a list of field values and coordinates



