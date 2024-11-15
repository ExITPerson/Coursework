import json
from collections import defaultdict
from typing import Any

import pandas as pd
from black import datetime


def profitable_cashback_categories(data: pd.DataFrame, year: str, month: str) -> Any:
    date = datetime.strptime(f"{month}.{year}", "%m.%Y").strftime("%m.%Y")
    try:
        df = pd.notnull(data["Кэшбэк"])
        data: dict = data[df].to_dict("records")

        cashback_categories = [
            {d["Категория"]: d["Кэшбэк"]}
            for d in data
            if date == datetime.strptime(d["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y")
        ]
    except ValueError:
        raise ValueError("Не корректный формат данных")

    dd = defaultdict(list)
    for category in cashback_categories:
        for k, v in category.items():
            dd[k].append(v)
    result = [{k: sum(v) for k, v in dd.items()}]

    return json.dumps(result, ensure_ascii=False)
