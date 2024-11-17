import json
from datetime import datetime
from typing import Any

import pandas as pd


def get_data_from_xlsx(file_path: str) -> pd.DataFrame:
    """Функция для чтения данных xlsx файла"""
    df = pd.read_excel(file_path)
    return df


def date_formater(date: str) -> datetime:
    """ Функция для форматирования даты """
    try:
        date_format = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y.%m.%d")
        date = datetime.strptime(date_format, "%Y.%m.%d")
        return date
    except Exception:
        raise TypeError("Не корректная дата")


def open_json(file_path: Any) -> Any:
    """ Функция для чтения файлов JSON"""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            result = json.load(f)
            return result
        except Exception:
            raise ValueError("Не верный формат файла")
