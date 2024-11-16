from pathlib import Path
from typing import Any, Callable
import json
import pytest


@pytest.fixture
def save_xlsx(tmp_path: Path) -> Callable:
    def save_xlsx_file(data: Any) -> Path:
        file_path = tmp_path / "test_xlsx.xlsx"
        data.to_excel(file_path, index=False)
        return file_path

    return save_xlsx_file


@pytest.fixture
def save_txt(tmp_path: Path) -> Path:
    file_path = tmp_path / "log_test.txt"
    return file_path

@pytest.fixture
def save_json(tmp_path: Path) -> Path:
    def save_json_file(data: Any):
        file_path = tmp_path / "test_data.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return file_path
    return save_json_file
