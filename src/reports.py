import json
import logging
from datetime import datetime, timedelta
from statistics import mean
from typing import Optional

import pandas as pd

logger = logging.getLogger("spending")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s_%(funcName)s:%(lineno)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd:
    """
    Функция формирующая отчет по операциям, фильтруя по категориям, за 3 месяца
    """
    logger.info("Преобразование df в объект Python")
    transactions_dict = transactions.to_dict("records")

    try:
        if date is None:
            logger.info("Дата не задана, получение даты в настоящем времени")
            date: datetime = datetime.now()
        else:
            logger.info(f"Преобразование даты {date} в нужный формат")
            date: datetime = datetime.strptime(date, "%d.%m.%Y")
    except Exception as ex:
        logger.error(f"Ошибка: {ex}")
        raise ValueError("Не верный формат даты")
    date_to = date
    date_from = date_to - timedelta(days=90)
    logger.info(f"Получение даты 3 месяца назад {date_from}")

    try:
        logger.info("Получение списка транзакций")

        filtered_transactions: list = []
        for transaction in transactions_dict:
            transaction_date: datetime = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if date_to >= transaction_date >= date_from and transaction["Категория"] == category:
                filtered_transactions.append(transaction)

    except Exception as ex:
        logger.info(f"Ошибка при получении списка транзакций: {ex}")
        raise ValueError("Не верный формат данных")

    logger.info("Преобразование списка в df")
    return json.dumps(filtered_transactions, ensure_ascii=False, indent=4)


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd:
    """
    Функция формирующая отчет по средней сумме операций по дням недели
    за 3 месяца от заданной даты
    """
    logger.info("Преобразование df в объект Python")
    transactions_dict = transactions.to_dict("records")
    try:
        if date is None:
            logger.info("Дата не задана, получение даты в настоящем времени")
            date: datetime = datetime.now()
        else:
            logger.info(f"Преобразование даты {date} в нужный формат")
            date: datetime = datetime.strptime(date, "%d.%m.%Y")
    except Exception as ex:
        logger.error(f"Ошибка: {ex}")
        raise ValueError("Не верный формат даты")
    date_to = date
    date_from = date_to - timedelta(days=90)
    logger.info(f"Получение даты 3 месяца назад {date_from}")

    try:
        day_list: list = [
            {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}
        ]
        logger.info("Получение списка сумм операций по фильтру")
        for transaction in transactions_dict:
            transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if (
                date_to >= transaction_date >= date_from
                and transaction["Статус"] == "OK"
                and transaction["Сумма операции"] < 0
            ):
                weekday = datetime.strftime(transaction_date, "%A")
                day_list[0][weekday].append(transaction["Сумма операции"])
    except Exception as ex:
        logger.info(f"Ошибка при получении списка транзакций: {ex}")
        raise ValueError("Не верный формат данных")

    logger.info("Преобразование списка в df")
    avg_daily_expenses = [{k: round(-mean(v), 2) if len(v) != 0 else 0 for k, v in day_list[0].items()}]
    return json.dumps(avg_daily_expenses, ensure_ascii=False, indent=4)


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd:
    """
    Функция формирующая отчет по средней сумме операций по выходным и будним дням
    за 3 месяца от заданной даты
    """
    weekdays_expenses: list = [{"Weekday": [], "Days_off": []}]
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    days_off = ["Saturday", "Sunday"]
    logger.info("Преобразование df в объект Python")
    average_daily_expenses = spending_by_weekday(transactions, date).to_dict("records")

    try:
        logger.info("Получение списка сумм операций по фильтру")
        for day, expenses in average_daily_expenses[0].items():
            if day in weekdays:
                weekdays_expenses[0]["Weekday"].append(expenses)
            elif day in days_off:
                weekdays_expenses[0]["Days_off"].append(expenses)
    except Exception as ex:
        logger.info(f"Ошибка при получении списка транзакций: {ex}")
        raise ValueError("Не верный формат данных")

    logger.info("Преобразование списка в df")
    avg_weekdays_expenses = [{k: round(mean(v), 2) if len(v) != 0 else 0 for k, v in weekdays_expenses[0].items()}]
    return json.dumps(avg_weekdays_expenses, ensure_ascii=False, indent=4)
