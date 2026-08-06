import pandas as pd
import streamlit as st

from datetime import datetime

from database import get_expenses


# =====================================
# Load Database into DataFrame
# =====================================

def load_expense_dataframe():

    expenses = get_expenses(
        st.session_state.database_name
)

    if not expenses:

        return pd.DataFrame()


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


    # Fix different date formats

    df["Date"] = pd.to_datetime(

        df["Date"],

        format="mixed",

        dayfirst=True,

        errors="coerce"

    )


    # Convert amount safely

    df["Amount"] = pd.to_numeric(

        df["Amount"],

        errors="coerce"

    )


    # Remove bad rows

    df = df.dropna(

        subset=[
            "Date",
            "Amount"
        ]

    )


    return df



# =====================================
# Total Spending
# =====================================

def total_spending():

    df = load_expense_dataframe()


    if df.empty:

        return 0


    return float(

        df["Amount"].sum()

    )



# =====================================
# Receipt Count
# =====================================

def receipt_count():

    df = load_expense_dataframe()


    return len(df)



# =====================================
# Average Expense
# =====================================

def average_expense():

    df = load_expense_dataframe()


    if df.empty:

        return 0


    return float(

        df["Amount"].mean()

    )



# =====================================
# Current Month Spending
# =====================================

def current_month_spending():

    df = load_expense_dataframe()


    if df.empty:

        return 0


    today = datetime.today()


    monthly = df[

        (df["Date"].dt.month == today.month)

        &

        (df["Date"].dt.year == today.year)

    ]


    return float(

        monthly["Amount"].sum()

    )



# =====================================
# Category Summary
# =====================================

def category_summary():

    df = load_expense_dataframe()


    if df.empty:

        return pd.DataFrame()


    return (

        df

        .groupby(
            "Category"
        )["Amount"]

        .sum()

        .reset_index()

        .sort_values(

            "Amount",

            ascending=False

        )

    )



# =====================================
# Monthly Summary
# =====================================

def monthly_summary():

    df = load_expense_dataframe()


    if df.empty:

        return pd.DataFrame()


    df["Month"] = (

        df["Date"]

        .dt

        .to_period("M")

        .astype(str)

    )


    return (

        df

        .groupby(
            "Month"
        )["Amount"]

        .sum()

        .reset_index()

    )



# =====================================
# Recent Expenses
# =====================================

def recent_expenses(limit=5):

    df = load_expense_dataframe()


    if df.empty:

        return pd.DataFrame()


    return (

        df

        .sort_values(

            "Date",

            ascending=False

        )

        .head(limit)

    )