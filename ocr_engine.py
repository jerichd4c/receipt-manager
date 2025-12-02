import cv2
import pytesseract
import re
from datetime import datetime
import numpy as np
from pdf2image import convert_from_path
import os


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

POPPLER_PATH = r'C:\Program Files\poppler-25.11.0\Library\bin'

def convert_pdf_to_image(pdf_path):
    # convert the PDF to an image compatible with OpenCV
    
        try:
            # convert PDF to list of images
            pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)

            if not pages:
                raise Exception("No pages found in PDF.")
            
            # take only the first page for OCR
            first_page = pages[0]

            # convert PIL format (pdf2image) to numpy array (OpenCV)
            image_numpy = np.array(first_page)
            image_opencv = cv2.cvtColor(image_numpy, cv2.COLOR_RGB2BGR)

            return image_opencv
        except Exception as e:
            print(f"Error converting PDF to image: {e}")
            return None

def pre_process_image(image_path):
    """Detect if its PDF or image for OCR processing."""

    # 1. check file extension
    ext = os.path.splitext(image_path)[1].lower()

    img = None

    if ext == ".pdf":
        print("PDF detected, converting to image...")
        img = convert_pdf_to_image(image_path)
    else:
        img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not load image. Check the file path and format.")

    # 1. convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 2. apply binary thresholding
    text_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return text_img

def extract_text(processed_image):
    """Extract text from the pre-processed image using Tesseract OCR."""
    
    # config = "--psm 6" asumes a single uniform block of text
    text = pytesseract.image_to_string(processed_image, lang='spa', config='--psm 6')
    return text

def analize_receipt(raw_text):
    """
    Applies RegEx (Regular expressions) to find specific fields.
    obligatory fields:
    """

    data = {
        "provider": None,
        "invoice_number": None,
        "issue_date": None,
        "total_amount": None,
        "taxes": None
    }

    # 1. find date in format DD/MM/YYYY or DD-MM-YYYY 
    match_fecha = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4})|(\d{4}[/-]\d{2}[/-]\d{2})', raw_text)
    if match_fecha:
        data["issue_date"] = match_fecha.group(0)

    # 2. find Invoice Number (Patterns like 'Factura N° 123' or 'No. 12345') 
    match_invoice = re.search(r'(Factura|No\.|N°)\s*[:#]?\s*([A-Z0-9-]+)', raw_text, re.IGNORECASE)
    if match_invoice:
        data["invoice_number"] = match_invoice.group(2)

    # 3. find Amounts (Searches for numbers with decimals and currency symbols) 
    # this regex looks for "Total" followed by digits and decimals
    match_total = re.search(r'(Total|Monto|Pagar).*?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))', raw_text, re.IGNORECASE)
    if match_total:
        data["total_amount"] = match_total.group(2)

    # Note: The provider is complex. A simple strategy is to take the first line
    # if it is not empty, or look for keywords like "S.A.", "C.A.", "Ltda".
    lines = [line for line in raw_text.split('\n') if line.strip()]
    if lines:
        data["provider"] = lines[0] # Assumes the header is the name

    return data

# test block

if __name__ == "__main__":
    route = "sample_invoice.jpg"  

    print("Starting OCR process...")
    processed_img = pre_process_image(route)

    print ("Extracting text from image...")
    text= extract_text(processed_img)
    print(f"Texto Crudo detectado:\n{text[:500]}...")

    print("Structuring extracted data...")
    result= analize_receipt(text)
    print(result)