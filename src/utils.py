import pandas as pd


def get_data_from_xlsx(file_path):
    """ Функция для чтения данных xlsx файла """
    df = pd.read_excel(file_path)
    return df

print(get_data_from_xlsx("data/operations_t.xlsx"))
