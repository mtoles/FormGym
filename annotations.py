import json
import fields


def read_annotations(filename):

    # Load the JSON data
    with open(filename, "r") as file:
        data = json.load(file)
    doc_width = data["item"]["slots"][0]["width"]
    doc_height = data["item"]["slots"][0]["height"]
    # Extract annotations
    # print("missing fields: ")
    annotations = []
    missing_fields = []
    for annotation in data.get("annotations", []):
        try:
            annotations.append(
                {
                    "id": annotation["id"],
                    "field_name": annotation["name"],
                    "bbox": {
                        "x": annotation["bounding_box"]["x"] / doc_width,
                        "y": annotation["bounding_box"]["y"] / doc_height,
                        "w": annotation["bounding_box"]["w"] / doc_width,
                        "h": annotation["bounding_box"]["h"] / doc_height,
                    },
                    "field": getattr(fields, annotation["name"]),
                    "prefilled": False,  # whether to count the field in evaluation
                }
            )
        except AttributeError:
            missing_fields.append(annotation["name"])

    if missing_fields:
        print("Fields are missing:")
        print("\n".join(missing_fields))
        raise ValueError

    return annotations


def read_annotations_funsd(filename):
    # Load the JSON data
    with open(filename, "r") as file:
        data = json.load(file)
    doc_width = data["item"]["slots"][0]["width"]
    doc_height = data["item"]["slots"][0]["height"]
    # Extract annotations
    # print("missing fields: ")
    annotations = []
    missing_fields = []
    for annotation in data.get("annotations", []):
        assert annotation["properties"][0]["name"] == "key"
        key = annotation["properties"][0]["value"]
        assert annotation["properties"][1]["name"] == "value"
        value = annotation["properties"][1]["value"]

        # class VehicleMakeAndModel(BaseStringField):
        #     @classmethod
        #     def get_profile_info(cls, user_profile):
        #         return (
        #             user_profile.features.VehicleMake + " " + user_profile.features.VehicleModel
        #         )
        def new_get_profile_info(cls, user_profile):
            return value

        new_cls = fields.FieldMeta.__new__(
            fields.FieldMeta,
            key,
            (fields.BaseStringField,),
            {"get_profile_info": new_get_profile_info},
        )

        try:
            annotations.append(
                {
                    "id": annotation["id"],
                    "field_name": key,
                    "bbox": {
                        "x": annotation["bounding_box"]["x"] / doc_width,
                        "y": annotation["bounding_box"]["y"] / doc_height,
                        "w": annotation["bounding_box"]["w"] / doc_width,
                        "h": annotation["bounding_box"]["h"] / doc_height,
                    },
                    # "field": getattr(fields, annotation["name"]),
                    "field": new_cls,
                    "prefilled": False,  # whether to count the field in evaluation
                }
            )
        except AttributeError:
            missing_fields.append(annotation["name"])

    if missing_fields:
        print("Fields are missing:")
        print("\n".join(missing_fields))
        raise ValueError
    assert len(annotations) == 1
    return annotations


def read_targets(filename):
    """
    Assumed data scheme in targets/al_0_0_targets.json
    {
        "selected_ids": [
            "9c17a3d4-6acd-41d9-8c9d-88b757ccd021",
            "da1f21ce-b797-4f6e-8973-65e6ebb8c144"
        ]
    }
    """

    with open(filename, "r") as f:
        data = json.load(f)
    return data
