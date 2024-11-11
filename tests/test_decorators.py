import os
import json
import pytest

from src.decorator import log


@log()
def sample_function():
    return [{"name": "Alice"}]


@log()
def return_unserializable():
    return {"data": {1, 2, 3}}


def clear_logs():
    if os.path.exists("json"):
        for filename in os.listdir("json"):
            os.remove(os.path.join("json", filename))


def test_log_file_creation_and_content(freezer):
    freezer.move_to("11.11.2024")
    clear_logs()

    sample_function()

    with open("json/2024_11_11_sample_function.json", "r", encoding="utf-8") as f:
        content = json.load(f)

    assert [{"name": "Alice"}] == content


# Тест логирования исключений
def test_log_error():
    with pytest.raises(ValueError, match="Ошибка записи, неверный формат данных"):
        return_unserializable()