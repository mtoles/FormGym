import os
from pdf2image import convert_from_path
from pathlib import Path
import platform

def get_poppler_path():
    # Check if we're on macOS
    if platform.system() == "Darwin":
        # Common Homebrew installation paths
        possible_paths = [
            "/opt/homebrew/bin/",
            "/usr/local/bin/",
            "/opt/local/bin/"
        ]
        for path in possible_paths:
            if os.path.exists(path + "pdftoppm"):
                return path
    return None

def convert_pdfs_to_pngs():
    # Get parent directory and create directories if they don't exist
    parent_dir = Path(__file__).parent.parent
    pdf_dir = parent_dir / 'pdfs'
    png_dir = parent_dir / 'pngs'
    pdf_dir.mkdir(exist_ok=True)
    png_dir.mkdir(exist_ok=True)

    # Get poppler path
    poppler_path = get_poppler_path()
    if not poppler_path:
        print("Error: Poppler not found. Please install it using:")
        print("brew install poppler")
        return

    # Get all PDF files
    pdf_files = list(pdf_dir.glob('*.pdf'))
    
    if not pdf_files:
        print("No PDF files found in the 'pdfs' directory.")
        return

    print(f"Found {len(pdf_files)} PDF files to convert.")

    # Convert each PDF
    for pdf_file in pdf_files:
        print(f"Converting {pdf_file.name}...")
        try:
            # Convert PDF to images with explicit poppler path
            images = convert_from_path(
                pdf_file,
                poppler_path=poppler_path
            )
            
            # Save each page as PNG
            for i, image in enumerate(images):
                output_file = png_dir / f"{pdf_file.stem}_page_{i+1}.png"
                image.save(output_file, 'PNG')
                print(f"Saved {output_file}")
                
        except Exception as e:
            print(f"Error converting {pdf_file.name}: {str(e)}")

    print("Conversion completed!")

if __name__ == "__main__":
    convert_pdfs_to_pngs()
