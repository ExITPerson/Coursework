import pandas as pd
import pytest

from tests.conftest import save_xlsx
from src.utils import get_data_from_xlsx


def test_get_data_from_xlsx(save_xlsx):
    data = pd.DataFrame(
        [
            {"data": "24.03.2024", "name": "Alice", "amount": 63516},
            {"data": "21.10.2024", "name": "Petr", "amount": 65712},
            {"data": "11.12.2024", "name": "Ivan", "amount": 516}
        ]
    )
    file = save_xlsx(data)
    result = get_data_from_xlsx(file)
    assert result == [
            {"data": "24.03.2024", "name": "Alice", "amount": 63516},
            {"data": "21.10.2024", "name": "Petr", "amount": 65712},
            {"data": "11.12.2024", "name": "Ivan", "amount": 516}
        ]
