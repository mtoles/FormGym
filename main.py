import fields
import user_features
import annotations
import models
import actions
from tasks import ImagePdfFill
from doc_state import DocState

from tqdm import tqdm
import argparse
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str)
parser.add_argument("--doc_format", type=str)
parser.add_argument("--flow", type=str)
# New argument to take a list of PNG file paths
parser.add_argument("--file_ids", type=str, nargs="+", help="List of file ids, e.g. `al_0_0`")
args = parser.parse_args()

assert args.flow in [e.value for e in FlowEnum]

user_profile = user_features.UserProfile(0)
nl_profile = "\n".join(user_profile.get_nl_profile())

# Load annotations once (assumed to be common to all images)
img_pdf_fill_task = ImagePdfFill()

# To collect metrics for each file
metrics_summary = []

# Iterate over each provided PNG file
for fid in args.file_ids:
    png_path = f"pngs/{fid}.png"
    annot_path = f"annotations/all-al/{fid}.json"
    annots = annotations.read_annotations(annot_path)
    # Reset document state for each image
    doc_fields = annots
    doc_state = DocState(doc_fields)
    action_count = 0

    # Process the current image
    while True:
        if args.model_name == "cheater":
            model = models.CheaterModel(doc_state=doc_state, user_profile=user_profile)
        elif args.model_name.lower().startswith("gpt"):
            model = models.GptModelE2E(model_name=args.model_name, draw_grid=True)
        else:
            raise ValueError(f"Unknown model name: {args.model_name}")

        agent_generations = model.forward(
            nl_profile=nl_profile,
            doc_image_path=png_path,  # Use current PNG file
            available_actions=["PlaceText"],
            flow=args.flow,
        )

        # Update document state based on agent outputs
        doc_state = actions.update_doc_state(
            doc_state=doc_state, agent_generations=agent_generations
        )

        if agent_generations == "terminate":
            break

        action_count += 1
        break  # For now, single-turn evaluation

    # Evaluate results for the current image
    result = img_pdf_fill_task.eval(user_profile=user_profile, doc_state=doc_state)
    overall_acc = sum([f["correct"] for f in result.fields]) / len(result.fields)

    # Optional: visualize predictions for the current image
    models.visualize_preds(
        preds=agent_generations,
        fields=result.fields,
        doc_image_path=png_path,
    )

    # Save metrics for the current file
    metrics_summary.append({
        "png_file": png_path,
        "overall_accuracy": overall_acc,
        "action_count": action_count
    })

# Summarize metrics for all processed images
print("Summary of Metrics:")
for metrics in metrics_summary:
    print(f"File: {metrics['png_file']}, Overall Accuracy: {metrics['overall_accuracy']:.2f}, Actions: {metrics['action_count']}")
