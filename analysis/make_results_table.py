"""
Script for reading every .md file in the results directory and making a table of the results.
"""

import os
import pandas as pd
from copy import deepcopy


def get_val(file_str, key):
    assert key in file_str, f"Key {key} not found in file"
    for line in file_str.split("\n"):
        if key in line:
            return float(line.split(key + ": ")[1].strip())
    raise ValueError(f"Key {key} not found in lines")


def read_md(file_path):
    # example path: results/paper_results.sh/deepseek_vl2/al/iterative/baseline/image/u0/2025-05-15/15:18:30/results.md

    (
        _,
        # _,
        model_name,
        domain,
        tempo,
        study_condition,
        profile_source,
        user_idx,
        datestamp,
        timestamp,
        _,
    ) = file_path.split("/")

    with open(file_path, "r") as file:
        file_str = file.read()

    # lines = file_str.split("\n")

    correct_field_count = get_val(file_str, "Correct Fields Count")
    total_field_count = get_val(file_str, "Total Fields Count")
    total_placement_count = get_val(file_str, "Total Placements")

    acc_fields = correct_field_count / total_field_count
    acc_placements = correct_field_count / total_field_count

    return {
        "model_name": model_name,
        "domain": domain,
        "tempo": tempo,
        "study_condition": study_condition,
        "profile_source": profile_source,
        "user_idx": user_idx,
        "datestamp": datestamp,
        "timestamp": timestamp,
        "correct_field_count": correct_field_count,
        "total_field_count": total_field_count,
        "total_placement_count": total_placement_count,
        "acc_fields": acc_fields,
        "acc_placements": acc_placements,
    }


def main():
    results_dir = "results/"
    results = []
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                results.append(read_md(file_path))
    models = list(set([result["model_name"] for result in results]) - {"deepseek_vl2"})
    domains = list(set([result["domain"] for result in results]))
    tempos = list(set([result["tempo"] for result in results]))
    study_conditions = list(set([result["study_condition"] for result in results]))
    profile_sources = list(set([result["profile_source"] for result in results]))
    user_idxs = list(set([result["user_idx"] for result in results]))

    for model in models:
        for study_condition in study_conditions:
            for domain in domains:
                for tempo in tempos:
                    for profile_source in profile_sources:
                        for user_idx in user_idxs:
                            relevant_examples = [
                                result
                                for result in results
                                if result["model_name"] == model
                                and result["study_condition"] == study_condition
                                and result["domain"] == domain
                                and result["tempo"] == tempo
                                and result["profile_source"] == profile_source
                                and result["user_idx"] == user_idx
                            ]
                            if not relevant_examples:
                                continue

                            # Sort by timestamp to get latest result
                            latest_result = sorted(
                                relevant_examples, key=lambda x: x["timestamp"]
                            )[-1]

                            # Create multi-index row
                            index = pd.MultiIndex.from_tuples(
                                [
                                    (
                                        model,
                                        study_condition,
                                        domain,
                                        tempo,
                                        profile_source,
                                        user_idx,
                                    )
                                ],
                                names=[
                                    "model",
                                    "condition",
                                    "domain",
                                    "tempo",
                                    "profile",
                                    "user",
                                ],
                            )

                            # Create row data
                            data = {
                                "correct_fields": latest_result["correct_field_count"],
                                "total_fields": latest_result["total_field_count"],
                                "total_placements": latest_result[
                                    "total_placement_count"
                                ],
                                "acc_fields": latest_result["acc_fields"],
                                "acc_placements": latest_result["acc_placements"],
                                "timestamp": latest_result["timestamp"],
                            }

                            # Create single-row DataFrame with multi-index
                            df_row = pd.DataFrame(data, index=index)

                            # Append to results list
                            if "df_results" not in locals():
                                df_results = df_row
                            else:
                                df_results = pd.concat([df_results, df_row])
                                # print(df_results.head())
    models.sort()
    # Sort the index to avoid PerformanceWarning
    df_results = df_results.sort_index()
    # drop ones we didn't do
    # models = [x for x in models if x not in ["molmo", "deepseek_vl2"]]
    print(models)
    for metric in ["correct_fields", "total_placements"]:
        print("=" * 10 + f"{metric}" + "=" * 10)
        for model in models:
            # baseline
            args = [
                model,
                "baseline",
                # "al",
                # "cr",
                "fun",
                "oneshot",
                # "iterative",
                "text",
                # "image",
            ]
            df_b = df_results.loc[
                tuple(args), ["correct_fields", "total_fields", "total_placements"]
            ]
            print(df_b.mean()[metric])
        for model in models:
            # ours
            # args2 = [model, "ours", "al", "oneshot", "text"]
            args2 = deepcopy(args)
            args2[0] = model
            args2[1] = "ours"
            df_o = df_results.loc[
                tuple(args2), ["correct_fields", "total_fields", "total_placements"]
            ]
            print(df_o.mean()[metric])
    # for metric in ["correct_fields", "total_placements"]:
    #     print("=" * 10 + f"{metric}" + "=" * 10)
    #     for model in models:
    #         args = [
    #             model,
    #             "baseline",
    #             "al",
    #             # "cr",
    #             # "fun",
    #             "oneshot",
    #             # "iterative",
    #             "text",
    #             # "image",
    #         ]
    #         filtered_df = df_results.loc[
    #             tuple(args),
    #             :,
    #         ][["correct_fields", "total_fields", "total_placements"]]
    #         expected_len = 4
    #         assert (
    #             len(filtered_df) == expected_len
    #         ), f"Expected {expected_len} results, got {len(filtered_df)}"
    #         print(filtered_df.mean()[metric])

    #         args2 = list(args)
    #         args2[1] = "ours"
    #         args2 = tuple(args2)
    #         filtered_df2 = df_results.loc[
    #             tuple(args2),
    #             :,
    #         ][["correct_fields", "total_fields", "total_placements"]]
    #         assert (
    #             len(filtered_df2) == expected_len
    #         ), f"Expected {expected_len} results, got {len(filtered_df2)}"
    #         print(filtered_df2.mean()[metric])

    #     # total placements
    #     # print("=" * 10)
    #     # print(filtered_df.mean()["total_placements"])
    #     # print(filtered_df2.mean()["total_placements"])


if __name__ == "__main__":
    main()
