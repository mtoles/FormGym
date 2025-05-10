import fields
import user_features
import annotations
import models
import actions
from tasks import ImagePdfFill
from doc_state import DocState
from utils import *
from apis import SqlDb
from process_data_to_classes import process_annotations, create_dynamic_classes
import form_fields as form_field_types
from user_profile_attributes import FormUserProfile

from tqdm import tqdm
import argparse
from copy import deepcopy
from PIL import Image
import pandas as pd
import inspect
import re
import numpy as np
from pathlib import Path


def get_relevant_user_features(doc_state: DocState) -> set:
    def _get_referenced_features(src_code: str) -> set:
        feat_pattern = r"feat\.([A-Za-z0-9_]+)"
        feat_matches = re.findall(feat_pattern, src_code)
        other_pattern = r"user_profile\.features\.([A-Za-z0-9_]+)"
        other_matches = re.findall(other_pattern, src_code)
        return set(feat_matches + other_matches)

    referenced_features = set()
    for field in doc_state.fields:
        field_cls = field["field"]
        try:
            # Try to get source code for regular classes
            src_code = inspect.getsource(field_cls)
            referenced_features_in_field = _get_referenced_features(src_code)
        except (OSError, TypeError):
            # For dynamically created classes, get features from get_profile_info implementation
            if hasattr(field_cls, 'get_profile_info'):
                # Get the implementation of get_profile_info
                get_profile_info = field_cls.get_profile_info.__func__
                try:
                    src_code = inspect.getsource(get_profile_info)
                    referenced_features_in_field = _get_referenced_features(src_code)
                except (OSError, TypeError):
                    # If we can't get source code, try to get features from the class name
                    class_name = field_cls.__name__
                    # Remove form name suffix if present (e.g. "FieldName_form1" -> "FieldName")
                    if '_' in class_name:
                        class_name = class_name.rsplit('_', 1)[0]
                    # Add both the full class name and the base name as features
                    referenced_features_in_field = {class_name, field_cls.__name__}
            else:
                # If no get_profile_info method, use the class name
                class_name = field_cls.__name__
                # Remove form name suffix if present (e.g. "FieldName_form1" -> "FieldName")
                if '_' in class_name:
                    class_name = class_name.rsplit('_', 1)[0]
                referenced_features_in_field = {class_name}
        
        assert referenced_features_in_field, f"No features referenced in {field_cls}"
        referenced_features.update(referenced_features_in_field)

    return referenced_features


def example_should_be_active(example):
    if example["flow"] == FlowEnum.ONESHOT.value:
        return False
    for action in example["actions"][-1]:
        if action["action"] == "Terminate":
            return False
    if len(example["doc_state"]) >= example["max_actions"]:
        return False
    return True


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
    parser.add_argument("--max_actions_multiplier", type=int, default=2)
    parser.add_argument("--suggest_localizer", action="store_true", default=False)
    parser.add_argument(
        "--study_condition",
        type=str,
        help=f"Whether to use a baseline action set or our model [{', '.join([c.value for c in StudyConditionEnum])}]",
    )
    parser.add_argument(
        "--use_dynamic_classes",
        action="store_true",
        help="Whether to use dynamically generated classes from annotations",
    )
    parser.add_argument(
        "--dataset_name",
        type=str,
        help="Name of the dataset to use when use_dynamic_classes is enabled",
    )
    args = parser.parse_args()

    # Validate the task argument
    task = TaskEnum(args.task).value
    study_condition = StudyConditionEnum(args.study_condition).value

    # If using dynamic classes, get files from dataset directory
    if args.use_dynamic_classes:
        if not args.dataset_name:
            raise ValueError("dataset_name must be provided when use_dynamic_classes is enabled")
        print("Processing annotations and creating dynamic classes...")
        dataset_path = f"tool/dataset/{args.dataset_name}"
        all_fields, checkbox_fields, processed_jsons, all_form_names = process_annotations(dataset_path)
        create_dynamic_classes(all_fields, checkbox_fields, all_form_names)
        print(f"Created dynamic classes for {len(all_form_names)} forms")

        # Get all image files from the dataset directory
        image_dir = Path(f"{dataset_path}/images")
        file_ids = [f.stem for f in image_dir.glob("*.png")]
        if not file_ids:
            raise ValueError(f"No PNG files found in {image_dir}")
        print(f"Found {len(file_ids)} files in dataset directory")
    else:
        file_ids = args.file_ids
        if not file_ids:
            raise ValueError("file_ids must be provided when use_dynamic_classes is disabled")

    BATCH_SIZE = min(2, len(file_ids))
    # set up the db

    # Prepare list to collect per-file data for batch processing
    all_files = []
    for i, fid in enumerate(file_ids):
        if args.use_dynamic_classes:
            png_path = f"{dataset_path}/images/{fid}.png"
            bounding_boxes_path = f"tool/dataset/processed/{args.dataset_name}/bounding_boxes/{fid}.json"
            annot_path = f"tool/dataset/processed/{args.dataset_name}/annotations/{fid}_processed.json"
            targets_path = f"tool/dataset/processed/{args.dataset_name}/targets/{fid}_targets.json"
            # Get form name from the file ID (assuming format like "formname_0_0")
            form_name = fid.split('_')[0]
            annots = annotations.read_annotations_dynamic(bounding_boxes_path, annot_path, form_name)
        else:
            png_path = f"pngs/{fid}.png"
            annot_path = f"annotations/{fid}.json"
            targets_path = f"targets/{fid}_targets.json"
            annots = annotations.read_annotations(annot_path)
            
        print(f"Processing file: {png_path}")

        blank_img = Image.open(png_path).convert("RGB")
        
        targets = annotations.read_targets(targets_path)[
            "selected_ids"
        ]
        doc_state = DocState(annots, blank_img=blank_img, doc_id=fid)

        # Get form name from the file ID (assuming format like "formname_0_0")
        form_name = fid.split('_')[0]
        
        if args.use_dynamic_classes:
            # Get all form fields for this form from the dynamic registry
            form_fields = []
            for field_name, field_class in form_field_types.FormFieldMeta.registry.items():
                if field_name.endswith(f"_{form_name}"):
                    form_fields.append({
                        "field": field_class,
                        "id": field_name,
                        "prefilled": False
                    })
            # Update doc_state with dynamic form fields
            doc_state.fields = form_fields
            
            # Get relevant features and create user profile
            relevant_user_features = get_relevant_user_features(doc_state)
            user_profile = FormUserProfile(form_name=form_name)
            user_profile.relevant_features = relevant_user_features
        else:
            # Original behavior
            relevant_user_features = get_relevant_user_features(doc_state)
            user_profile = user_features.UserProfile(i, relevant_user_features)

        nl_profile = "\n".join(user_profile.get_nl_profile())

        db = SqlDb(user_profile=user_profile)

        action_count = 0

        flow = None
        if task == TaskEnum.ONESHOT.value:
            flow = FlowEnum.ONESHOT.value
            if study_condition == StudyConditionEnum.BASELINE.value:
                available_actions = AvailableActionsEnum.BASELINE_ONESHOT.value
            else:
                available_actions = AvailableActionsEnum.EXPERIMENTAL_ONESHOT.value

        elif task == TaskEnum.MULTISHOT.value:
            flow = FlowEnum.ITERATIVE.value
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
                "feedback": [],
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
            model_name=args.model_name, download_dir=args.download_dir
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
                        save_path=f"tmp/{example['fid']}-{len(example['doc_state'])}.png"
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
            if field["gt"] in ["None", False, ""]:
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
                "action_count": example["action_count"],
                "flow": example["flow"],
                # "study_condition": args.study_condition,
            }
        )

    # Print summary of metrics for all processed images
    print("Summary of Metrics:")
    for metrics in file_wise_metrics:
        print(
            f"File: {metrics['png_file']}, Overall Accuracy: {metrics['overall_accuracy']:.2f}, Actions: {metrics['action_count']}"
        )

    average_acc = sum([m["overall_accuracy"] for m in file_wise_metrics]) / len(
        file_wise_metrics
    )
    acc_std = np.std([m["overall_accuracy"] for m in file_wise_metrics])

    # print average acc and acc std to a markdown file
    with open("metrics.md", "w") as f:
        f.write("# Form Filler Metrics Report\n\n")

        # Write input parameters
        f.write("## Input Parameters\n")
        f.write(f"- Model Type: {args.model_type}\n")
        f.write(f"- Model Name: {args.model_name}\n")
        f.write(f"- Task: {args.task}\n")
        f.write(f"- Study Condition: {args.study_condition}\n")
        f.write(f"- File IDs: {', '.join(args.file_ids)}\n")
        f.write(f"- K Missing Fields: {args.k_missing_fields}\n")
        f.write(f"- Max Actions Multiplier: {args.max_actions_multiplier}\n")
        f.write(f"- Suggest Localizer: {args.suggest_localizer}\n\n")

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
                f"| {metrics['png_file']} | {metrics['overall_accuracy']:.2f} | {metrics['action_count']} |\n"
            )
