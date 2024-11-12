import logging
from idlelib.iomenu import encoding

from typing import Optional

import pandas as pd

from datetime import datetime, timedelta

from statistics import mean


logger = logging.getLogger("currency")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s_%(funcName)s:%(lineno)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция формирующая отчет по операциям, фильтруя по категориям, за 3 месяца
    """
    transactions_dict = transactions.to_dict("records")
    logger.info(f"Преобразование даты {date}")
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%d.%m.%Y")
    except Exception:
        raise ValueError("Не правильный формат даты")
    date_to = date
    date_from = (date_to - timedelta(days=90))
    logger.info("Получение даты 3 месяца назад")

    try:
        logger.info("Получение списка транзакций")
        filtered_transactions = [transaction for transaction in transactions_dict if date_to >= datetime.strptime(
                transaction["Дата операции"], "%d.%m.%Y %H:%M:%S") >= date_from
                                 and transaction["Категория"] == category]
        df = pd.DataFrame(filtered_transactions)
        return df
    except Exception as ex:
        logger.info(f"Ошибка при получении списка транзакций: {ex}")
        raise ValueError("Не верный формат данных")


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция формирующая отчет по средней сумме операций по дням недели
    за 3 месяца от заданной даты
    """
    transactions_dict = transactions.to_dict("records")
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%d.%m.%Y")
    except Exception:
        raise ValueError("Не правильный формат даты")
    date_to = date
    date_from = (date_to - timedelta(days=90))

    try:
        day_list = [
            {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}
        ]
        for transaction in transactions_dict:
            transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if (date_to >= transaction_date >= date_from
                    and transaction["Статус"] == "OK"
                    and transaction["Сумма операции"] < 0):
                weekday = datetime.strftime(transaction_date, "%A")
                day_list[0][weekday].append(transaction["Сумма операции"])

        avg_daily_expenses = [{k: round(-mean(v),2) if len(v) != 0 else 0 for k, v in day_list[0].items()}]
        df = pd.DataFrame(avg_daily_expenses)
        return df
    except Exception:
        raise ValueError("Не верный формат данных")


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция формирующая отчет по средней сумме операций по дням недели
    за 3 месяца от заданной даты
    """
    weekdays_expenses = [{"Weekday": [], "Days_off": []}]
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    days_off = ["Saturday", "Sunday"]
    average_daily_expenses = spending_by_weekday(transactions, date).to_dict("records")
    for day, expenses in average_daily_expenses[0].items():
        if day in weekdays:
            weekdays_expenses[0]["Weekday"].append(expenses)
        elif day in days_off:
            weekdays_expenses[0]["Days_off"].append(expenses)

    avg_weekdays_expenses = [{k: round(mean(v),2) if len(v) != 0 else 0 for k, v in weekdays_expenses[0].items()}]
    df = pd.DataFrame(avg_weekdays_expenses)
    return df
