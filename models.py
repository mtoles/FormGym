import fields

from PIL import Image, ImageDraw, ImageFont


def visualize_preds(preds, doc_image_path):
    # Open the image and prepare drawing context.
    """
    Visualizes prediction results on a document image by drawing text at specified coordinates.

    Parameters:
    preds (list): List of dictionaries containing predicted coordinates and value.
                  Expected keys are "x", "y", and "value", where "x" and "y" are
                  relative positions (0 to 1) and "value" is the text to be displayed.
    doc_image_path (str): File path to the document image on which predictions are to be visualized.

    The function opens the specified image, calculates the absolute position for the
    text using the relative coordinates from `preds`, and draws the text centered at
    this position in blue color. The result is saved as 'output.png' in the current directory.
    """

    img = Image.open(doc_image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Calculate absolute coordinates.
    for pred in preds:
        x = pred["x"] * width
        y = pred["y"] * height

        # Load Times New Roman font, size 10.
        try:
            font = ImageFont.truetype("Times New Roman.ttf", 50) # BROKEN
            pass
        except IOError:
            font = ImageFont.load_default()

        text = pred["field_name"] + ":\n" + str(pred["value"])
        text_x, text_y, text_w, text_h = font.getbbox(text)
        # Compute position so that the text is centered at (x, y)
        text_x = x - text_w / 2
        text_y = y - text_h / 2

        # Draw the text in blue.
        draw.text((text_x, text_y), text, fill="blue", font=font)
    # Save the image.
    img.save("output.png")


class CheaterModel:
    def __init__(self):
        pass

    def forward(self, user_profile, annotated_doc, doc_image_path):
        """
        Give the model the ground truth annotated doc so it can cheat, for data validation
        """
        preds = []
        for field in annotated_doc.fields:
            cheat_input = field["field"].get_profile_info(user_profile)
            field_mid_x = field["bbox"]["x"] + field["bbox"]["w"] / 2
            field_mid_y = field["bbox"]["y"] + field["bbox"]["h"] / 2
            preds.append(
                {
                    "x": field_mid_x,
                    "y": field_mid_y,
                    "field_name": field["field_name"],
                    "value": cheat_input,
                }
            )
        visualize_preds(preds, doc_image_path)
        return preds
