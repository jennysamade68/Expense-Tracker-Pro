import pandas as pd
from database import get_expenses


def get_expense_dataframe():

    expenses = get_expenses()

    return pd.DataFrame(
        expenses,
        columns=[
            "ID",
            "Date",
            "Merchant",
            "Category",
            "Amount",
            "Description",
            "Payment Method",
            "Created At"
        ]
    )