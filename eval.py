import fields
import form_state
import user_features
import annotations
import models

### Setup ###
form_state = form_state.FormState()
user_profile = user_features.UserProfile(0)

annots = annotations.read_annotations("annotations/one-file/al_1_0.json")

### Define the doc ###
# doc_fields = [fields.AutoAmountRequested(0.1, 0.1, 0.1, 0.1)]

doc_fields = annots

doc = fields.Doc(doc_fields)

### Agent makes input ###

# cheat to get the ground truth

# cheater_model = CheaterModel()

# cheater_model.forward(
#     user_profile=user_profile,
#     annotated_doc=doc,
#     doc_image_path="pngs/al_1_0.png",
# )

user_profile_str = "Your name is John Doe and you live at 123 Main St., Seattle WA 98105. You are buying a honda civic."

model = models.GptModelE2E(model_name="gpt-4o-mini-2024-07-18")

agent_input = model.forward(
    user_profile=user_profile_str,
    doc_image_path="pngs/al_1_0.png",
)

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
