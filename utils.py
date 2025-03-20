from enum import Enum


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
