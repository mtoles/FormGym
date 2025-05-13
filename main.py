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
import inspect
import re
import numpy as np
from datetime import datetime
import os
import json
from fields import FieldMeta


def get_relevant_user_features(doc_state: DocState) -> set:
    def _get_referenced_features(src_code: str) -> set:
        feat_pattern = r"feat\.([A-Za-z0-9_]+)"
        feat_matches = re.findall(feat_pattern, src_code)
        other_pattern = r"user_profile\.features\.([A-Za-z0-9_]+)"
        other_matches = re.findall(other_pattern, src_code)
        get_profile_info_pattern = r"([A-Za-z0-9_]+)\.get_profile_info"

        rec_matches = []
        get_profile_info_matches = re.findall(get_profile_info_pattern, src_code)
        for match in get_profile_info_matches:
            rec_matches.extend(
                _get_referenced_features(inspect.getsource(FieldMeta.registry[match]))
            )
        return set(feat_matches + other_matches + rec_matches)

    referenced_features = set()
    for field in doc_state.fields:
        field_cls = field["field"]
        src_code = inspect.getsource(field_cls)
        referenced_features_in_field = _get_referenced_features(src_code)
        assert referenced_features_in_field, f"No features referenced in {field_cls}"
        referenced_features.update(referenced_features_in_field)

    # drop database features (CROI)
    # referenced_features = {f for f in referenced_features if not f.startswith("CROI")}

    return referenced_features


def get_completed_source_doc(source_doc_id: str, user_idx):
    # Load the document image and annotations
    png_path = f"pngs/{source_doc_id}.png"
    blank_img = Image.open(png_path).convert("RGB")
    annot_path = f"annotations/{source_doc_id}.json"
    annots = annotations.read_annotations(annot_path)
    targets = annotations.read_targets(f"targets/{source_doc_id}_targets.json")[
        "selected_ids"
    ]

    # Create document state
    doc_state = DocState(annots, blank_img=blank_img, doc_id=source_doc_id)
    source_doc_relevant_user_features = get_relevant_user_features(doc_state)

    # Get relevant user features and create user profile
    source_doc_relevant_user_features = get_relevant_user_features(doc_state)
    user_profile = user_features.UserProfile(
        user_idx, source_doc_relevant_user_features
    )
    nl_profile = "\n".join(user_profile.get_nl_profile())

    # Create database connection
    db = SqlDb(user_profile=user_profile)

    # Create and run cheater model
    cheater_model = models.CheaterModel(doc_state=doc_state, user_profile=user_profile)
    available_actions = []

    cheater_gens = cheater_model.forward(
        nl_profile=nl_profile,
        doc_image=blank_img,
        available_actions=available_actions,
        targets=[],
        suggest_localizer=False,
    )

    # Update document state with cheater model's actions
    doc_state, feedback = actions.update_doc_state(
        doc_state=doc_state, agent_generations=cheater_gens
    )

    # Get image of filled document and save to tmp directory
    save_path = f"tmp/{source_doc_id}_gt.png"
    filled_img = doc_state.get_image_of_state(save_path=save_path)

    return filled_img, source_doc_relevant_user_features


def example_should_be_active(example):
    if example["flow"] == FlowEnum.ONESHOT.value:
        return False
    for action in example["actions"][-1]:
        if action["action"] == "Terminate":
            return False
    if len(example["doc_state"]) >= example["max_turns"]:
        return False
    return True


def mask_answer_field(blank_img: Image.Image, annots: list) -> Image.Image:
    """return an image with white rectangle over the answer field"""
    for annot in annots:
        # if annot["type"] == "answer":
        # x1, y1, x2, y2 = annot["bbox"]
        x1 = annot["bbox"]["x"] * blank_img.width
        y1 = annot["bbox"]["y"] * blank_img.height
        x2 = (annot["bbox"]["x"] + annot["bbox"]["w"]) * blank_img.width
        y2 = (annot["bbox"]["y"] + annot["bbox"]["h"]) * blank_img.height
        blank_img = blank_img.copy()
        draw = ImageDraw.Draw(blank_img)
        draw.rectangle([x1, y1, x2, y2], fill="white")
    # Save masked image to tmp directory
    # os.makedirs("tmp", exist_ok=True)
    # save_path = f"tmp/masked.png"
    # blank_img.save(save_path)
    return blank_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, help="Specify model type, e.g., hf")
    parser.add_argument("--download_dir", type=str)
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--doc_format", type=str)
    parser.add_argument("--task", type=str)
    # New argument to take a list of PNG file paths
    parser.add_argument(
        "--file_ids", type=str, nargs="+", help="List of file ids, e.g. al_0_0"
    )
    parser.add_argument("--k_missing_fields", type=int, default=1)
    parser.add_argument("--max_turns", type=int, default=10)
    parser.add_argument("--suggest_localizer", type=bool, default=False)
    # parser.add_argument("--source_doc_id", type=str, default=None)
    parser.add_argument("--user_idx", type=int, default=0)
    parser.add_argument(
        "--study_condition",
        type=str,
        help=f"Whether to use a baseline action set or our model [{', '.join([c.value for c in StudyConditionEnum])}]",
    )
    parser.add_argument(
        "--profile_source",
        type=str,
        help=f"Whether to use a baseline action set or our model [{', '.join([c.value for c in ProfileSourceEnum])}]",
        default=ProfileSourceEnum.TEXT.value,
    )
    parser.add_argument("--note", type=str, default="no_note")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")
    domain = get_domain_from_doc_id(args.file_ids[0]).value
    save_dir = f"results/{args.note}/{args.model_name.replace('/', '_')}/{domain}/{args.task}/{args.study_condition}/{args.profile_source}/u{args.user_idx}/{today}/{now}/"

    # Validate the task argument
    flow = FlowEnum(args.task).value
    study_condition = StudyConditionEnum(args.study_condition).value
    profile_source = ProfileSourceEnum(args.profile_source).value
    BATCH_SIZE = min(1, len(args.file_ids))

    # set up the db

    # Prepare list to collect per-file data for batch processing
    all_files = []
    if args.file_ids[0] == "funsd_test":
        args.file_ids = [
            f.split(".")[0]
            for f in os.listdir("annotations/funsd_test")
            if f.endswith(".json")
        ]
        assert len(args.file_ids) == 50, "there should be 50 docs"
    for i, fid in enumerate(args.file_ids):
        if "al" not in fid:
            assert (
                args.profile_source == ProfileSourceEnum.TEXT.value
            ), "Only auto loan docs dataset supports document transfer setting"
        if profile_source == ProfileSourceEnum.IMAGE.value:
            source_doc_no = (
                int(fid.split("_")[1]) - 1
            ) % 4  # use the previous doc as the source doc
            source_doc_id = f"al_{source_doc_no}_0"
        png_path = f"pngs/{fid}.png"
        print(f"Processing file: {png_path}")

        blank_img = Image.open(png_path).convert("RGB")
        if domain == DomainEnum.FUN.value:
            annot_path = f"annotations/funsd_test/{fid}.json"
            annots = annotations.read_annotations_funsd(annot_path)
            blank_img = mask_answer_field(blank_img, annots)
            targets = [x["id"] for x in annots]
        else:
            annot_path = f"annotations/{fid}.json"
            annots = annotations.read_annotations(annot_path)
            targets = annotations.read_targets(f"targets/{fid}_targets.json")[
                "selected_ids"
            ]
        doc_state = DocState(annots, blank_img=blank_img, doc_id=fid)

        if domain == DomainEnum.FUN.value:
            raise NotImplementedError

        user_profile = user_features.UserProfile(args.user_idx, relevant_user_features)
        if profile_source == ProfileSourceEnum.TEXT.value:
            nl_profile = "\n".join(
                [
                    f for f in user_profile.get_nl_profile() if not f.startswith("CROI")
                ]  # don't show features that appear in the db
            )
            source_doc_img = None
        else:
            assert (
                domain == DomainEnum.AL.value
            ), "Only auto loan docs dataset supports document transfer setting"
            # nl_profile = "<Refer to the source image for information on the user>"
            source_doc_img, source_doc_relevant_user_features = (
                get_completed_source_doc(source_doc_id, args.user_idx)
            )
            user_features_not_in_source_doc = (
                relevant_user_features - source_doc_relevant_user_features
            )
            user_profile = user_features.UserProfile(
                args.user_idx, relevant_user_features
            )  # only used for creating the nl profile, which has reduced info when source doc is provided

            nl_user_profile = user_features.UserProfile(
                args.user_idx, user_features_not_in_source_doc
            )
            nl_profile = (
                "\n".join(nl_user_profile.get_nl_profile())
                if user_features_not_in_source_doc
                else "<Refer to the source image for information on the user>"
            )

        db = SqlDb(user_profile=user_profile)

        turn_count = 0

        # flow = None
        if flow == FlowEnum.ONESHOT.value:
            # flow = FlowEnum.ONESHOT.value
            if study_condition == StudyConditionEnum.BASELINE.value:
                available_actions = AvailableActionsEnum.BASELINE_ONESHOT.value
            else:
                available_actions = AvailableActionsEnum.EXPERIMENTAL_ONESHOT.value

        elif flow == FlowEnum.ITERATIVE.value:
            # flow = FlowEnum.ITERATIVE.value
            cheater_model = models.CheaterModel(
                doc_state=doc_state, user_profile=user_profile
            )
            # available_actions = ["PlaceText", "DeleteText", "SignOrInitial", "Terminate"]
            # available_actions = list(set(actions.ActionMeta.registry.keys()) - {"InvalidAction"})
            # available_actions = ["PlaceWithLocalizer", "DeleteText", "SignOrInitial", "Terminate"]
            if study_condition == StudyConditionEnum.BASELINE.value:
                available_actions = AvailableActionsEnum.BASELINE_MULTISHOT.value
            else:
                available_actions = AvailableActionsEnum.EXPERIMENTAL_MULTISHOT.value

            cheater_gens = cheater_model.forward(
                nl_profile=nl_profile,
                doc_image=blank_img,
                available_actions=available_actions,
                targets=targets,
                suggest_localizer=False,  # irrelevant
            )
            # cheater_gens["bbox"] = get_text_bbox()
            doc_state, feedback = actions.update_doc_state(
                doc_state=doc_state, agent_generations=cheater_gens
            )
            # set the prefilled fields to true
            for field in doc_state.fields:
                if field["id"] not in targets:
                    field["prefilled"] = True

            new_doc_state = deepcopy(doc_state)
            for j in range(len(new_doc_state.marks)):
                new_doc_state.marks[j]["creator"] = CreatorEnum.PREFILLED.value
            # new_doc_state.pop_last_k_fields(k=args.k_missing_fields)
            # target_fields = new_doc_state.pop_target_fields(targets=targets)
            doc_state = new_doc_state

            #
        else:
            raise ValueError(f"Invalid task specified: {args.task}")
        if domain == DomainEnum.CR.value:
            available_actions.append("QuerySql")
        all_files.append(
            {
                "fid": fid,
                "user_profile": user_profile,
                "nl_profile": nl_profile,
                "png_path": png_path,
                "blank_img": blank_img,
                "turn_count": turn_count,
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
                "max_turns": args.max_turns,
                "feedback": [],
                "source_doc_img": source_doc_img,
            }
        )

    df = pd.DataFrame(all_files)

    # Create a model instance based on the model name.
    if args.model_type == "cheater":
        raise NotImplementedError
        model = models.CheaterModel()  # Instance now will use batched inputs
    elif args.model_type == "scripted":
        model = models.ScriptedModel(
            batch_size=BATCH_SIZE, script_name=args.file_ids[0]
        )
    elif args.model_type.lower().startswith("gpt"):
        model = models.GptModelE2E(model_name=args.model_name, draw_grid=False)
    elif args.model_type.lower().startswith("hf"):
        model = models.HFE2EModel(
            model_name=args.model_name,
            download_dir=args.download_dir,
            profile_source=args.profile_source,
            n_images=2 if args.profile_source == ProfileSourceEnum.IMAGE.value else 1,
        )
    elif args.model_type.lower().startswith("anthropic"):
        model = models.AnthropicModelE2E(model_name=args.model_name, draw_grid=False)
    else:
        raise ValueError(f"Unknown model type: {args.model_type}")
    # Set batch size to 2 and process in batches

    # Main processing loop: continue while there are active examples to process
    while not (active_df := df[df.active.apply(lambda x: x[-1])]).empty:
        # Process examples in batches for efficiency
        for batch_start in range(0, len(active_df), BATCH_SIZE):
            # Get current batch of examples
            batch = active_df.iloc[batch_start : batch_start + BATCH_SIZE]
            batch = batch.reset_index(drop=True)

            # Get model predictions for the current batch
            batch_model_outputs = model.forward(
                nl_profile=batch["nl_profile"].to_list(),
                doc_image=batch["img"].apply(lambda x: x[-1]).to_list(),
                feedback=batch["feedback"].to_list(),
                available_actions=available_actions,
                flow=batch["flow"].to_list(),
                suggest_localizer=args.suggest_localizer,  # irrelevant
                source_doc_image=batch["source_doc_img"].to_list(),
            )

            # Process each example in the batch
            for i, acts in enumerate(batch_model_outputs):
                example = batch.iloc[i]
                # Record the action taken
                example["actions"].append(acts)
                print(f"Processing example: {example['fid']}, Action: {acts}")

                # Update document state based on the action
                doc_state, feedback = actions.update_doc_state(
                    doc_state=example["doc_state"][-1],
                    agent_generations=acts,
                    db=db,
                )
                print(feedback)
                # Update example state with new document state and feedback
                example["doc_state"].append(doc_state)
                example["feedback"].append(feedback)

                # Generate and save visualization of the updated document state
                example["img"].append(
                    doc_state.get_image_of_state(
                        save_path=f"{save_dir}/images/{example['fid']}-{len(example['doc_state'])}.png"
                    )
                )

                # Update whether this example should continue being processed
                example["active"].append(example_should_be_active(example=example))
                print

    file_wise_metrics = []
    for example in df.iloc:
        doc_state = example["doc_state"][-1]
        user_profile = example["user_profile"]
        result = ImagePdfFill().eval(user_profile=user_profile, doc_state=doc_state)
        # overall_acc = sum([f["correct"] for f in result.fields]) / len(result.fields)

        correct_count = 0
        total_count = 0
        for field in result.fields:
            if field["prefilled"]:
                continue
            total_count += 1
            if field["gt"] in ["None", False, "", None, "N/A"]:
                continue
            if field["correct"]:
                correct_count += 1
        file_acc = correct_count / total_count
        models.visualize_preds(
            doc_state=doc_state,
            fields=result.fields,
            img=example["blank_img"],
        )
        file_wise_metrics.append(
            {
                "png_file": example["png_path"],
                "overall_accuracy": file_acc,
                "turn_count": example["turn_count"],
                "flow": example["flow"],
                # "study_condition": args.study_condition,
            }
        )

    # Print summary of metrics for all processed images
    print("Summary of Metrics:")
    for metrics in file_wise_metrics:
        print(
            f"File: {metrics['png_file']}, Overall Accuracy: {metrics['overall_accuracy']:.2f}, Actions: {metrics['turn_count']}"
        )

    average_acc = sum([m["overall_accuracy"] for m in file_wise_metrics]) / len(
        file_wise_metrics
    )
    acc_std = np.std([m["overall_accuracy"] for m in file_wise_metrics])

    # print average acc and acc std to a markdown file
    results_save_path = f"{save_dir}/results.md"
    data_save_path = f"{save_dir}/history.jsonl"
    # Save raw data to jsonl, keeping only json-serializable columns
    json_serializable_df = df.copy()
    # Drop columns with non-serializable objects like PIL Images
    json_serializable_df = json_serializable_df.drop(
        columns=["blank_img", "user_profile", "doc_state", "img", "source_doc_img"]
    )

    os.makedirs(os.path.dirname(data_save_path), exist_ok=True)
    json_serializable_df.to_json(data_save_path, orient="records", lines=True)

    os.makedirs(os.path.dirname(results_save_path), exist_ok=True)
    with open(results_save_path, "w") as f:
        f.write("# Form Filler Metrics Report\n\n")

        # Write input parameters
        f.write("## Input Parameters\n")
        f.write(f"- Model Type: {args.model_type}\n")
        f.write(f"- Model Name: {args.model_name}\n")
        f.write(f"- Task: {args.task}\n")
        f.write(f"- Study Condition: {args.study_condition}\n")
        f.write(f"- File IDs: {', '.join(args.file_ids)}\n")
        f.write(f"- Suggest Localizer: {args.suggest_localizer}\n\n")
        f.write(f"- User Index: {args.user_idx}\n\n")
        f.write(f"- Note: {args.note}\n\n")
        # Write summary metrics
        f.write("## Summary Metrics\n")
        f.write(f"- Average Accuracy: {average_acc:.2f}\n")
        f.write(f"- Accuracy Standard Deviation: {acc_std:.2f}\n\n")

        # Write raw data
        f.write("## Raw Data\n")
        f.write("| File | Accuracy | Actions |\n")
        f.write("|------|----------|---------|\n")
        for metrics in file_wise_metrics:
            f.write(
                f"| {metrics['png_file']} | {metrics['overall_accuracy']:.2f} | {metrics['turn_count']} |\n"
            )
