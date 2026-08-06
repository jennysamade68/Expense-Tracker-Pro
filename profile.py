import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime


def get_profile_data(database_name):

    conn = sqlite3.connect(database_name)

    cursor = conn.cursor()


    # Number of expenses

    cursor.execute(
        "SELECT COUNT(*) FROM expenses"
    )

    expense_count = cursor.fetchone()[0]


    # Total spending

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    total = cursor.fetchone()[0]

    if total is None:
        total = 0


    conn.close()


    return expense_count, total



def show_profile():

    st.title(
        "👤 My Profile"
    )


    username = st.session_state.username

    database_name = st.session_state.database_name


    expense_count, total_spending = get_profile_data(
        database_name
    )


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            f"""
            **Username**

            {username}
            """
        )


        st.info(
            f"""
            **Database**

            {database_name}
            """
        )


    with col2:

        st.info(
            f"""
            **Number of Expenses**

            {expense_count}
            """
        )


        st.info(
            f"""
            **Total Spending**

            €{total_spending:.2f}
            """
        )


    st.divider()


    st.subheader(
        "📅 Account Information"
    )


    st.write(
        "Account creation date"
    )


    # For now use users.db later we can store real date

    st.write(
        datetime.now().strftime(
            "%d/%m/%Y"
        )
    )


    st.divider()


    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.database_name = None
        st.session_state.page = None

        st.rerun()