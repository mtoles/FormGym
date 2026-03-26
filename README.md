# FormGym

FormGym is a benchmark for evaluating language model agents on end-to-end form completion. Given an unfilled form image and source persona data, agents must place correct text values into the appropriate fields using an editor API.

We find that field localization is the primary bottleneck for current models and introduce **FieldFinder**, a fine-tuned Florence-2 tool that enables zero-shot VLAs to accurately locate input fields, improving accuracy from ≤3% (baseline) to 23% (Claude + FieldFinder).

Paper: [FormGym: Doing Paperwork with Agents](https://arxiv.org/abs/2506.14079) (EACL 2026)

## Datasets

FormGym includes four datasets spanning scanned and digital documents:

| Dataset | Domain | Forms (train/test) | Fields (train/test) | Language | Source |
|---------|--------|-------------------|---------------------|----------|--------|
| **Auto Loans (AL)** | Financial | — / 10 | 886 / 88 | English | Manually annotated |
| **FUNSD** | Tobacco industry | 155 / 39 | — / — | English | Scanned documents |
| **XFUND** | Common Crawl | 1,112 / 100 | — / — | 7 languages | Scanned documents |
| **Form-NLU** | Australian financial | 442 / 66 | — / — | English | Digital filings |

## Task Overview

**Action space:**

| Action | Parameters | Description |
|--------|-----------|-------------|
| `PlaceText` | `cx, cy, value` | Place text at normalized coordinates (0–1) |
| `DeleteText` | `x, y` | Remove text at a location |
| `SignOrInitial` | `x, y, value` | Add a signature or initials |
| `Terminate` | — | End the episode |

With FieldFinder enabled (`--study_condition ours`), coordinate-based actions are replaced with field-name-based actions (`PlaceWithLocalizer`, `SignOrInitialWithLocalizer`).

**Evaluation modes:**

| Setting | `--task` | Description |
|---------|----------|-------------|
| One-shot | `oneshot` | Agent places all text in a single turn |
| Iterative | `iterative` | Agent gets up to `--max_turns` rounds with feedback |

**Profile source** (`--profile_source`):

| Source | Description |
|--------|-------------|
| `text` | User information as plain text (default) |
| `image` | Information from a completed source document image (Auto Loans only) |

**Study conditions** (`--study_condition`):

| Condition | Description |
|-----------|-------------|
| `baseline` | Coordinate-based actions (`PlaceText`) |
| `ours` | FieldFinder-based actions (`PlaceWithLocalizer`) |

**Metric:** Field accuracy — percentage of fields with correct values whose text center falls within the field bounding box.

## Setup


### Installation

```bash
# Clone the repo
git clone https://github.com/mtoles/form-filler.git
cd form-filler

# Create environment and install dependencies
pip install -r requirements.txt

# Preprocess PDFs to PNGs and generate target files
python preprocess/preprocess.py
```

### Preparing converted datasets (FUNSD, Form-NLU, XFUND)

For FUNSD, Form-NLU, and XFUND, additional preprocessing is required:

```bash
python preprocess/process_form-nlu.py
```

These datasets require processed annotation files in `tool/dataset/processed/`.

### FieldFinder setup (optional, for `--study_condition ours`)

FieldFinder requires building [content-aware-fill](https://github.com/Karbo123/content-aware-fill) from source into `tool/content-aware-fill/`, and a fine-tuned Florence-2 checkpoint in `tool/checkpoints/`.

## Supported Models

### API models

| `--model_type` | `--model_name` | Provider |
|----------------|---------------|----------|
| `gpt` | `gpt-5` | OpenAI |
| `gpt` | `gpt-5-mini` | OpenAI |
| `anthropic` | `claude-sonnet-4-20250514` | Anthropic |

Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` environment variables.

### Local models (vLLM)

| `--model_type` | `--model_name` | Notes |
|----------------|---------------|-------|
| `hf` | `aria` | Aria 25B |
| `hf` | `llava` | Llava 7B |
| `hf` | `molmo` | Molmo 7B |
| `hf` | `qwen_vl` | Qwen-VL |
| `hf` | `deepseek_vl2` | DeepSeek-VL2 |
| `hf` | `gemma3` | Gemma 3 |
| `hf` | `mllama` | MLlama |

Local models require a CUDA GPU and vLLM. Use `--download_dir` to set the HF model cache location.

## Usage

### API models

```bash
# GPT-4o on Auto Loans (one-shot, baseline)
python main.py \
  --model_type gpt \
  --model_name gpt-5 \
  --task oneshot \
  --domain al \
  --chosen_file_ids al_0_0 \
  --study_condition baseline \
  --profile_source text

# Claude on Auto Loans (iterative, multiple forms)
python main.py \
  --model_type anthropic \
  --model_name claude-sonnet-4-20250514 \
  --task iterative \
  --domain al \
  --chosen_file_ids al_0_0 al_1_0 al_2_0 \
  --study_condition baseline \
  --profile_source text \
  --max_turns 5

# GPT-4o on FUNSD
python main.py \
  --model_type gpt \
  --model_name gpt-5 \
  --task oneshot \
  --domain funsd \
  --chosen_file_ids 82092117 \
  --study_condition baseline
```

### Local models (vLLM)

```bash
# Molmo 7B on Auto Loans
python main.py \
  --model_type hf \
  --model_name molmo \
  --task oneshot \
  --domain al \
  --chosen_file_ids al_0_0 \
  --study_condition baseline \
  --download_dir /path/to/hf_cache
```

### With FieldFinder (experimental condition)

```bash
python main.py \
  --model_type gpt \
  --model_name gpt-5 \
  --task oneshot \
  --domain al \
  --chosen_file_ids al_0_0 \
  --study_condition ours
```

### Document transfer (image profile source, Auto Loans only)

```bash
python main.py \
  --model_type gpt \
  --model_name gpt-5 \
  --task oneshot \
  --domain al \
  --chosen_file_ids al_1_0 \
  --study_condition baseline \
  --profile_source image \
  --source_doc_id al_0_0
```

## CLI Reference

| Argument | Type | Description |
|----------|------|-------------|
| `--model_type` | str | Model backend: `gpt`, `anthropic`, `hf`, `scripted` |
| `--model_name` | str | Model identifier (e.g., `gpt-5`, `claude-sonnet-4-20250514`) |
| `--task` | str | `oneshot` or `iterative` |
| `--domain` | str | `al`, `cr`, `funsd`, `form-nlu`, `xfund` |
| `--chosen_file_ids` | str+ | Space-separated list of document IDs |
| `--study_condition` | str | `baseline` (coordinates) or `ours` (FieldFinder) |
| `--profile_source` | str | `text` (default) or `image` (AL only) |
| `--max_turns` | int | Max rounds for iterative mode (default: 3) |
| `--user_idx` | int | User profile index (default: 0) |
| `--source_doc_id` | str | Source document for image profile transfer |
| `--gt_coordinates` | flag | Pass ground-truth coordinates to the model |
| `--draw_grid` | flag | Overlay coordinate grid on form images |
| `--download_dir` | str | Download directory for HF models |
| `--use_short_dataset` | bool | Use short dataset splits (default: True) |
| `--note` | str | Note saved with results |

## Output

Results are saved to `results/<model_name>/<domain>/<task>/<study_condition>/<profile_source>/u<user_idx>/<date>/<time>/`:

- `results.md` — summary metrics (average accuracy, cost, token usage)
- `history.jsonl` — full run data per document
- `images/` — visualizations of form state at each turn

## FieldFinder Training

To train FieldFinder from scratch:

1. Download the FUNSD dataset to `tool/dataset/FUNSD` from https://guillaumejaume.github.io/FUNSD/download/
2. Build [content-aware-fill](https://github.com/Karbo123/content-aware-fill) from source to `tool/content-aware-fill`
3. Preprocess training data:
   ```bash
   python tool/process_annotations_and_images.py
   ```
4. Train:
   ```bash
   python tool/train_florence.py
   ```

## Citation

```bibtex
@inproceedings{toles2025formgym,
  title={FormGym: Doing Paperwork with Agents},
  author={Toles, Michael and others},
  booktitle={Proceedings of EACL},
  year={2026}
}
```
