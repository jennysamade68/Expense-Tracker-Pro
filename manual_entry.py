import streamlit as st
from datetime import date

from database import save_expense


def manual_expense_form():

    st.subheader("✍️ Add Expense Manually")


    expense_date = st.date_input(
        "Date",
        value=date.today()
    )


    merchant = st.text_input(
        "Merchant",
        placeholder="Example: Carrefour"
    )


    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Healthcare",
            "Entertainment",
            "Other"
        ],
        key="manual_category"
    )


    amount = st.number_input(
        "Amount (€)",
        min_value=0.0,
        step=0.50,
        key="manual_amount"
    )


    description = st.text_input(
        "Description",
        placeholder="Example: Weekly groceries",
        key="manual_description"
    )


    payment_method = st.selectbox(
        "Payment Method",
        [
            "Card",
            "Cash",
            "Bank Transfer",
            "Other"
        ],
        key="manual_payment"
    )


    if st.button(
        "💾 Save Expense",
        key="manual_save_expense"
    ):


        if merchant == "":

            st.error(
                "Please enter merchant name"
            )

            return


        if amount <= 0:

            st.error(
                "Amount must be greater than zero"
            )

            return


        save_expense(

            date=str(expense_date),

            merchant=merchant,

            category=category,

            amount=amount,

            description=description,

            payment_method=payment_method

        )


        st.success(
            "✅ Expense saved successfully!"
        )
         st.rerun()
