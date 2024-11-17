import json
import logging
from collections import defaultdict
from datetime import datetime
from typing import Any

import pandas as pd

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s_%(funcName)s:%(lineno)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def profitable_cashback_categories(data: pd.DataFrame, year: str, month: str) -> Any:
    """ Функция для отображения возможного кэшбэка по категориям за определенный месяц """
    logger.info(f"Преобразование даты из параметров {year} и {month}")
    date = datetime.strptime(f"{month}.{year}", "%m.%Y").strftime("%m.%Y")
    try:
        logger.info("Отбрасываем пустые значения из колонки Кэшбэк")
        df = pd.notnull(data["Кэшбэк"])
        logger.info("Преобразование данных в словарь")
        data: dict = data[df].to_dict("records")

        logger.info("Создание словаря")
        cashback_categories = [
            {d["Категория"]: d["Кэшбэк"]}
            for d in data
            if date == datetime.strptime(d["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y")
        ]
    except ValueError as ex:
        logger.error(f"Ошибка {ex}")
        raise ValueError("Не корректный формат данных")

    logger.info("Создаем список словарей для вывода")
    dd = defaultdict(list)
    for category in cashback_categories:
        for k, v in category.items():
            dd[k].append(v)
    result = [{k: sum(v) for k, v in dd.items()}]

    return json.dumps(result, ensure_ascii=False)
