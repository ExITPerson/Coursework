import pandas as pd


def get_data_from_xlsx(file_path: str) -> pd.DataFrame:
    """Функция для чтения данных xlsx файла"""
    df = pd.read_excel(file_path)
    return df


def get_data_from_csv(file_path: str) -> pd.DataFrame:
    """Функция для чтения данных xlsx файла"""
    df = pd.read_csv(file_path)
    return df
