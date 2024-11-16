from datetime import datetime

import pandas as pd
import pytest

from src.views import info_on_the_card


def test_positive_result():
    """ Тестирование если df и date корректные """
    df = pd.DataFrame([
        {"Номер карты": "*7228", "Сумма операции": -10, "Дата операции": "10.11.2024 23:32:01"},
        {"Номер карты": "*1888", "Сумма операции": -10, "Дата операции": "10.11.2024 23:32:01"},
        {"Номер карты": "*1888", "Сумма операции": -10, "Дата операции": "09.11.2024 23:32:01"},
        {"Номер карты": "*7228", "Сумма операции": -10, "Дата операции": "08.11.2024 23:32:01"},
        {"Номер карты": "*7228", "Сумма операции": -10, "Дата операции": "11.10.2024 23:32:01"}
    ])

    date = datetime.strptime("2024.11.11", "%Y.%m.%d").date()
    result = info_on_the_card(df, date)

    assert result == [{'cashback': 0.2, 'last_digits': '7228', 'total_spent': 20},
                      {'cashback': 0.2, 'last_digits': '1888', 'total_spent': 20}]


def test_no_data_for_the_month():
    """ Тестирование если нет данных за месяц """
    df = pd.DataFrame([
        {"Номер карты": "*7228", "Сумма операции": -10, "Дата операции": "10.10.2024 23:32:01"},
        {"Номер карты": "*1888", "Сумма операции": -10, "Дата операции": "10.10.2024 23:32:01"},
        {"Номер карты": "*1888", "Сумма операции": -10, "Дата операции": "09.10.2024 23:32:01"},
        {"Номер карты": "*7228", "Сумма операции": -10, "Дата операции": "08.10.2024 23:32:01"},
        {"Номер карты": "*7228", "Сумма операции": -10, "Дата операции": "11.09.2024 23:32:01"}
    ])

    date = datetime.strptime("2024.11.11", "%Y.%m.%d").date()
    result = info_on_the_card(df, date)

    assert result == []


def test_incorrect_date():
    """ Тестирование при неправильном формате date """
    df = pd.DataFrame([{"Номер карты": "*7228", "Сумма операции": -10, "Дата операции": "10.10.2024 23:32:01"}])
    date = datetime.strptime("2024.11.11", "%Y.%m.%d")

    with pytest.raises(TypeError, match="Не правильный формат даты"):
        info_on_the_card(df, date)


def test_empty_list_with_df():
    """ Тестирование при пустом листе в df """
    df = pd.DataFrame([])
    date = datetime.strptime("2024.11.11", "%Y.%m.%d").date()
    result = info_on_the_card(df, date)

    assert result == []


def test_empty_df():
    """ Тестирование при пустом df """
    df = pd.DataFrame(None)
    date = datetime.strptime("2024.11.11", "%Y.%m.%d").date()
    result = info_on_the_card(df, date)

    assert result == []