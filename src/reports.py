import logging

from typing import Optional

import pandas as pd

from datetime import datetime, timedelta

from utils import get_data_from_xlsx
from decorator import log


@log()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%d.%m.%Y")

    date_to = date
    date_from = (date_to - timedelta(days=90))

    transactions_dict = get_data_from_xlsx(transactions)

    filtered_transactions = []
    for transaction in transactions_dict:
        transaction_date = datetime.strptime(
            transaction["Дата операции"], "%d.%m.%Y %H:%M:%S"
        )
        if date_to > transaction_date > date_from and transaction["Категория"] == category:
            filtered_transactions.append(transaction)
    return filtered_transactions
