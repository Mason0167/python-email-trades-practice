import os
import re
import zipfile
from bs4 import BeautifulSoup
from pypdf import PdfReader
from datetime import date


def download_attachment(filename, filedata, PDF_DIR):
    
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

def parse_USA_pdf(file_path, password=None):
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
       
    # Choose lines
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    
    trades = []

    for line in lines:
    # Filter by 2 strings
        if "202" not in line or "-" not in line:
            continue

        parts = line.split()

        cleanSide = ""
        if "-" in parts[10]:
            cleanSide = "Buy"
        else:
            cleanSide = "Sell"

        year, month, day = parts[0].split("/")
        cleanTradeDate = date(int(year), int(month), int(day)).isoformat()

        Tax = 0

        trade = {
            "Trade Date": cleanTradeDate,
            "Tax": Tax,
            "Currency": parts[2],
            "Ticker": parts[3],
            "Side": cleanSide,
            "Quantity": parts[5],
            "Execution Price": parts[6],
            "Commission": parts[8],
            "Total Amount": parts[10]
        }
        trades.append(trade)



def parse_TW_pdf(file_path, password=None):
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
        if "若有任何疑問" in page_text:
            break
        if page_text:
            text += page_text + "\n"
       
    # Choose lines
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    full_text = ""
    buffer = None

    for line in lines:
    # Filtering
    # 偵測空格: r"\s+"
        
        if re.match(r"\d{2}/\d{2}\s+", line) or re.match(r".*@", line):
            buffer = line            
            continue
        
        if buffer and ("現買" in line or "現賣" in line):
            full_text += buffer + " " + line + "\n"
            buffer = None


    filename = os.path.basename(file_path)
    # Extract year
    match = re.search(r"(\d{4})", filename)
    if not match:
        raise ValueError("Cannot find YYYY in filename")
    year = int(match.group(1))

    trades = [] # list
    trade = {} # dict

    for line in full_text.splitlines():
        parts = line.split()

        month, day = parts[0].split("/")
        day = day.strip("@")
        trade_date = date(year, int(month), int(day)).isoformat()

        cleanSide = ""
        if parts[5] == "現買":
            cleanSide = "Buy"
        else:
            cleanSide = "Sell"

        Tax = 0
        Commission = 1
        if len(parts) == 10:
            cleanTotalAmount = parts[9].strip("-")
            Commission = int(parts[4]) - int(parts[8])
        elif len(parts) == 11:
            cleanTotalAmount = parts[10].strip("-")
            Commission = int(parts[4]) - int(parts[9])
            Tax = int(parts[8])
        else:
            cleanTotalAmount = parts[8].strip("-")

        trade = {
            "Currency": "TWD",
            "Tax": Tax,
            "TradeDate": trade_date,
            "Ticker": parts[1],
            "Quantity": parts[2],
            "ExecutionPrice": parts[3],
            "Commission": Commission,
            "Side": cleanSide,
            "Company Name": parts[6],
            "TotalAmount": cleanTotalAmount
        }
        print(trade)
        trades.append(trade)
    


# 台新舊版zip
def combine_two_rows(rows):
    grouped_rows = []

    for i in range(0, len(rows), 2):

        # 保險：避免最後一筆不完整
        if i + 1 < len(rows):
            combined = rows[i] + rows[i+1]
            grouped_rows.append(combined)
    
    return grouped_rows

def parse_zip(file_path, PDF_PASSWORD=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    file_path = os.path.join(base_dir, file_path)

    with zipfile.ZipFile(file_path) as zf:
        info = zf.infolist()[0]

        with zf.open(info, pwd=PDF_PASSWORD.encode()) as f:
            html_bytes = f.read()
    
    
    html_text = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html_text, "lxml")
    inner_tbody = soup.find("tbody", id="report")

    data_rows = []

    for tr in inner_tbody.find_all("tr"):
        row_data = []

        for span in tr.find_all("span", class_="style10"):
            text = span.get_text(strip=True)

            if text:
                row_data.append(text)

        if row_data:
            if '應收付' not in row_data and '合計:' not in row_data:
                data_rows.append(row_data)

    
    grouped_rows = combine_two_rows(data_rows)

    filename = os.path.basename(file_path)
    # Extract year
    match = re.search(r"(\d{4})", filename)
    if not match:
        raise ValueError("Cannot find YYYY in filename")
    year = int(match.group(1))

    trades = []

    for row in grouped_rows:
        month, day = row[0].split("/")
        trade_date = date(year, int(month), int(day)).isoformat()

        cleanTicker = row[6].strip("()")
        cleanTotalAmount = row[8].strip("-")

        cleanSide = ""
        if row[5] == "現買":
            cleanSide = "Buy"
        else:
            cleanSide = "Sell"

        Tax = 0
        trade = {
            "Currency": "TWD",
            "Tax": Tax,
            "Trade date": trade_date,
            "Company Name": row[1],
            "Quantity": row[2],
            "Execution Price": row[3],
            "Commission": row[4],
            "Side": cleanSide,
            "Ticker": cleanTicker,
            "Total Amount": cleanTotalAmount
        }
        trades.append(trade)

        
        

    
    

    
    
    
