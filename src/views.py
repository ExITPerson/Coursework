import os
from collections import defaultdict
from datetime import datetime

import json
from http.client import responses

import pandas as pd

import requests

from utils import get_data_from_xlsx

from dotenv import load_dotenv

load_dotenv()

API_KEY_RATE = os.getenv("API_KEY_RATE")

API_KEY_STOCK = os.getenv("API_KEY_STOCK")


def greeting():
    time = datetime.now().strftime("%H:%M")
    if "4:00" <= time < "12:00":
        return "Доброе утро"
    elif "12:00" <= time < "16:00":
        return "Добрый день"
    elif "16:00" <= time < "00:00":
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def info_on_the_card(data: pd.DataFrame, date=None):
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y.%m.%d")
    date_to = date.replace(day=1)

    df = pd.notnull(data["Номер карты"])
    operations = data[df].to_dict("records")

    card_operations = [{operation["Номер карты"]: operation["Сумма операции"]}
                       for operation in operations
        if date_to <= datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S") <= date
                       and operation["Сумма операции"] < 0]

    dd = defaultdict(list)
    for card in card_operations:
        for k, v in card.items():
            dd[k].append(v)
    result = [{"last_digits": k[1:], "total_spent": -sum(v), "cashback": round((-sum(v) / 100),2)} for k, v in dd.items()]
    return result


print(info_on_the_card(get_data_from_xlsx("data/operations_t.xlsx")))


def get_top_five_transactions(data, date=None):
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y.%m.%d")
    date_to = date.replace(day=1)

    operations = data.to_dict("records")

    sort_transactions = [operation for operation in operations
                         if date_to <= datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S") <= date
                             and operation["Сумма операции"] < 0]

    sort_list = sorted(sort_transactions, key=lambda x: x["Сумма операции"], reverse=False)
    top_transactions = [{
                    "date":
                        datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y"),
                    "amount": -i["Сумма операции"],
                    "category": i["Категория"],
                    "discription": i["Описание"]
                } for i in sort_list[0:5]]

    return top_transactions


print(get_top_five_transactions(get_data_from_xlsx("data/operations_t.xlsx")))


def exchange_rate(setting = "json/user_settings.json"):
    with open(setting, "r", encoding="utf-8") as f:
        try:
            currency_user = json.load(f)
        except Exception as ex:
            raise ValueError("Не верный формат файла")

    exchange = []
    for currency in currency_user["user_currencies"]:
        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {"apikey": API_KEY_RATE}
        payload = {
            "amount": 1,
            "from": currency,
            "to": "RUB",
        }
        response = requests.get(url, headers=headers, params=payload)
        if response.status_code == 200:
            exchange.append({
                "currency": currency,
                "rate": round(response.json()["result"], 2)
            })
        else:
            raise BaseException(response.status_code)
    return exchange

print(exchange_rate())


def stock_quotes(setting = "json/user_settings.json"):
    with open(setting, "r", encoding="utf-8") as f:
        try:
            stocks = json.load(f)
        except Exception as ex:
            raise ValueError("Не верный формат файла")

        quotes = []
        for stock in stocks["user_stocks"]:
            url = f"http://api.marketstack.com/v1/tickers/{stock}/intraday/latest"
            params = {"access_key": API_KEY_STOCK}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                quotes.append({"stock": stock, "price": response.json()["last"]})
            else:
                raise BaseException(response.status_code)

        return quotes

print(stock_quotes())