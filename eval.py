import fields
import form_state
import user_features
import annotations
import models

### Setup ###
form_state = form_state.FormState()
user_profile = user_features.UserProfile(0)
nl_profile = "\n".join(user_profile.get_nl_profile())

annots = annotations.read_annotations("annotations/one-file/al_1_0.json")

### Define the doc ###
# doc_fields = [fields.AutoAmountRequested(0.1, 0.1, 0.1, 0.1)]

doc_fields = annots

doc = fields.Doc(doc_fields)

### Agent makes input ###

# cheat to get the ground truth

cheater_model = models.CheaterModel()

agent_input = cheater_model.forward(
    user_profile=user_profile,
    annotated_doc=doc,
    doc_image_path="pngs/al_1_0.png",
)


# model = models.GptModelE2E(model_name="gpt-4o-mini-2024-07-18")
model = models.GptModelE2E(model_name="gpt-4o-2024-08-06")

agent_input = model.forward(
    user_profile=nl_profile,
    doc_image_path="pngs/al_1_0.png",
)

models.visualize_preds(agent_input, "pngs/al_1_0.png")

# # test a single model output
# agent_input = [
#     {
#         "value": user_features.AutoAmountRequested.options[0],
#         "x": 0.338,
#         "y": 0.104,
#     }
# ]


# TODO: make a visualization of the doc

form_state.state.extend(agent_input)

### Evaluate ###
for field in doc.fields:
    if field["field_name"] != "AutoAmountRequested":
        continue
    field_class = getattr(fields, field["field_name"])(
        x=field["bbox"]["x"],
        y=field["bbox"]["y"],
        w=field["bbox"]["w"],
        h=field["bbox"]["h"],
    )
    print(field_class.is_correct(agent_input=agent_input, user_profile=user_profile))
