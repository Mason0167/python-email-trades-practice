from email_handler import *
from attachment_handler import *
from config import *


# Filter emails then download the attachment
# service = get_service(PATH, SCOPES)
# messages = get_message(SENDER_ADDRESS, DATE_AFTER, SUBJECT_KEYWORDS, service)

# for msg in messages:
#     result = gmail_parser(msg, service)
    
#     if result:
#         filename, filedata = result
        
#         download_attachment(filename, filedata, PDF_DIR)

# Decrypt password-protected PDFs and ZIPs
file_path = "transaction_records\台新證券受託買賣外國有價證券確認書20260126.pdf"
parse_USA_pdf(file_path, PDF_PASSWORD)

# file_path = "transaction_records\綜合月對帳單2026年01月.pdf"
# parse_TW_pdf(file_path, PDF_PASSWORD)

# file_path = "transaction_records/TSSCO_Bill202510.zip"
# parse_zip(file_path, PDF_PASSWORD)