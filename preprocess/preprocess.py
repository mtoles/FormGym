import os
import fitz  # PyMuPDF

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
