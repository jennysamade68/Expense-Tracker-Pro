import sqlite3
import pandas as pd

from datetime import datetime
import pandas as pd

DATABASE = "expenses.db"


def load_database(database_name):

    conn = sqlite3.connect(
        database_name,
        timeout=10
    )

    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    conn.close()

    return df


def spending_by_merchant(merchant, database_name):

    df = load_database(database_name)

    if df.empty:
        return 0

    merchant = merchant.lower()

    filtered = df[

        df["merchant"].str.lower().str.contains(
            merchant,
            na=False
        )

    ]

    return filtered["amount"].sum()

def biggest_expense(database_name):

    df = load_database(database_name)


    if df.empty:
        return None


    biggest = df.loc[
        df["amount"].idxmax()
    ]


    return biggest

def spending_by_category(database_name, category):

    df = load_database(database_name)

    if df.empty:
        return 0

    filtered = df[

        df["category"].str.lower() == category.lower()

    ]

    return filtered["amount"].sum()

def monthly_total(database_name):

    df = load_database(database_name)

    return df["amount"].sum()

def biggest_expense(database_name):

    df = load_database(database_name)


    if df.empty:
        return None


    biggest = df.loc[
        df["amount"].idxmax()
    ]


    return biggest

def biggest_category(database_name):

    df = load_database(database_name)


    result = (

        df.groupby("category")
        ["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(1)

    )

    return result

def last_expenses(database_name, limit=5):

    df = load_database(database_name)


    if df.empty:
        return df


    return df.sort_values(
        "date",
        ascending=False
    ).head(limit)

def last_month_total(database_name):

    df = load_database(database_name)


    if df.empty:
        return 0


    df["date"] = pd.to_datetime(
        df["date"]
    )


    today = datetime.today()


    last_month = today.month - 1
    year = today.year


    if last_month == 0:
        last_month = 12
        year -= 1


    filtered = df[
        (df["date"].dt.month == last_month)
        &
        (df["date"].dt.year == year)
    ]


    return filtered["amount"].sum()
