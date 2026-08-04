import pandas as pd

from database import get_expenses


def get_expense_dataframe():

    expenses = get_expenses()

    df = pd.DataFrame(
        expenses,
        columns=[
            "ID",
            "Date",
            "Merchant",
            "Category",
            "Amount",
            "Description",
            "Payment Method",
            "Receipt Image",
            "Created At"
        ]
    )

    return df



def export_excel(df):

    filename = "expense_report.xlsx"

    df.to_excel(
        filename,
        index=False
    )

    return filename



def export_pdf(df):

    from reportlab.platypus import (
        SimpleDocTemplate,
        Table
    )


    filename = "expense_report.pdf"


    doc = SimpleDocTemplate(
        filename
    )


    data = [
        [
            "Date",
            "Merchant",
            "Category",
            "Amount"
        ]
    ]


    for _, row in df.iterrows():

        data.append(
            [
                row["Date"],
                row["Merchant"],
                row["Category"],
                str(row["Amount"])
            ]
        )


    table = Table(data)


    doc.build(
        [table]
    )


    return filename