import fields
import user_features
import annotations
import models
import argparse
from form_state import FormState

from tqdm import tqdm


def main(args):
    ### Setup ###
    form_state = FormState()
    user_profile = user_features.UserProfile(0)
    nl_profile = "\n".join(user_profile.get_nl_profile())

    annots = annotations.read_annotations("annotations/one-file/al_1_0.json")

    ### Define the doc ###

    doc_fields = annots
    doc = fields.Doc(doc_fields)

    ### Agent makes input ###

    if args.model_name == "cheater":
        model = models.CheaterModel(doc=doc, user_profile=user_profile)
    elif args.model_name.lower().startswith("gpt"):
        model = models.GptModelE2E(model_name=args.model_name, draw_grid=True)
    else:
        raise ValueError(f"Unknown model name: {args.model_name}")

    agent_inputs = model.forward(
        nl_profile=nl_profile,
        doc_image_path="pngs/al_1_0.png",
    )

    form_state.state.extend(agent_inputs)

    ### Evaluate ###
    for field in tqdm(doc.fields):
        field_class = getattr(fields, field["field_name"])(
            x=field["bbox"]["x"],
            y=field["bbox"]["y"],
            w=field["bbox"]["w"],
            h=field["bbox"]["h"],
        )
        agent_inputs_inside = fields.get_inputs_inside_field(
            field=field_class, agent_inputs=agent_inputs
        )
        # concatted_input = fields.concat_agent_inputs(agent_inputs_inside)
        profile_info = field_class.get_profile_info(user_profile)
        field["gt"] = profile_info  # field_class.get_profile_info(form_state.state)
        field["pred"] = fields.concat_agent_inputs(agent_inputs_inside)
        field["correct"] = field_class.is_correct(
            agent_inputs_inside=agent_inputs_inside, profile_info=profile_info
        )

    models.visualize_preds(
        preds=agent_inputs, fields=doc.fields, doc_image_path="pngs/al_1_0.png"
    )
    overall_acc = sum([f["correct"] for f in doc.fields]) / len(doc.fields)
    print(f"Overall accuracy: {overall_acc}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str)
    args = parser.parse_args()
    main(args)
