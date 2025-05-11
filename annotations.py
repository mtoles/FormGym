import json
import fields
import form_fields as form_field_types
from process_data_to_classes import normalize_field_name, clean_class_name


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
                    "prefilled": False,# whether to count the field in evaluation
                }
            )
        except AttributeError:
            missing_fields.append(annotation["name"])

    if missing_fields:
        print("Fields are missing:")
        print("\n".join(missing_fields))
        raise ValueError

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

def read_annotations_dynamic(bounding_boxes_path, form_name):
    """
    Read annotations using dynamic classes from the registry.
    
    Args:
        bounding_boxes_path: Path to the bounding boxes JSON file containing annotations
        form_name: Name of the form to get dynamic classes for
    """
    # Load the bounding boxes data
    with open(bounding_boxes_path, "r") as file:
        bbox_data = json.load(file)
    doc_width = bbox_data["item"]["slots"][0]["width"]
    doc_height = bbox_data["item"]["slots"][0]["height"]

    # Get all form fields for this form from the dynamic registry
    form_fields = {}
    for field_name, field_class in form_field_types.FormFieldMeta.registry.items():
        if field_name.endswith(f"_{form_name}"):
            # Remove the form name suffix to get the base field name
            base_name = field_name[:-len(f"_{form_name}")]
            form_fields[base_name] = field_class

    # Extract annotations
    annotations = []
    missing_fields = []

    for annotation in bbox_data.get("annotations", []):
        try:
            # Get the field class from our form-specific registry
            field_class = form_fields[annotation["name"]]
            
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
                    "field": field_class,
                    "prefilled": False,  # whether to count the field in evaluation
                }
            )
        except KeyError:
            missing_fields.append(annotation["name"])

    if missing_fields:
        print("Fields are missing:")
        print("\n".join(missing_fields))
        raise ValueError

    return annotations

