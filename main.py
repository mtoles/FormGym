import fields
import user_features
import annotations
import models
import actions
from tasks import ImagePdfFill
from doc_state import DocState

from tqdm import tqdm
import argparse
from utils import *


parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str)
parser.add_argument("--doc_format", type=str)
parser.add_argument("--flow", type=str)
args = parser.parse_args()

assert args.flow in [e.value for e in FlowEnum]



user_profile = user_features.UserProfile(0)
nl_profile = "\n".join(user_profile.get_nl_profile())

annots = annotations.read_annotations("annotations/all-al/al_3_0.json")
img_pdf_fill_task = ImagePdfFill()
### Define the doc ###

doc_fields = annots
doc_state = DocState(doc_fields)

### Agent makes input ###
action_count = 0
while True:
    if args.model_name == "cheater":
        model = models.CheaterModel(doc_state=doc_state, user_profile=user_profile)
    elif args.model_name.lower().startswith("gpt"):
        model = models.GptModelE2E(model_name=args.model_name, draw_grid=True)
    else:
        raise ValueError(f"Unknown model name: {args.model_name}")

    agent_generations = model.forward(
        nl_profile=nl_profile,
        doc_image_path="pngs/al_3_0.png",
        available_actions=["PlaceText"],
        flow=args.flow,
    )

    # call the various actions
    doc_state = actions.update_doc_state(
        doc_state=doc_state, agent_generations=agent_generations
    )

    if agent_generations == "terminate":
        break

    action_count += 1

    break  # TODO: multi turn evaluations


### Evaluate ###
result = img_pdf_fill_task.eval(user_profile=user_profile, doc_state=doc_state)

models.visualize_preds(
    preds=agent_generations,
    fields=result.fields,
    doc_image_path="pngs/al_1_0.png",
)
overall_acc = sum([f["correct"] for f in result.fields]) / len(result.fields)
print(f"Overall accuracy: {overall_acc}")
