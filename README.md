# form-filler

First, preprocess all files with 

```
python3 preprocess/preprocess.py
```

Then run baseline models with

```
python3 main.py --model_name gpt-4o-2024-11-20 --task oneshot --file_ids xx_0_0 --max_actions_multiplier 4 
```