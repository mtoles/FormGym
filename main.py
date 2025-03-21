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
    "--file_ids", type=str, nargs="+", help="List of file ids, e.g. al_0_0"
)
parser.add_argument("--k_missing_fields", type=int, default=1)
parser.add_argument("--max_actions_multiplier", type=int, default=2)
args = parser.parse_args()

# Validate the task argument
try:
    task = TaskEnum(args.task).value
except ValueError:
    raise ValueError(f"Invalid task specified: {args.task}")

# Prepare list to collect per-file data for batch processing
all_files = []
for i, fid in enumerate(args.file_ids):
    user_profile = user_features.UserProfile(i)
    nl_profile = "\n".join(user_profile.get_nl_profile())
    png_path = f"pngs/{fid}.png"
    blank_img = Image.open(png_path)
    annot_path = f"annotations/{fid}.json"
    annots = annotations.read_annotations(annot_path)
    targets = annotations.read_targets(f"targets/{fid}_targets.json")["selected_ids"]
    doc_state = DocState(annots, blank_img.width, blank_img.height)
    action_count = 0

    flow = None
    if task == TaskEnum.ONESHOT.value:
        flow = FlowEnum.ONESHOT.value
    elif task == TaskEnum.MULTISHOT.value:
        flow = FlowEnum.ITERATIVE.value
        cheater_model = models.CheaterModel(
            doc_state=doc_state, user_profile=user_profile
        )
        cheater_gens = cheater_model.forward(
            nl_profile=nl_profile,
            doc_image=blank_img,
            available_actions=["PlaceText"],
            targets=targets,
        )
        # cheater_gens["bbox"] = get_text_bbox()
        doc_state = actions.update_doc_state(
            doc_state=doc_state, agent_generations=cheater_gens
        )
        new_doc_state = deepcopy(doc_state)
        for j in range(len(new_doc_state.marks)):
            new_doc_state.marks[j]["creator"] = CreatorEnum.PREFILLED.value
        # new_doc_state.pop_last_k_fields(k=args.k_missing_fields)
        # target_fields = new_doc_state.pop_target_fields(targets=targets)
        doc_state = new_doc_state
    else:
        raise ValueError(f"Invalid task specified: {args.task}")

    all_files.append(
        {
            "user_profile": user_profile,
            "nl_profile": nl_profile,
            "png_path": png_path,
            "blank_img": blank_img,
            "doc_state": doc_state,
            "action_count": action_count,
            "flow": flow,
            "targets": targets,
        }
    )


# Create a model instance based on the model name.
BATCH_SIZE = 2
if args.model_name == "cheater":
    model = models.CheaterModel()  # Instance now will use batched inputs
elif args.model_name == "scripted":
    model = models.ScriptedModel(batch_size=BATCH_SIZE)
elif args.model_name.lower().startswith("gpt"):
    model = models.GptModelE2E(model_name=args.model_name, draw_grid=False)
else:
    raise ValueError(f"Unknown model name: {args.model_name}")
# Set batch size to 2 and process in batches
metrics_summary = []
for batch_start in range(0, len(all_files), BATCH_SIZE):
    batch = all_files[batch_start : batch_start + BATCH_SIZE]
    # 'active' flags indicate which files still need processing
    active = [True] * len(batch)
    actions_taken = [[] for _ in range(len(batch))]

    # while any(active):
    while True:
        # Build batched inputs for active files
        batch_nl = []
        batch_imgs = []
        batch_actions = []
        batch_flows = []
        active_indices = []
        for idx, file in enumerate(batch):
            if active[idx]:
                current_img = models.get_image_of_state(
                    doc_state=file["doc_state"],
                    blank_img=file["blank_img"],
                    save_path=f"tmp/{args.file_ids[idx]}-{file['action_count']}.png",
                )
                batch_nl.append(file["nl_profile"])
                batch_imgs.append(current_img)
                batch_actions.append("PlaceText")  # same for all
                batch_flows.append(file["flow"])
                active_indices.append(idx)

        # Call forward in batch (assume it now accepts list inputs)
        batch_outputs = model.forward(
            nl_profile=batch_nl,
            doc_image=batch_imgs,
            available_actions=batch_actions,
            flow=batch_flows,
        )
        if flow == FlowEnum.ITERATIVE.value:
            for gen in batch_outputs:
                # for act in gen:
                # add the text bbox
                # act["bbox"] = get_text_bbox(
                #     text=act["value"],
                #     doc_width=file["blank_img"].width,
                #     doc_height=file["blank_img"].height,
                #     cx=act["cx"],
                #     cy=act["cy"],
                # )
                if len(gen) > 1:
                    print(
                        "warning: multiple generations despite being in iterative flow"
                    )
                    gen = gen[:1]

        # Process outputs and update each file’s doc_state
        for i, idx in enumerate(active_indices):
            gens = batch_outputs[i]
            actions_taken[i].append(gens)
            for gen in gens:
                if gen["action"] == "Terminate":
                    active[idx] = False
                    models.get_image_of_state(
                        doc_state=file["doc_state"],
                        blank_img=file["blank_img"],
                        save_path=f"tmp/{args.file_ids[idx]}-{file['action_count']}.png",
                    )
                else:
                    batch[idx]["doc_state"] = actions.update_doc_state(
                        doc_state=batch[idx]["doc_state"], agent_generations=[gen]
                    )
                    batch[idx]["action_count"] += 1

        if not any(active):
            print("Terminating: no active files left")
            break
        if (
            batch[idx]["action_count"]
            >= args.max_actions_multiplier * args.k_missing_fields
        ):
            print("Terminating: action limit reached")
            break
        if batch[idx]["flow"] == FlowEnum.ONESHOT.value:
            print("Terminating: oneshot")
            break
    for idx, file in enumerate(batch):
        models.get_image_of_state(
            doc_state=file["doc_state"],
            blank_img=file["blank_img"],
            save_path=f"tmp/{args.file_ids[idx]}-last.png",
        )
    # Evaluate each processed file in the batch
    for file in batch:
        result = ImagePdfFill().eval(
            user_profile=file["user_profile"], doc_state=file["doc_state"]
        )
        overall_acc = sum([f["correct"] for f in result.fields]) / len(result.fields)
        models.visualize_preds(
            doc_state=file["doc_state"],
            fields=result.fields,
            img=file["blank_img"],
        )
        metrics_summary.append(
            {
                "png_file": file["png_path"],
                "overall_accuracy": overall_acc,
                "action_count": file["action_count"],
            }
        )

# Print summary of metrics for all processed images
print("Summary of Metrics:")
for metrics in metrics_summary:
    print(
        f"File: {metrics['png_file']}, Overall Accuracy: {metrics['overall_accuracy']:.2f}, Actions: {metrics['action_count']}"
    )
