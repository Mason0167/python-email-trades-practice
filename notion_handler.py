import requests
from datetime import date

def create_notion_page(test_trade: dict, NOTION_TOKEN, DB_ID):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    data = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "Ticker": {
                "title": [{"text": {"content": test_trade["Ticker"]}}]
            },
            "Company Name": {
                "rich_text": [{"text": {"content": test_trade["Company Name"]}}]
            },
            "Broker": {
                "rich_text": [{"text": {"content": "台新證券"}}]
            },
            "Side": {"select": {"name": test_trade["Side"]}},
            "Quantity": {"number": test_trade["Quantity"]},
            "Execution Price": {"number": test_trade["Execution Price"]},
            "Commission": {"number": test_trade["Commission"]},
            "Tax": {"number": test_trade["Tax"]},
            "Currency": {"select": {"name": test_trade["Currency"]}},
            "Total Amount": {"number": test_trade["Total Amount"]},
            "Trade Date": {
                "date": {"start": test_trade["Trade Date"], "end": None}
            }
        }
    }

    res = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=data
    )

    print(res.status_code)
    # print(res.text)


def normalize_trade(trade: dict) -> dict:
    TaxValue = trade.get("Tax")
    trade["Tax"] = int(TaxValue)
    
    # 如果沒給預設值，預設回傳 None
    TradeYear, TradeMonth, TradeDay = trade.get("Trade Date").split("/")
    if "@" in TradeDay:
        TradeDay = TradeDay.strip("@")
    trade["Trade Date"] = date(int(TradeYear), int(TradeMonth), int(TradeDay)).isoformat()


    if "," in trade["Quantity"]:
        Qty = trade["Quantity"].replace(",", "")
        trade["Quantity"] = float(Qty)
    else:
        trade["Quantity"] = float(trade["Quantity"])

    trade["Execution Price"] = float(trade["Execution Price"])
    trade["Commission"] = float(trade["Commission"])

    if '現買' in trade["Side"] or '-' in trade["Side"]:
        trade["Side"] = "Buy"
    else:
        trade["Side"] = "Sell"

    if "(" in trade["Ticker"]:
        trade["Ticker"] = trade["Ticker"].strip("()")

    TotalAmount = trade["Total Amount"].replace(",", "")
    trade["Total Amount"] = float(TotalAmount)

    return {
        "Currency": trade["Currency"],
        "Tax": trade["Tax"],
        "Trade Date": trade["Trade Date"],
        "Ticker": trade["Ticker"],
        "Quantity": trade["Quantity"],
        "Execution Price": trade["Execution Price"],
        "Commission": trade["Commission"],
        "Side": trade["Side"],
        "Company Name": trade["Company Name"],
        "Total Amount": trade["Total Amount"]
    }