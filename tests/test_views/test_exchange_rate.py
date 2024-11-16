from unittest.mock import mock_open, patch

import pytest

from src.views import exchange_rate


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
@patch("requests.get")
def test_positive_result(mock_get, mock_open):
    """Тестирование корректного ответа API и выдачи результата"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 100}
    result = exchange_rate()

    assert result == [{"currency": "USD", "rate": 100}, {"currency": "EUR", "rate": 100}]


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
@patch("requests.get")
def test_error_api(mock_get, mock_open):
    """Тестирование ошибки API"""
    mock_get.return_value.status_code = 500

    with pytest.raises(BaseException, match="500"):
        exchange_rate()


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies":[]}')
def test_exchange_rate_no_currencies(mock_open):
    """Тестирование при отсутствии пользовательских валют"""
    result = exchange_rate()
    assert result == []
