export CUDA_VISIBLE_DEVICES=4,6
# export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1
export CUDA_HOME=/usr/local/cuda-12.6

MODEL_NAMES=(
    "llava"
)

MODEL_TYPE="hf"

STUDY_CONDITIONS=(
    "ours"
    "baseline"
)

start_idx=0
end_idx=3

for user_idx in $(seq $start_idx $end_idx); do
    for study_condition in ${STUDY_CONDITIONS[@]}; do
        for model_name in ${MODEL_NAMES[@]}; do
            # Text input
            python3 main.py --model_type $MODEL_TYPE --model_name $model_name --download_dir /local/data/mt/vllm_cache --task oneshot  --file_ids al_0_0 al_1_0 al_2_0 al_3_0 --study_condition $study_condition --user_idx $user_idx --note paper_results.sh
            python3 main.py --model_type $MODEL_TYPE --model_name $model_name --download_dir /local/data/mt/vllm_cache --task iterative  --file_ids al_0_0 al_1_0 al_2_0 al_3_0 --study_condition $study_condition --user_idx $user_idx --note paper_results.sh

            # Doc transfer input
            python3 main.py --model_type $MODEL_TYPE --model_name $model_name --download_dir /local/data/mt/vllm_cache --task oneshot  --file_ids al_0_0 al_1_0 al_2_0 al_3_0 --study_condition $study_condition --user_idx $user_idx --note paper_results.sh --profile_source image
            python3 main.py --model_type $MODEL_TYPE --model_name $model_name --download_dir /local/data/mt/vllm_cache --task iterative  --file_ids al_0_0 al_1_0 al_2_0 al_3_0 --study_condition $study_condition --user_idx $user_idx --note paper_results.sh --profile_source image

            # # Database
            # if [ $user_idx -eq 0 ]; then
            python3 main.py --model_type $MODEL_TYPE --model_name $model_name --download_dir /local/data/mt/vllm_cache --task iterative  --file_ids cr_0_0 cr_1_0 --study_condition $study_condition --user_idx $user_idx --note paper_results.sh

            # Funsd
            python3 main.py --model_type $MODEL_TYPE --model_name $model_name --download_dir /local/data/mt/vllm_cache --task oneshot  --file_ids funsd_test --study_condition $study_condition --user_idx $user_idx --note paper_results.sh
            # fi
        done
    done
done 