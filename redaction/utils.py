# redaction/utils.py
import fitz  # PyMuPDF
import os
from django.utils import timezone

def redact_pdf(input_path: str, output_path: str, regions: list):
    """
    input_path: path to original pdf
    output_path: path to save redacted pdf
    regions: list of dicts:
      {'page_number':1, 'x':..., 'y':..., 'width':..., 'height':...}
    Coordinates assumed in PDF points (same units used by PyMuPDF).
    This function draws filled rectangles (black) over areas.
    """
    doc = fitz.open(input_path)
    try:
        for r in regions:
            pno = int(r['page_number']) - 1
            if pno < 0 or pno >= doc.page_count:
                continue
            page = doc[pno]
            # PyMuPDF uses coordinates (x0,y0,x1,y1) where origin is top-left in display coords.
            x0 = r['x']
            y0 = r['y']
            x1 = x0 + r['width']
            y1 = y0 + r['height']
            rect = fitz.Rect(x0, y0, x1, y1)
            # Draw filled rectangle (black)
            page.draw_rect(rect, color=(0, 0, 0), fill=(0,0,0))
        doc.save(output_path)
    finally:
        doc.close()
