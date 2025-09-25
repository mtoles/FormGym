#!/bin/bash

# Determine the number of available GPUs from CUDA_VISIBLE_DEVICES
if [[ -z "$CUDA_VISIBLE_DEVICES" ]]; then
    echo "Error: CUDA_VISIBLE_DEVICES is not set. Please set it to specify which GPUs to use (e.g., '0,1,2,3' for 4 GPUs)."
    exit 1
fi

# Count the number of GPUs in CUDA_VISIBLE_DEVICES
CUDA_IS_AVAILABLE=$(echo "$CUDA_VISIBLE_DEVICES" | tr ',' '\n' | wc -l)

echo "Detected $CUDA_IS_AVAILABLE available GPUs from CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"

# Parse CUDA_VISIBLE_DEVICES into array of actual GPU IDs
IFS=',' read -r -a GPU_LIST <<< "$CUDA_VISIBLE_DEVICES"

# All jobs combining both HF and API models
all_jobs=(

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3 --profile_source image"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2"

"python3 main.py --model_type hf --model_name aria --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3 --profile_source image"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0 --profile_source image --gt_coordinates"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1 --profile_source image --gt_coordinates"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2 --profile_source image --gt_coordinates"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3 --profile_source image --gt_coordinates"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0 --gt_coordinates"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1 --gt_coordinates"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2 --gt_coordinates"

"python3 main.py --model_type anthropic --model_name claude-sonnet-4-20250514 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3 --gt_coordinates"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3 --profile_source image"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2"

"python3 main.py --model_type gpt --model_name gpt-5 --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3 --profile_source image"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2"

"python3 main.py --model_type hf --model_name llava --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 0"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 1"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 2"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition baseline --user_idx 3"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 0"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 1"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 2"

"python3 main.py --model_type hf --model_name molmo --download_dir /local/data/mt/vllm_cache --task iterative --file_ids al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0 --study_condition ours --user_idx 3"

)

# --- Automatic Job Sorting Function ---
# Function to determine GPU requirements for a job
get_gpu_requirements() {
    local job="$1"
    local gpus=0
    
    # Extract model type and name from the job command
    if echo "$job" | grep -q "model_type anthropic\|model_type gpt"; then
        # API models (Anthropic, GPT) don't require GPUs
        gpus=0
    elif echo "$job" | grep -q "model_name llava\|model_name molmo"; then
        # HF models require 1 GPU
        gpus=1
    elif echo "$job" | grep -q "model_name aria"; then
        # Aria model requires 2 GPUs
        gpus=2
    fi
    
    # Add one more GPU if study_condition is "ours"
    if echo "$job" | grep -q "study_condition ours"; then
        gpus=$((gpus + 1))
    fi
    
    echo $gpus
}

# Function to sort jobs into arrays based on GPU requirements
sort_jobs() {
    zero_gpu_jobs=()
    one_gpu_jobs=()
    two_gpu_jobs=()
    three_gpu_jobs=()
    skipped_jobs=()
    
    for job in "${all_jobs[@]}"; do
        # Skip empty jobs
        if [[ -z "$job" || "$job" =~ ^[[:space:]]*$ ]]; then
            continue
        fi
        
        gpu_count=$(get_gpu_requirements "$job")
        
        # Skip jobs that require more GPUs than available
        if [[ $gpu_count -gt $CUDA_IS_AVAILABLE ]]; then
            skipped_jobs+=("$job")
            echo "Skipping job requiring $gpu_count GPUs (only $CUDA_IS_AVAILABLE available): $job"
            continue
        fi
        
        case $gpu_count in
            0)
                zero_gpu_jobs+=("$job")
                ;;
            1)
                one_gpu_jobs+=("$job")
                ;;
            2)
                two_gpu_jobs+=("$job")
                ;;
            3)
                three_gpu_jobs+=("$job")
                ;;
            *)
                echo "Warning: Unknown GPU requirement ($gpu_count) for job: $job"
                ;;
        esac
    done
    
    echo "Job sorting complete:"
    echo "  0-GPU jobs: ${#zero_gpu_jobs[@]}"
    echo "  1-GPU jobs: ${#one_gpu_jobs[@]}"
    echo "  2-GPU jobs: ${#two_gpu_jobs[@]}"
    echo "  3-GPU jobs: ${#three_gpu_jobs[@]}"
    echo "  Skipped jobs: ${#skipped_jobs[@]}"
}

# Sort all jobs automatically
sort_jobs

# --- Execution Logic ---

# --- GPU Scheduling Helpers ---
is_pid_running() {
    local pid="$1"
    if [[ -z "$pid" ]]; then
        return 1
    fi
    kill -0 "$pid" 2>/dev/null
}

cleanup_finished_jobs() {
    for idx in "${!GPU_PIDS[@]}"; do
        local pid="${GPU_PIDS[$idx]}"
        if [[ -n "$pid" ]] && ! is_pid_running "$pid"; then
            GPU_PIDS[$idx]=""
        fi
    done
}

find_free_gpu_index() {
    cleanup_finished_jobs
    for idx in "${!GPU_LIST[@]}"; do
        if [[ -z "${GPU_PIDS[$idx]}" ]]; then
            echo "$idx"
            return
        fi
    done
    echo "-1"
}

join_gpu_ids() {
    local ids=""
    for i in "$@"; do
        if [[ -n "$ids" ]]; then ids+=","; fi
        ids+="${GPU_LIST[$i]}"
    done
    echo "$ids"
}

# Phase 1: Run 3-GPU jobs with dynamic scheduling based on free GPUs
if [[ ${#three_gpu_jobs[@]} -gt 0 ]]; then
    echo "--- Starting Phase 1: 3-GPU Jobs (Max $((CUDA_IS_AVAILABLE/3)) parallel) ---"
    declare -a GPU_PIDS
    for CMD in "${three_gpu_jobs[@]}"; do
        while true; do
            cleanup_finished_jobs
            free_idxs=()
            for idx in "${!GPU_LIST[@]}"; do
                if [[ -z "${GPU_PIDS[$idx]}" ]]; then
                    free_idxs+=("$idx")
                    if [[ ${#free_idxs[@]} -ge 3 ]]; then
                        break
                    fi
                fi
            done
            if [[ ${#free_idxs[@]} -ge 3 ]]; then
                GPU_IDS=$(join_gpu_ids "${free_idxs[0]}" "${free_idxs[1]}" "${free_idxs[2]}")
                echo "Running job on GPUs ${GPU_IDS}: ${CMD}"
                CUDA_VISIBLE_DEVICES=$GPU_IDS eval $CMD &
                pid=$!
                GPU_PIDS[${free_idxs[0]}]=$pid
                GPU_PIDS[${free_idxs[1]}]=$pid
                GPU_PIDS[${free_idxs[2]}]=$pid
                break
            else
                wait -n
            fi
        done
    done
    echo "Waiting for the last batch of 3-GPU jobs to finish..."
    wait
    echo "--- All 3-GPU jobs finished. ---"
fi

# Phase 2: Run 2-GPU jobs with dynamic scheduling based on free GPUs
if [[ ${#two_gpu_jobs[@]} -gt 0 ]]; then
    echo "--- Starting Phase 2: 2-GPU Jobs (Max $((CUDA_IS_AVAILABLE/2)) parallel) ---"
    declare -a GPU_PIDS
    for CMD in "${two_gpu_jobs[@]}"; do
        while true; do
            cleanup_finished_jobs
            free_idxs=()
            for idx in "${!GPU_LIST[@]}"; do
                if [[ -z "${GPU_PIDS[$idx]}" ]]; then
                    free_idxs+=("$idx")
                    if [[ ${#free_idxs[@]} -ge 2 ]]; then
                        break
                    fi
                fi
            done
            if [[ ${#free_idxs[@]} -ge 2 ]]; then
                GPU_IDS=$(join_gpu_ids "${free_idxs[0]}" "${free_idxs[1]}")
                echo "Launching job on GPUs ${GPU_IDS}: ${CMD}"
                CUDA_VISIBLE_DEVICES=$GPU_IDS eval $CMD &
                pid=$!
                GPU_PIDS[${free_idxs[0]}]=$pid
                GPU_PIDS[${free_idxs[1]}]=$pid
                break
            else
                wait -n
            fi
        done
    done
    echo "Waiting for the last batch of 2-GPU jobs to finish..."
    wait
    echo "--- All 2-GPU jobs finished. ---"
fi

# Phase 3: Run all 1-GPU jobs with parallel execution based on available GPUs
if [[ ${#one_gpu_jobs[@]} -gt 0 ]]; then
    echo "--- Starting Phase 3: 1-GPU Jobs (Max $CUDA_IS_AVAILABLE parallel) ---"
    # Track which GPU is occupied by which PID
    declare -a GPU_PIDS
    for CMD in "${one_gpu_jobs[@]}"; do
        while true; do
            idx=$(find_free_gpu_index)
            if [[ "$idx" -ge 0 ]]; then
                GPU_ID="${GPU_LIST[$idx]}"
                echo "Launching job on GPU ${GPU_ID}: ${CMD}"
                CUDA_VISIBLE_DEVICES=$GPU_ID eval $CMD &
                GPU_PIDS[$idx]=$!
                break
            else
                # Wait for any job to finish, then re-check
                wait -n
            fi
        done
    done

    # Wait for all remaining background jobs from this phase to complete
    echo "Waiting for the last batch of 1-GPU jobs to finish..."
    wait
    echo "--- All 1-GPU jobs finished. ---"
fi

# Phase 4: Run all 0-GPU jobs serially
if [[ ${#zero_gpu_jobs[@]} -gt 0 ]]; then
    echo "--- Starting Phase 4: 0-GPU Jobs (Serial) ---"
    for CMD in "${zero_gpu_jobs[@]}"; do
        echo "Running job: ${CMD}"
        eval $CMD
    done
    echo "--- All 0-GPU jobs finished. ---"
fi

echo "All experiments complete."
