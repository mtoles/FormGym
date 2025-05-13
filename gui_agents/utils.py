import pymupdf
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

def view_page(page):
    pix = page.get_pixmap()
    image = pix.tobytes("png")
    img = Image.open(BytesIO(image))
    plt.rcParams['figure.figsize'] = [12, 12]  # Adjust size in inches
    plt.rcParams['figure.dpi'] = 500  # Increase DPI for higher resolution
    plt.axis('off')
    plt.imshow(img)

def view_rects(document, pnum, rects):
    if type(rects) is not list:
        rects = [rects]
        
    new_doc = pymupdf.open()
    new_doc.insert_pdf(document, from_page=pnum, to_page=pnum)
    page_copy = new_doc[0]
    for rect in rects:
        page_copy.draw_rect(rect, color=(0, 1, 0), width=2)
    view_page(page_copy)
    
def view_lines(document, pnum, lines):
    if type(lines) is not list:
        lines = [lines]
        
    new_doc = pymupdf.open()
    new_doc.insert_pdf(document, from_page=pnum, to_page=pnum)
    page_copy = new_doc[0]
    for line in lines:
        page_copy.draw_line(*line, color=(0, 1, 0), width=2)
    view_page(page_copy)
    
def view_points(document, pnum, points):
    if type(points) is not list:
        points = [points]
        
    new_doc = pymupdf.open()
    new_doc.insert_pdf(document, from_page=pnum, to_page=pnum)
    page_copy = new_doc[0]
    for point in points:
        page_copy.draw_circle(point, radius=2, color=(0, 1, 0), width=2)
    view_page(page_copy)


def get_text_in_rect(page, rect):
    blocks = page.get_text("dict")['blocks']
    spans = [span for block in blocks for line in block.get('lines', []) for span in line.get('spans', [])]
    
    def bbox_in_rect(rect, bbox):
        return rect[0] <= (bbox[2] + bbox[0]) / 2 <= rect[2] and rect[1] <= (bbox[3] + bbox[1]) / 2 <= rect[3]
    
    return [span['text'] for span in spans if 'bbox' in span and bbox_in_rect(rect, span['bbox']) and span['text'].strip()]

