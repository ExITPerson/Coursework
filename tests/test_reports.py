import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday

data_1 = pd.DataFrame([
    {"Дата операции": "10.11.2024 23:23:23", "Категория": "Фастфуд"},
    {"Дата операции": "09.09.2024 11:11:11", "Категория": "Перевод"},
    {"Дата операции": "09.09.2024 09:11:11", "Категория": "Фастфуд"},
    {"Дата операции": "15.08.2024 15:15:15", "Категория": "Фастфуд"}
])

def test_spending_by_category(freezer) -> None:
    """ Тестирование функции с разными аргументами """
    """ Тестирование функции с существующей категорией и датой """
    freezer.move_to("11.11.2024")
    result = spending_by_category(data_1, "Фастфуд", "10.11.2024")
    assert len(result) == 2

    """ Тестирование функции с существующей категорией и без указания даты """
    result = spending_by_category(data_1, "Перевод")
    assert len(result) == 1
    assert result.iloc[0]["Категория"] == "Перевод"

    """ Тестирование функции с категорией, которой нет в df """
    result = spending_by_category(data_1, "Рестораны")
    assert result.empty

    """ Тестирование обработки некорректного формата даты"""
    with pytest.raises(ValueError, match="Не верный формат даты"):
        spending_by_category(data_1, "Фастфуд", "2024-11-10")

    """ Тестирование функции с пустым DataFrame """
    empty_df = pd.DataFrame(columns=["Дата операции", "Категория"])
    result = spending_by_category(empty_df, "Фастфуд")
    assert result.empty

    """Тестирование функции с не верным форматом переданного df"""
    data_1_error = pd.DataFrame([{"Name": "Alice", "Age": 23}])
    with pytest.raises(ValueError, match="Не верный формат данных"):
        spending_by_workday(data_1_error, "11.11.2024")


data_2 = pd.DataFrame([
    {"Дата операции": "10.11.2024 23:23:23", "Статус": "OK", "Сумма операции": -100.0},
    {"Дата операции": "10.11.2024 11:11:11", "Статус": "OK", "Сумма операции": -200.0},
    {"Дата операции": "09.09.2024 09:11:11", "Статус": "OK", "Сумма операции": -150.0},
    {"Дата операции": "15.08.2024 15:15:15", "Статус": "FAIL", "Сумма операции": -50.0},
    {"Дата операции": "10.08.2024 12:30:30", "Статус": "OK", "Сумма операции": -300.0}
])


def test_spending_by_weekday(freezer) -> None:
    """ Тестирование работы функции """
    freezer.move_to("11.11.2024")
    """Тестирование функции с указанной датой"""
    result = spending_by_weekday(data_2, "10.11.2024")
    assert result.loc[0, "Sunday"] == 0
    assert result.loc[0, "Monday"] == 150.0

    """Тестирование функции без указания даты"""
    result = spending_by_weekday(data_2)
    expected_columns = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    assert list(result.columns) == expected_columns

    """Тестирование, что функция игнорирует операции со статусом "FAIL"""
    filtered_result = spending_by_weekday(data_2, "10.11.2024")
    assert filtered_result.loc[0, "Friday"] == 0

    """Тестирование обработки пустого DataFrame"""
    empty_df = pd.DataFrame(columns=["Дата операции", "Статус", "Сумма операции"])
    result = spending_by_weekday(empty_df, "10.11.2024")
    assert (result.iloc[0] == 0).all()

    """ Тестирование обработки некорректного формата даты"""
    with pytest.raises(ValueError, match="Не верный формат даты"):
        spending_by_weekday(data_1, "2024-11-10")

    """Тестирование функции с не верным форматом переданного df"""
    data_2_error = pd.DataFrame([{"Name": "Alice", "Age": 23}])
    with pytest.raises(ValueError, match="Не верный формат данных"):
        spending_by_workday(data_2_error, "11.11.2024")


data_3 = pd.DataFrame([
    {"Дата операции": "10.11.2024 23:23:23", "Статус": "OK", "Сумма операции": -100.0},
    {"Дата операции": "09.11.2024 11:11:11", "Статус": "OK", "Сумма операции": -200.0},
    {"Дата операции": "08.11.2024 09:11:11", "Статус": "OK", "Сумма операции": -150.0},
    {"Дата операции": "07.11.2024 15:15:15", "Статус": "FAIL", "Сумма операции": -50.0},
    {"Дата операции": "06.11.2024 15:15:15", "Статус": "FAIL", "Сумма операции": -400.0},
    {"Дата операции": "06.11.2024 12:30:30", "Статус": "OK", "Сумма операции": -300.0},
    {"Дата операции": "05.11.2024 10:10:10", "Статус": "OK", "Сумма операции": -250.0}
])

def test_spending_by_workday(freezer) -> None:
    """ Тестирование работы функции, если дата не была задана """
    freezer.move_to("11.11.2024")

    """Тестирование на то, что функция возвращает правильные средние значения для будних и выходных дней"""
    result = spending_by_workday(data_3, "10.11.2024")
    assert result.loc[0, "Weekday"] == 140.0
    assert result.loc[0, "Days_off"] == 100.0

    """Тестирование на то, что функция игнорирует операции со статусом FAIL"""
    result = spending_by_workday(data_3, "10.11.2024")
    assert result.loc[0, "Weekday"] == 140.0

    """Тестирование на работу с пустым df"""
    empty_df = pd.DataFrame(columns=["Дата операции", "Статус", "Сумма операции"])
    result = spending_by_workday(empty_df, "10.11.2024")
    assert result.loc[0, "Weekday"] == 0
    assert result.loc[0, "Days_off"] == 0

    """ Тестирование обработки некорректного формата даты"""
    with pytest.raises(ValueError, match="Не верный формат даты"):
        spending_by_workday(data_3, "2024-11-10")

    """Тестирование функции с не верным форматом переданного df"""
    data_3_error = pd.DataFrame([{"Name": "Alice", "Age": 23}])
    with pytest.raises(ValueError, match="Не верный формат данных"):
        spending_by_workday(data_3_error, "11.11.2024")
