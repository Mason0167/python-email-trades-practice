import os
from config import *

def download_attachment(filename, filedata):
    
    # __file__ 是程式檔案路徑
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    save_path = os.path.join(base_dir, SAVE_DIR)

    # Ensure the dir exists
    os.makedirs(save_path, exist_ok=True)

    # Complete file path
    file_path = os.path.join(save_path, filename)

    with open(file_path, "wb") as f:
        f.write(filedata)

    print(f"Saved: {file_path}")

