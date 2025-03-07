import json
import fields


def read_annotations(filename):

    # Load the JSON data
    with open(filename, "r") as file:
        data = json.load(file)
    doc_width = data["item"]["slots"][0]["width"]
    doc_height = data["item"]["slots"][0]["height"]
    # Extract annotations
    annotations = [
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
        }
        for annotation in data.get("annotations", [])
    ]

    return annotations
