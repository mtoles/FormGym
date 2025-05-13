from tqdm import tqdm
import fields
from copy import deepcopy
from utils import *


class TaskMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name != "BaseTask":
            # check for duplicates
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class BaseTask(metaclass=TaskMeta):
    def eval(self):
        raise NotImplemented


class ImagePdfFill(BaseTask):
    def eval(self, user_profile, doc_state):
        doc_state = deepcopy(doc_state)
        for field in tqdm(doc_state.fields):
            # field_class = getattr(fields, field["field_name"])(
            field_class = fields.FieldMeta.registry[field["field_name"]](
                x=field["bbox"]["x"],
                y=field["bbox"]["y"],
                w=field["bbox"]["w"],
                h=field["bbox"]["h"],
            )
            marks_inside = fields.get_inputs_inside_field(
                field=field_class, agent_generations=doc_state.marks
            )
            mark_creators_inside = [x["creator"] for x in marks_inside]
            # concatted_input = fields.concat_agent_generations(agent_generations_inside)
            profile_info = field_class.get_profile_info(user_profile)
            field["gt"] = profile_info  # field_class.get_profile_info(form_state.state)
            field["pred"] = fields.concat_agent_generations(marks_inside)
            field["correct"] = field_class.is_correct(
                agent_generations_inside=marks_inside, profile_info=profile_info
            )

        return doc_state
