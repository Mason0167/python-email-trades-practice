import os
import re
from pypdf import PdfReader

from config import *

def download_attachment(filename, filedata):
    
    # __file__ 是程式檔案路徑
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    save_path = os.path.join(base_dir, PDF_DIR)

    # Ensure the dir exists
    os.makedirs(save_path, exist_ok=True)

    # Complete file path
    file_path = os.path.join(save_path, filename)

    with open(file_path, "wb") as f:
        f.write(filedata)

    print(f"Saved: {file_path}")


def parse_pdf(file_path, password=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    file_path = os.path.join(base_dir, file_path)

    reader = PdfReader(file_path)
    if reader.is_encrypted:
        if password is None:
            raise ValueError(f"{file_path} is encrypted but no password provided")
        reader.decrypt(password)

    # Extract Text
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    print(text)