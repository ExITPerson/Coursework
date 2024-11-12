import logging

from typing import Optional

import pandas as pd

from datetime import datetime, timedelta

from statistics import mean

from utils import get_data_from_xlsx
from decorator import log


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция формирующая отчет по операциям, фильтруя по категориям, за 3 месяца
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%d.%m.%Y")
    date_to = date
    date_from = (date_to - timedelta(days=90))

    try:
        transactions_dict = get_data_from_xlsx(transactions)
    except Exception as fn:
        raise FileNotFoundError("Файл не найден")

    try:
        filtered_transactions = [transaction for transaction in transactions_dict if date_to >= datetime.strptime(
                transaction["Дата операции"], "%d.%m.%Y %H:%M:%S") >= date_from
                                 and transaction["Категория"] == category]
        return filtered_transactions
    except Exception:
        raise ValueError("Не верный формат данных")


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция формирующая отчет по средней сумме операций по дням недели
    за 3 месяца от заданной даты
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%d.%m.%Y")
    date_to = date
    date_from = (date_to - timedelta(days=90))

    try:
        transactions_dict = get_data_from_xlsx(transactions)
    except Exception as fn:
        raise FileNotFoundError("Файл не найден")
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
        return avg_daily_expenses
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
    average_daily_expenses = spending_by_weekday(transactions, date)
    for day, expenses in average_daily_expenses[0].items():
        if day in weekdays:
            weekdays_expenses[0]["Weekday"].append(expenses)
        elif day in days_off:
            weekdays_expenses[0]["Days_off"].append(expenses)

    avg_weekdays_expenses = [{k: round(mean(v),2) if len(v) != 0 else 0 for k, v in weekdays_expenses[0].items()}]
    return avg_weekdays_expenses
