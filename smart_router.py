from database_agent import (
    last_month_total,
    spending_by_merchant,
    spending_by_category,
    monthly_total,
    biggest_expense,
    last_expenses,
    biggest_category
)


def route_question(question):

    q = question.lower()


    # ----------------------------
    # Merchant questions
    # ----------------------------

    if "carrefour" in q:

        amount = spending_by_merchant(
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
            "Food"
        )

        return (
            "database",
            f"You spent €{amount:.2f} on Food."
        )


    if "shopping" in q:

        amount = spending_by_category(
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

        amount = monthly_total()

        return (
            "database",
            f"Your spending this month is €{amount:.2f}."
        )


    # ----------------------------
    # Last month spending
    # ----------------------------

    if "last month" in q:

        amount = last_month_total()

        return (
            "database",
            f"Your spending last month was €{amount:.2f}."
        )


    # ----------------------------
    # Last expenses
    # ----------------------------

    if "last 5 expenses" in q:

        data = last_expenses(5)

        return (
            "database",
            data
        )


    if "last 10 expenses" in q:

        data = last_expenses(10)

        return (
            "database",
            data
        )


    # ----------------------------
    # Biggest category
    # ----------------------------

    if "category costs me the most" in q:

        data = biggest_category()

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

        expense = biggest_expense()


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