import pandas as pd

import json

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import profitable_cashback_categories
from src.utils import get_data_from_xlsx
from src.views import get_the_end_result


def main():
    print("Приветствую")
    user_input = input("Введите, что хотели бы получить\n"
                       "1. Главное меню\n"
                       "2. Категории повышенного кэшбэка\n"
                       "3. Отчеты о транзакциях\n")
    if user_input == "1":
        data = get_data_from_xlsx("data/operations_t.xlsx")
        date = "2024-11-11 01:01:01"
        result = get_the_end_result(date, data)
        print(json.dumps(result, indent=4, ensure_ascii=False))
    elif user_input == "2":
        data = get_data_from_xlsx("data/operations_t.xlsx")
        result = profitable_cashback_categories(data, "2024", "11")
        print(json.dumps(result, indent=4, ensure_ascii=False))
    elif user_input == "3":
        data = get_data_from_xlsx("data/operations_t.xlsx")
        input_spending = input("Какой вариант отчета хотите получить:\n"
                               "1. По категориям\n"
                               "2. По дням недели\n"
                               "3. По выходным и будним дням\n")
        if input_spending == "1":
            category = input("Введите категорию:")
            df = pd.DataFrame(spending_by_category(data, category))
            print(df.to_dict("records"))
        elif input_spending =="2":
            df = pd.DataFrame(spending_by_weekday(data))
            print(df.to_dict("records"))
        elif input_spending == "3":
            df = pd.DataFrame(spending_by_workday(data))
            print(df.to_dict("records"))



if __name__ == "__main__":
    main()