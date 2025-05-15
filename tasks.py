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
        for field in tqdm(doc_state.fields, leave=False):
            field_class = getattr(fields, field["field_name"])(
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


        ### DEBUGGING ###
        # break point for debugging, allows to inspect prediction results
        # 
        # 
        # doc_id: document
        # marked_fields: all fields that have predictions
        # incorrect_fields: fields that are marked but incorrect
        # unmapped_fields: fields that are not marked
        # 
        # doc_fields: all fields in the document
        # doc_marks: all marks in the document
        
        doc_id = doc_state.doc_id
        
        doc_fields = deepcopy(doc_state.fields)
        for field in doc_fields:
            field.pop("id")
            field.pop("bbox")
            field.pop("field")
        
        marked_fields = list(
            filter(
                lambda x: x["pred"] != "",
                doc_fields,
            )
        )
        
        incorrect_fields = list(
            filter(
                lambda x: x["correct"] is False,
                marked_fields,
            )
        )
        
        doc_marks = deepcopy(doc_state.marks)
        for mark in doc_marks:
            mark.pop("creator")
            mark.pop("action")
            mark.pop("bbox")
            
        all_marks = set([y["pred"] for y in marked_fields])
        unmapped_fields = list(
            filter(
                lambda x: x['value'] not in all_marks,
                doc_marks,
            )
        )

        # break point for debugging
        return doc_state