from pathlib import Path
from typing import Any, Callable

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
