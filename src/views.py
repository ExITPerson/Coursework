import pandas as pd


def get_data_from_xlsx(file_path):
    df = pd.read_excel(file_path)
    file_read = df.to_dict("records")
    return file_read
