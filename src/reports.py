import logging

from typing import Optional

import pandas as pd

from datetime import datetime, timedelta

from utils import get_data_from_xlsx
from decorator import log


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция формирующая отчет по операциям,
    фильтруя по категориям, за 3 месяца
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
        filtered_transactions = []
        for transaction in transactions_dict:
            transaction_date = datetime.strptime(
                transaction["Дата операции"], "%d.%m.%Y %H:%M:%S"
            )
            if date_to >= transaction_date >= date_from and transaction["Категория"] == category:
                filtered_transactions.append(transaction)
        return filtered_transactions
    except Exception:
        raise ValueError("Не верный формат данных")


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция формирующая отчет по операциям,
    фильтруя по категориям, за 3 месяца
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
        weekday_list = [[],[],[],[],[],[],[]]
        for transaction in transactions_dict:
            transaction_date = datetime.strptime(
                transaction["Дата операции"], "%d.%m.%Y %H:%M:%S"
            )

            if (date_to >= transaction_date >= date_from
                    and transaction["Статус"] == "OK"
                    and transaction["Сумма операции"] < 0):

                weekday = datetime.weekday(transaction_date)
                weekday_list[int(weekday)].append(transaction["Сумма операции"])

        weekday_avg_expenses = [
            {
                "Понедельник": -round((sum(weekday_list[0]) / len(weekday_list[0])), 2),
                "Вторник": -round((sum(weekday_list[1]) / len(weekday_list[1])),2),
                "Среда": -round((sum(weekday_list[2]) / len(weekday_list[2])),2),
                "Четверг": -round((sum(weekday_list[3]) / len(weekday_list[3])),2),
                "Пятница": -round((sum(weekday_list[4]) / len(weekday_list[4])),2),
                "Суббота": -round((sum(weekday_list[5]) / len(weekday_list[5])),2),
                "Воскресенье": -round((sum(weekday_list[6]) / len(weekday_list[6])),2),
            }
        ]
        return weekday_avg_expenses
    except Exception:
        raise ValueError("Не верный формат данных")


print(spending_by_weekday("data/operations_t.xlsx"))