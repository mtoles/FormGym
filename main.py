import fields
import user_features
import annotations
import models
import actions
from tasks import ImagePdfFill
from doc_state import DocState
from utils import *

from tqdm import tqdm
import argparse
from copy import deepcopy
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str)
parser.add_argument("--doc_format", type=str)
parser.add_argument("--task", type=str)
# New argument to take a list of PNG file paths
parser.add_argument(
    "--file_ids", type=str, nargs="+", help="List of file ids, e.g. `al_0_0`"
)
parser.add_argument("--k_missing_fields", type=int, default=1)
args = parser.parse_args()

VALID_TASKS = [
    "AutoLoan-Full",
    "AutoLoan-Iterative",
]

assert args.task in VALID_TASKS

# To collect metrics for each file
metrics_summary = []


# Iterate over each provided PNG file
for i, fid in enumerate(args.file_ids):
    ### User setup
    user_profile = user_features.UserProfile(i)
    nl_profile = "\n".join(user_profile.get_nl_profile())

    ### Document setup
    png_path = f"pngs/{fid}.png"
    blank_img = Image.open(png_path)
    annot_path = f"annotations/all-al/{fid}.json"
    annots = annotations.read_annotations(annot_path)

    # Reset document state for each image
    doc_fields = annots
    doc_state = DocState(doc_fields)
    action_count = 0

    ### Task setup
    if args.task == "AutoLoan-Full":
        flow = FlowEnum.full.value
        img_pdf_fill_task = ImagePdfFill()
    elif args.task == "AutoLoan-Iterative":
        flow = FlowEnum.iterative.value
        img_pdf_fill_task = ImagePdfFill()
        cheater_model = models.CheaterModel(
            doc_state=doc_state, user_profile=user_profile
        )
        cheater_gens = cheater_model.forward(
            nl_profile=nl_profile,
            doc_image=blank_img,
            available_actions=["PlaceText"],
            # flow=FlowEnum.full.value,
        )
        doc_state = actions.update_doc_state(
            doc_state=doc_state, agent_generations=cheater_gens
        )

        new_doc_state = deepcopy(doc_state)
        # change change all mark creators to "prefilled"

        for i in range(len(new_doc_state.marks)):
            new_doc_state.marks[i]["creator"] = actions.CreatorEnum.prefilled.value
        print(f"before: {len(doc_state.marks)}")
        popped_fields = new_doc_state.pop_last_k_fields(
            k=args.k_missing_fields
        )  # edits in place
        doc_state = new_doc_state

    assert flow in [e.value for e in FlowEnum]

    ### Do the task
    while True:
        if args.model_name == "cheater":
            model = models.CheaterModel(doc_state=doc_state, user_profile=user_profile)
        elif args.model_name.lower().startswith("gpt"):
            model = models.GptModelE2E(model_name=args.model_name, draw_grid=True)
        else:
            raise ValueError(f"Unknown model name: {args.model_name}")

        current_state_img = models.get_image_of_state(
            doc_state=doc_state,
            blank_img=blank_img,
        )

        agent_generations = model.forward(
            nl_profile=nl_profile,
            doc_image=current_state_img,  # Use current PNG file
            available_actions=["PlaceText"],
            flow=flow,
        )
        # agent_generations =
        if flow == FlowEnum.iterative.value:
            agent_generations = agent_generations[:1]

        # Update document state based on agent outputs
        for gen in agent_generations:
            if gen["action"] == "Terminate":
                break
            doc_state = actions.update_doc_state(
                doc_state=doc_state, agent_generations=[gen]
            )

        # Break if we've filled at least 2 * k fields or if we are in full flow
        if action_count >= 2 * args.k_missing_fields or flow == FlowEnum.full.value:
            break

        action_count += 1

    # Evaluate results for the current image
    result = img_pdf_fill_task.eval(user_profile=user_profile, doc_state=doc_state)
    overall_acc = sum([f["correct"] for f in result.fields]) / len(result.fields)

    # Optional: visualize predictions for the current image
    models.visualize_preds(
        # preds=agent_generations,
        doc_state=doc_state,
        fields=result.fields,
        img=blank_img,
    )

    # Save metrics for the current file
    metrics_summary.append(
        {
            "png_file": png_path,
            "overall_accuracy": overall_acc,
            "action_count": action_count,
        }
    )

# Summarize metrics for all processed images
print("Summary of Metrics:")
for metrics in metrics_summary:
    print(
        f"File: {metrics['png_file']}, Overall Accuracy: {metrics['overall_accuracy']:.2f}, Actions: {metrics['action_count']}"
    )
