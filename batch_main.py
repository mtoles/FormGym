import argparse
from tqdm import tqdm
import pandas as pd
from utils import StudyConditionEnum, ProfileSourceEnum

from itertools import product
from multiprocessing import Pool

from main import main as main_func

# Batch processing script for running multiple configurations of the main function
# This script allows you to specify multiple parameters and runs the main function for each combination of parameters.
# It uses multiprocessing to speed up the execution of the main function across different configurations.

# Main difference from the original script is addition of nargs="+" to the argument parser for nearly all arguments.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, nargs="+", help="Specify model type, e.g., hf")
    parser.add_argument("--download_dir", type=str, nargs="+")
    parser.add_argument("--model_name", type=str, nargs="+")
    parser.add_argument("--doc_format", type=str, nargs="+")
    parser.add_argument("--task", type=str, nargs="+")
    # New argument to take a list of PNG file paths
    parser.add_argument(
        "--file_ids", type=str, nargs="+", help="List of file ids, e.g. al_0_0"
    )
    parser.add_argument("--k_missing_fields", type=int, nargs="+", default=1)
    parser.add_argument("--max_turns", type=int, nargs="+", default=10)
    parser.add_argument("--suggest_localizer", type=bool, nargs="+", default=False)
    # parser.add_argument("--source_doc_id", type=str, default=None)
    parser.add_argument("--user_idx", type=int, nargs="+", default=0)
    parser.add_argument(
        "--study_condition",
        type=str, nargs="+",
        help=f"Whether to use a baseline action set or our model [{', '.join([c.value for c in StudyConditionEnum])}]",
    )
    parser.add_argument(
        "--profile_source",
        type=str, nargs="+",
        help=f"Whether to use a baseline action set or our model [{', '.join([c.value for c in ProfileSourceEnum])}]",
        default=ProfileSourceEnum.TEXT.value,
    )
    parser.add_argument("--note", type=str, default="no_note")
    args = parser.parse_args()

    # mirrors the argparse structure
    params = [
        args.model_type,
        args.model_name,
        args.doc_format,
        args.task,
        [args.file_ids],
        args.k_missing_fields,
        args.max_turns,
        args.suggest_localizer,
        args.user_idx,
        args.study_condition,
        args.profile_source,
        args.note,
        args.download_dir,
    ]
    
    params = [arg if isinstance(arg, list) else [arg] for arg in params]
    
    params_cart_product = list(product(*params))
    print("Total number of tests:", len(params_cart_product))
    
    # This is a placeholder for testing main function call
    # results = list(main_func(*params_cart_product[0]))
    
    # Use multiprocessing to run the main function in parallel for each combination of parameters
    with Pool() as pool:
        results = list(tqdm(pool.starmap(main_func, params_cart_product)))
    
    # Combine all results into a single DataFrame
    overall_results = pd.concat(results, ignore_index=True)
    # written to a csv file for easy temporary storage
    overall_results.to_csv("tmp/run_summaries/batch_summary.csv", index=False)
    
    print(overall_results)