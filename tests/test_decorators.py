import json
import os
from typing import Any

import pandas as pd
import pytest

from src.decorator import log


def test_log_file_creation_and_content(freezer: Any) -> None:
    """Тестирование создания файла с корректными данными """
    freezer.move_to("11.11.2024")

    @log()
    def sample_function() -> list:
        df = pd.DataFrame([{"name": "Alice", "Age": 30}])
        return df

    sample_function()

    with open("json/2024_11_11_sample_function.json", "r", encoding="utf-8") as f:
        content = json.load(f)

    assert [{'Age': 30, 'name': 'Alice'}] == content


def test_log_error() -> None:
    """Тестирование ошибки при передаче формата данных не df """
    @log()
    def return_error() -> None:
        raise ValueError

    with pytest.raises(ValueError, match="Ошибка, не корректные данные"):
        return_error()


