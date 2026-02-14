from email_handler import *
from attachment_handler import *
from config import *



service = get_service(PATH, SCOPES)
messages = get_message(SENDER_ADDRESS, DATE_AFTER, SUBJECT_KEYWORDS, service)

for msg in messages:
    result = gmail_parser(msg, service)
    
    if result:
        filename, filedata = result
        
        download_attachment(filename, filedata)