import pytest

from pathlib import Path
from typing import Callable, Any
from datetime import datetime

@pytest.fixture
def save_xlsx(tmp_path: Path) -> Callable:
    def save_xlsx_file(data: Any) -> Path:
        file_path = tmp_path / "test_xlsx.xlsx"
        data.to_excel(file_path, index=False)
        return file_path

    return save_xlsx_file


@pytest.fixture
def save_txt(tmp_path: Path) -> Callable:
    file_path = tmp_path / f"log_test.txt"
    return file_path
