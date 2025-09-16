# form-filler

# Tool Train Setup

Download and add the FUNSD dataset to `tool/dataset/FUNSD`

https://guillaumejaume.github.io/FUNSD/download/

Preprocess with

```
python3 tool/process_annotations_and_images.py
```

For preprocessing data, you must build https://github.com/Karbo123/content-aware-fill from source to `tool/content-aware-fill`

# FormGym Eval Setup

Preprocess all files with 

```
python3 preprocess/preprocess.py
```

Then run baseline models with

```
python3 main.py --model_name gpt-4o-2024-11-20 --task oneshot --file_ids xx_0_0 --max_actions_multiplier 4 
```