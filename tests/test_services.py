from re import match

import pandas as pd
import json

import pytest

from src.services import profitable_cashback_categories


def test_profitable_cashback_categories_valid_data():
    """ Проверка с корректным df """
    df = pd.DataFrame([
        {"Категория": "Фастфуд", "Кэшбэк": 2.0, "Дата операции": "11.11.2024 20:20:20"},
        {"Категория": "Супермаркеты", "Кэшбэк": 2.0, "Дата операции": "10.11.2024 20:20:20"},
        {"Категория": "Рестораны", "Кэшбэк": 2.0, "Дата операции": "09.11.2024 20:20:20"},
        {"Категория": "Фастфуд", "Кэшбэк": 2.0, "Дата операции": "29.10.2024 20:20:20"}
    ])

    result = profitable_cashback_categories(df, "2024", "11")
    expected = json.dumps([{"Фастфуд": 2.0, "Супермаркеты": 2.0, "Рестораны": 2.0}], ensure_ascii=False)
    assert result == expected


def test_profitable_cashback_categories_empty_data():
    """ Проверка с пустым df """
    df = pd.DataFrame(columns=["Дата операции", "Кэшбэк", "Категория"])

    result = profitable_cashback_categories(df, "2024", "11")
    expected = json.dumps([{}], ensure_ascii=False)
    assert result == expected


def test_profitable_cashback_categories_no_cashback_data():
    """ Проверка если кэшбэк пустой """
    df = pd.DataFrame([
        {"Категория": "Фастфуд", "Кэшбэк": None, "Дата операции": "11.11.2024 20:20:20"},
        {"Категория": "Супермаркеты", "Кэшбэк": None, "Дата операции": "10.11.2024 20:20:20"},
    ])

    result = profitable_cashback_categories(df, "2024", "11")
    expected = json.dumps([{}], ensure_ascii=False)
    assert result == expected


def test_profitable_cashback_categories_invalid_date_format():
    """ Проверка, если в df не корректный формат даты """
    df = pd.DataFrame([
        {"Категория": "Фастфуд", "Кэшбэк": 2.0, "Дата операции": "11-11-2024 20:20:20"},
        {"Категория": "Супермаркеты", "Кэшбэк": 2.0, "Дата операции": "10-11-2024 20:20:20"},
    ])

    with pytest.raises(ValueError, match="Не корректный формат данных"):
        profitable_cashback_categories(df, "2024", "11")


def test_profitable_cashback_categories_different_month():
    """ Проверка, если данных за месяц нет """
    df = pd.DataFrame([
        {"Категория": "Фастфуд", "Кэшбэк": 2.0, "Дата операции": "11.11.2024 20:20:20"},
        {"Категория": "Супермаркеты", "Кэшбэк": 2.0, "Дата операции": "10.11.2024 20:20:20"},
        {"Категория": "Рестораны", "Кэшбэк": 2.0, "Дата операции": "09.11.2024 20:20:20"},
        {"Категория": "Фастфуд", "Кэшбэк": 2.0, "Дата операции": "08.11.2024 20:20:20"}
    ])

    result = profitable_cashback_categories(df, "2024", "10")
    expected = json.dumps([{}], ensure_ascii=False)
    assert result == expected
