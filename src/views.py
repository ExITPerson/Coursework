import os
from collections import defaultdict
from datetime import datetime
import json
import pandas as pd
import requests
from src.utils import get_data_from_xlsx, date_formater, open_json
from dotenv import load_dotenv


load_dotenv()

API_KEY_RATE = os.getenv("API_KEY_RATE")

API_KEY_STOCK = os.getenv("API_KEY_STOCK")


def greeting():
    time = datetime.now().hour

    if 4 <= time < 12:
        return "Доброе утро"
    elif 12 <= time < 16:
        return "Добрый день"
    elif 16 <= time <= 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"



def info_on_the_card(data: pd.DataFrame, date):
    date_to = date.replace(day=1)
    try:
        operations = data[pd.notnull(data["Номер карты"])].to_dict("records")
    except Exception as ex:
        return []

    try:
        card_operations = [{operation["Номер карты"]: operation["Сумма операции"]}
                           for operation in operations
            if date_to <= datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S").date() <= date
                           and operation["Сумма операции"] < 0]
    except TypeError as te:
        raise TypeError("Не правильный формат даты")

    dd = defaultdict(list)
    for card in card_operations:
        for k, v in card.items():
            dd[k].append(v)

    result = [{
        "last_digits": k[1:],
        "total_spent": round(-sum(v), 2),
        "cashback": round((-sum(v) / 100),2)}
        for k, v in dd.items()]
    return result


def get_top_five_transactions(data, date):
    date_to = date.replace(day=1)
    operations = data.to_dict("records")

    try:
        sort_list = sorted([operation for operation in operations
                            if date_to <=
                            datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S").date() <= date
                            and operation["Сумма операции"] < 0],
                           key=lambda x: x["Сумма операции"], reverse=False)
    except TypeError as te:
        raise TypeError("Не корректные данные")

    top_transactions = [{
                    "date":
                        datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y"),
                    "amount": -i["Сумма операции"],
                    "category": i["Категория"],
                    "description": i["Описание"]
                } for i in sort_list[0:5]]

    return top_transactions


def exchange_rate():
    currency_user = open_json("user_settings.json")

    exchange = []
    for currency in currency_user["user_currencies"]:
        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {"apikey": API_KEY_RATE}
        payload = {
            "amount": 1,
            "from": currency,
            "to": "RUB",}
        response = requests.get(url, headers=headers, params=payload)

        if response.status_code == 200:
            exchange.append({
                "currency": currency,
                "rate": round(response.json()["result"], 2)
            })
        else:
            raise BaseException(response.status_code)
    return exchange


def stock_quotes():
    stocks = open_json("user_settings.json")

    quotes = []
    for stock in stocks["user_stocks"]:
        url = f"http://api.marketstack.com/v1/tickers/{stock}/intraday/latest"
        params = {"access_key": API_KEY_STOCK}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            quotes.append({"stock": stock, "price": round(response.json()["last"], 2)})
        else:
            raise BaseException(response.status_code)

    return quotes


# data = get_data_from_xlsx("data/operations_t.xlsx")


def get_the_end_result(date_user):
    date = date_formater(date_user).date()
    greet = greeting()
    cards = info_on_the_card(data, date)
    top_transactions = get_top_five_transactions(data, date)
    rate = exchange_rate()
    stocks = stock_quotes()

    result = {
        "greeting": greet,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": rate,
        "stock_prices": stocks,
    }

    return json.dumps(result, ensure_ascii=False, indent=4)

# date = "2024-11-11 00:00:00"
#
# if __name__ == "__main__":
#     print(get_the_end_result(date))


