import json
from datetime import datetime
from functools import wraps
from typing import Any, Callable


def log() -> Callable:
    """Декоратор, записывающий выходные данные функции в json файл"""

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            date = datetime.now().strftime("%Y_%m_%d")

            df = func(*args, **kwargs)
            result = df.to_dict("records")
            try:
                with open(f"json/{date}_{func.__name__}.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
            except Exception:
                raise ValueError("Ошибка записи, неверный формат данных")

        return inner

    return wrapper
