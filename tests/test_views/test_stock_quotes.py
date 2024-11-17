from unittest.mock import mock_open, patch

import pytest

from src.views import stock_quotes


@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "TSLA"]}')
@patch("requests.get")
def test_positive_result(mock_get, mock_open):
    """Тестирование корректного ответа API и выдачи результата"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"last": 100}
    result = stock_quotes()

    assert result == [{"stock": "AAPL", "price": 100}, {"stock": "TSLA", "price": 100}]


@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "TSLA"]}')
@patch("requests.get")
def test_error_api(mock_get, mock_open):
    """Тестирование ошибки API"""
    mock_get.return_value.status_code = 500

    with pytest.raises(BaseException, match="500"):
        stock_quotes()


@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks":[]}')
def test_exchange_rate_no_currencies(mock_open):
    """Тестирование при отсутствии пользовательских тикеров"""
    result = stock_quotes()
    assert result == []
