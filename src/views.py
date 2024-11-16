import json
import logging
import os
from collections import defaultdict
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import date_formater, open_json

logger = logging.getLogger("menu")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/views.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s_%(funcName)s:%(lineno)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


load_dotenv()

API_KEY_RATE = os.getenv("API_KEY_RATE")

API_KEY_STOCK = os.getenv("API_KEY_STOCK")


def greeting() -> str:
    logger.info("Получаем часы")
    time = datetime.now().hour

    logger.info("Проверяем условие и выводим результат")
    if 4 <= time < 12:
        return "Доброе утро"
    elif 12 <= time < 16:
        return "Добрый день"
    elif 16 <= time <= 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def info_on_the_card(data: pd.DataFrame, date: datetime) -> list:
    logger.info("Получаем дату начала месяца")
    date_to = date.replace(day=1)
    try:
        logger.info("Создаем данные без пустых строк")
        operations = data[pd.notnull(data["Номер карты"])].to_dict("records")
    except Exception as ex:
        logger.error(f"Ошибка {ex}")
        return []

    try:
        logger.info("Сортируем данные")
        card_operations = [
            {operation["Номер карты"]: operation["Сумма операции"]}
            for operation in operations
            if date_to <= datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S").date() <= date
            and operation["Сумма операции"] < 0
        ]
    except TypeError as te:
        logger.error(f"Ошибка {te}")
        raise TypeError("Не правильный формат даты")

    logger.info("Создаем список словарей из нужных значений")
    dd = defaultdict(list)
    for card in card_operations:
        for k, v in card.items():
            dd[k].append(v)

    logger.info("Создаем список словарей для вывода")
    result = [
        {"last_digits": k[1:], "total_spent": round(-sum(v), 2), "cashback": round((-sum(v) / 100), 2)}
        for k, v in dd.items()
    ]
    return result


def get_top_five_transactions(data: pd.DataFrame, date: datetime) -> list:
    logger.info("Получаем дату начала месяца")
    date_to = date.replace(day=1)
    logger.info("Переводим данный в формат списка словарей")
    operations = data.to_dict("records")

    try:
        logger.info("Сортируем полученный список")
        sort_list = sorted(
            [
                operation
                for operation in operations
                if date_to <= datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S").date() <= date
                and operation["Сумма операции"] < 0
            ],
            key=lambda x: x["Сумма операции"],
            reverse=False,
        )
    except TypeError as te:
        logger.error(f"Ошибка {te}")
        raise TypeError("Не корректные данные")

    logger.info("Формируем данные для вывода")
    top_transactions = [
        {
            "date": datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y"),
            "amount": -i["Сумма операции"],
            "category": i["Категория"],
            "description": i["Описание"],
        }
        for i in sort_list[0:5]
    ]

    return top_transactions


def exchange_rate() -> list:
    logger.info("Открываем пользовательские настройки")
    currency_user = open_json("user_settings.json")

    logger.info("Итерируемся по валютам из пользовательских настроек и подставляем данные для API запроса")
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
            logger.info(f"Статус код: {response.status_code}. Формируем список курса валют.")
            exchange.append({"currency": currency, "rate": round(response.json()["result"], 2)})
        else:
            logger.error(f"Ошибка, статус код: {response.status_code}")
            raise BaseException(response.status_code)
    return exchange


def stock_quotes() -> list:
    logger.info("Открываем пользовательские настройки")
    stocks = open_json("user_settings.json")

    logger.info("Итерируемся по тикерам из пользовательских настроек и подставляем данные для API запроса")
    quotes = []
    for stock in stocks["user_stocks"]:
        url = f"http://api.marketstack.com/v1/tickers/{stock}/intraday/latest"
        params = {"access_key": API_KEY_STOCK}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            logger.info(f"Статус код: {response.status_code}. Формируем данные для вывода.")
            quotes.append({"stock": stock, "price": round(response.json()["last"], 2)})
        else:
            logger.error(f"Ошибка, статус код: {response.status_code}")
            raise BaseException(response.status_code)

    return quotes


def get_the_end_result(date_user: str, data: pd.DataFrame) -> Any:
    logger.info("Получаем данные из функций для формирования JSON-ответа")
    date = date_formater(date_user).date()
    greet = greeting()
    cards = info_on_the_card(data, date)
    top_transactions = get_top_five_transactions(data, date)
    rate = exchange_rate()
    stocks = stock_quotes()

    logger.info("Формирование и отправка JSON-ответа")
    result = {
        "greeting": greet,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": rate,
        "stock_prices": stocks,
    }

    return json.dumps(result, ensure_ascii=False, indent=4)
