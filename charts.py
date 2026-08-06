import matplotlib.pyplot as plt

from dashboard import (
    category_summary,
    monthly_summary,
    load_expense_dataframe
)


# ----------------------------
# Category Pie Chart
# ----------------------------

def category_chart():

    df = category_summary()


    if df.empty:
        return None


    fig, ax = plt.subplots(
        figsize=(6, 4)
    )


    ax.pie(
        df["Amount"],
        labels=df["Category"],
        autopct="%1.1f%%"
    )


    ax.set_title(
        "Spending by Category"
    )


    return fig



# ----------------------------
# Monthly Trend Chart
# ----------------------------

def monthly_chart():

    df = monthly_summary()


    if df.empty:
        return None


    fig, ax = plt.subplots(
        figsize=(7, 4)
    )


    ax.plot(
        df["Month"],
        df["Amount"],
        marker="o"
    )


    ax.set_title(
        "Monthly Spending"
    )


    ax.set_xlabel(
        "Month"
    )


    ax.set_ylabel(
        "Amount (€)"
    )


    plt.xticks(
        rotation=45
    )


    return fig



# ----------------------------
# Top Merchants Chart
# ----------------------------

def merchant_chart():

    df = load_expense_dataframe()


    if df.empty:
        return None


    merchants = (
        df
        .groupby("Merchant")["Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    fig, ax = plt.subplots(
        figsize=(8, 4)
    )


    ax.bar(
        merchants.index,
        merchants.values
    )


    ax.set_title(
        "Top Spending Merchants"
    )


    ax.set_ylabel(
        "Amount (€)"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    return fig