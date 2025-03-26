import fields
import user_features
import annotations
import models
import actions
from tasks import ImagePdfFill
from doc_state import DocState
from utils import *
from apis import SqlDb

from tqdm import tqdm
import argparse
from copy import deepcopy
from PIL import Image
import pandas as pd


def example_should_be_active(example):
    if example["flow"] == FlowEnum.ONESHOT.value:
        return False
    for action in example["actions"][-1]:
        if action["action"] == "Terminate":
            return False
    if len(example["doc_state"]) >= example["max_actions"]:
        return False
    return True


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

# set up the db

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
    db = SqlDb(user_profile=user_profile)

    action_count = 0

    flow = None
    if task == TaskEnum.ONESHOT.value:
        flow = FlowEnum.ONESHOT.value
        available_actions = ["PlaceText"]
    elif task == TaskEnum.MULTISHOT.value:
        flow = FlowEnum.ITERATIVE.value
        cheater_model = models.CheaterModel(
            doc_state=doc_state, user_profile=user_profile
        )
        available_actions = ["PlaceText", "DeleteText", "SignOrInitial", "Terminate"]
        cheater_gens = cheater_model.forward(
            nl_profile=nl_profile,
            doc_image=blank_img,
            available_actions=available_actions,
            targets=targets,
        )
        # cheater_gens["bbox"] = get_text_bbox()
        doc_state, feedback = actions.update_doc_state(
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
            "fid": fid,
            "user_profile": user_profile,
            "nl_profile": nl_profile,
            "png_path": png_path,
            "blank_img": blank_img,
            "action_count": action_count,
            "flow": flow,
            "targets": targets,
            # fields calculated dynamically
            "doc_state": [doc_state],
            "active": [True],
            "img": [blank_img],
            "actions": [
                []
            ],  # fill first with empty list since no actions are taken during the prep
            "active": [True],
            "max_actions": args.max_actions_multiplier * len(targets),
            "feedback": ["[No Feedback]"],
        }
    )

df = pd.DataFrame(all_files)

# Create a model instance based on the model name.
BATCH_SIZE = 2
if args.model_name == "cheater":
    raise NotImplementedError
    model = models.CheaterModel()  # Instance now will use batched inputs
elif args.model_name == "scripted":
    model = models.ScriptedModel(batch_size=BATCH_SIZE)
elif args.model_name.lower().startswith("gpt"):
    model = models.GptModelE2E(model_name=args.model_name, draw_grid=False)
else:
    raise ValueError(f"Unknown model name: {args.model_name}")
# Set batch size to 2 and process in batches

while not (active_df := df[df.active.apply(lambda x: x[-1])]).empty:
    # active_df = df[df.active.apply(lambda x: x[-1])]
    # prep the images
    for batch_start in range(0, len(active_df), BATCH_SIZE):
        batch = active_df.iloc[batch_start : batch_start + BATCH_SIZE]
        batch = batch.reset_index(drop=True)

        batch_model_outputs = model.forward(
            nl_profile=batch["nl_profile"].to_list(),
            doc_image=batch["img"].apply(lambda x: x[-1]).to_list(),
            available_actions=available_actions,
            flow=batch["flow"].to_list(),
        )

        for i, act in enumerate(batch_model_outputs):
            example = batch.iloc[i]
            example["actions"].append(act)
            doc_state, feedback = actions.update_doc_state(
                doc_state=example["doc_state"][-1],
                agent_generations=act,
                # targets=example["targets"],
            )
            # save_path=f"tmp/{args.file_ids[idx]}-last.png",
            example["doc_state"].append(doc_state)
            example["feedback"].append(feedback)
            example["img"].append(
                models.get_image_of_state(
                    doc_state=doc_state,
                    blank_img=example["blank_img"],
                    save_path=f"tmp/{example['fid']}-{len(example['doc_state'])}.png",
                )
            )
            example["active"].append(example_should_be_active(example=example))
            print

            # any([a for a in act if a["action"] == "Terminate"])
metrics_summary = []
for example in df.iloc:
    doc_state = example["doc_state"][-1]
    user_profile = example["user_profile"]
    result = ImagePdfFill().eval(user_profile=user_profile, doc_state=doc_state)
    overall_acc = sum([f["correct"] for f in result.fields]) / len(result.fields)
    models.visualize_preds(
        doc_state=doc_state,
        fields=result.fields,
        img=example["blank_img"],
    )
    metrics_summary.append(
        {
            "png_file": example["png_path"],
            "overall_accuracy": overall_acc,
            "action_count": example["action_count"],
        }
    )

    # # Evaluate each processed file in the batch
    # for file in batch:
    #     result = ImagePdfFill().eval(
    #         user_profile=file["user_profile"], doc_state=file["doc_state"]
    #     )
    #     overall_acc = sum([f["correct"] for f in result.fields]) / len(result.fields)
    #     models.visualize_preds(
    #         doc_state=file["doc_state"],
    #         fields=result.fields,
    #         img=file["blank_img"],
    #     )
    #     metrics_summary.append(
    #         {
    #             "png_file": file["png_path"],
    #             "overall_accuracy": overall_acc,
    #             "action_count": file["action_count"],
    #         }
    #     )

# Print summary of metrics for all processed images
print("Summary of Metrics:")
for metrics in metrics_summary:
    print(
        f"File: {metrics['png_file']}, Overall Accuracy: {metrics['overall_accuracy']:.2f}, Actions: {metrics['action_count']}"
    )
print
