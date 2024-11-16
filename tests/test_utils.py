from pathlib import Path
import pandas as pd
import pytest
import json
from unittest.mock import patch, mock_open

from src.utils import get_data_from_xlsx, date_formater, open_json
from datetime import datetime


def test_get_data_from_xlsx(save_xlsx: Path) -> None:
    """Тест чтения файла xlsx"""
    data = pd.DataFrame(
        [
            {"data": "24.03.2024", "name": "Alice", "amount": 63516},
            {"data": "21.10.2024", "name": "Petr", "amount": 65712},
            {"data": "11.12.2024", "name": "Ivan", "amount": 516},
        ]
    )
    file = save_xlsx(data)
    result = get_data_from_xlsx(file)

    assert result.to_dict("records") == [
        {"data": "24.03.2024", "name": "Alice", "amount": 63516},
        {"data": "21.10.2024", "name": "Petr", "amount": 65712},
        {"data": "11.12.2024", "name": "Ivan", "amount": 516},
    ]

def test_date_formater():
    """ Тест с корректным форматом даты """
    result = date_formater("2024-11-11 01:01:01")
    assert result == datetime(2024, 11, 11, 0, 0)


def test_date_formater_error():
    """ Тест с не корректным форматом даты """
    with pytest.raises(TypeError, match="Не корректная дата"):
        date_formater("2024.11.11 01:01:01")


def test_open_json(save_json):
    data = [{"name": "Alice", "Age": 30}, {"name": "Bob", "Age": 32}]
    file = save_json(data)
    result = open_json(file)
    assert result == data

def test_open_json_error(save_xlsx):
    data = pd.DataFrame([{"name": "Alice", "Age": 30}, {"name": "Bob", "Age": 32}])
    file = save_xlsx(data)

    with pytest.raises(ValueError, match="Не верный формат файла"):
        open_json(file)
