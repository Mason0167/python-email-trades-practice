from email_handler import *
from attachment_handler import *
from notion_handler import *
from config import *

from pathlib import Path

# Filter emails then download the attachment
# service = get_service(PATH, SCOPES)
# messages = get_message(SENDER_ADDRESS, DATE_AFTER, SUBJECT_KEYWORDS, service)

# for msg in messages:
#     result = gmail_parser(msg, service)
    
#     if result:
#         filename, filedata = result
        
#         download_attachment(filename, filedata, PDF_DIR)




folder_path = Path("transaction_records")

for file_path in folder_path.iterdir():
    if not file_path.is_file():
        continue

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        filename = os.path.basename(file_path)
        if "受託" in filename:
            print("\nProcessing PDF:", file_path)
            trades = parse_USA_pdf(file_path, PDF_PASSWORD)
        else:
            print("\nProcessing PDF:", file_path)
            trades = parse_TW_pdf(file_path, PDF_PASSWORD)

    elif suffix == ".zip":
        print("\nProcessing PDF:", file_path)
        trades = parse_zip(file_path, PDF_PASSWORD)

    for trade in trades:
        normalize_trade(trade)
        print("\n", trade)
        create_notion_page(trade, NOTION_TOKEN, DB_ID)