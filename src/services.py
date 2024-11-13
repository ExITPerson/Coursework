import pandas as pd

from collections import defaultdict

from black import datetime


def profitable_cashback_categories(data: pd.DataFrame, year: str=None, month: str=None):
    date = datetime.strptime(f"{month}.{year}", "%m.%Y").strftime("%m.%Y")

    bool = pd.notnull(data["Кэшбэк"])
    data = data[bool].to_dict("records")

    cashback_categories = [
        {d["Категория"]: d["Кэшбэк"]}
        for d in data
        if date == datetime.strptime(d["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y")
    ]
    dd = defaultdict(list)
    for category in cashback_categories:
        for k, v in category.items():
            dd[k].append(v)
    result = [{k: sum(v) for k, v in dd.items()}]

    return result