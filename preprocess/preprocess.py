import os
import fitz  # PyMuPDF
import json
import random

"""
Convert PDFs to PNGs
"""

pdf_dir = "pdfs"
png_dir = "pngs"

for root, _, files in os.walk(pdf_dir):

    for f in files:
        if f.lower().endswith(".pdf"):
            pdf_path = os.path.join(root, f)
            f_prefix = f.split(".")[0]
            doc = fitz.open(pdf_path)

            # Create corresponding output directory
            rel_path = os.path.relpath(root, pdf_dir)
            out_dir = os.path.join(png_dir, rel_path)
            os.makedirs(out_dir, exist_ok=True)

            name, _ = os.path.splitext(f)
            for i, page in enumerate(doc):
                zoom = 2
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                page_name = f"{name}_{i}.png"
                os.makedirs(os.path.join(out_dir), exist_ok=True)
                pix.save(os.path.join(out_dir, page_name))


random.seed(0)
k = 99999999  # adjust as needed

annotations_dir = "annotations"
for file_name in os.listdir(annotations_dir):
    if file_name.lower().endswith(".json"):
        file_path = os.path.join(annotations_dir, file_name)
        with open(file_path, "r") as f:
            data = json.load(f)
        ids = [ann["id"] for ann in data.get("annotations", [])]
        if len(ids) >= k:
            selected_ids = random.sample(ids, k)
        else:
            selected_ids = ids  # if fewer than k ids, take them all
        os.makedirs("targets", exist_ok=True)
        output_file = os.path.join("targets", file_name.split(".")[0] + "_targets.json")
        with open(output_file, "w") as f:
            json.dump({"selected_ids": selected_ids}, f, indent=4)
