import pytest

from pathlib import Path
from typing import Callable, Any


@pytest.fixture
def save_xlsx(tmp_path: Path) -> Callable:
    def save_xlsx_file(data: Any) -> Path:
        file_path = tmp_path / "test_xlsx.xlsx"
        data.to_excel(file_path, index=False)
        return file_path

    return save_xlsx_file