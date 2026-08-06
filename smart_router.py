from database_agent import (
    last_month_total,
    spending_by_merchant,
    spending_by_category,
    monthly_total,
    biggest_expense,
    last_expenses,
    biggest_category
)


def route_question(question, database_name):

    q = question.lower()


    # ----------------------------
    # Merchant questions
    # ----------------------------

    if "carrefour" in q:

        amount = spending_by_merchant(
            database_name,
            "carrefour"
             
        )

        return (
            "database",
            f"You spent €{amount:.2f} at Carrefour."
        )


    # ----------------------------
    # Category questions
    # ----------------------------

    if "food" in q:

        amount = spending_by_category(
            database_name,
            "Food"
        )

        return (
            "database",
            f"You spent €{amount:.2f} on Food."
        )


    if "shopping" in q:

        amount = spending_by_category(
            database_name,
            "Shopping"
        )

        return (
            "database",
            f"You spent €{amount:.2f} on Shopping."
        )


    # ----------------------------
    # This month spending
    # ----------------------------

    if "this month" in q:

        amount = monthly_total(database_name)

        return (
            "database",
            f"Your spending this month is €{amount:.2f}."
        )


    # ----------------------------
    # Last month spending
    # ----------------------------

    if "last month" in q:

        amount = last_month_total(database_name)

        return (
            "database",
            f"Your spending last month was €{amount:.2f}."
        )


    # ----------------------------
    # Last expenses
    # ----------------------------

    if "last 5 expenses" in q:

        data = last_expenses(database_name, 5)

        return (
            "database",
            data
        )


    if "last 10 expenses" in q:

        data = last_expenses(database_name, 10)

        return (
            "database",
            data
        )


    # ----------------------------
    # Biggest category
    # ----------------------------

    if "category costs me the most" in q:

        data = biggest_category(database_name)

        return (
            "database",
            str(data)
        )


    # ----------------------------
    # Biggest expense
    # ----------------------------

    if (
        "biggest expense" in q
        or
        "largest expense" in q
    ):

        expense = biggest_expense(database_name)


        if expense is not None:

            return (
                "database",
                f"""
Your biggest expense was:

Merchant: {expense['merchant']}
Category: {expense['category']}
Amount: €{expense['amount']:.2f}
Date: {expense['date']}
"""
            )


        return (
            "database",
            "No expenses found."
        )


    # ----------------------------
    # AI fallback
    # ----------------------------

    return (
        "ai",
        question
    )