import os
import fitz  # PyMuPDF

pdf_dir = "pdfs"
png_dir = "pngs"

for root, _, files in os.walk(pdf_dir):

    for f in files:
        if f.lower().endswith(".pdf"):
            pdf_path = os.path.join(root, f)
            doc = fitz.open(pdf_path)

            # Create corresponding output directory
            rel_path = os.path.relpath(root, pdf_dir)
            out_dir = os.path.join(png_dir, rel_path)
            os.makedirs(out_dir, exist_ok=True)

            for i, page in enumerate(doc):
                pix = page.get_pixmap()
                name, _ = os.path.splitext(f)
                pix.save(os.path.join(out_dir, f"{name}.png"))
