import streamlit as st

from database import (
    verify_user,
    add_user
)


def login_page():

    st.title("🔐 Expense Tracker Pro")

    tab1, tab2 = st.tabs(
        [
            "Login",
            "New User"
        ]
    )


    # LOGIN TAB
    with tab1:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button("Login"):

            user = verify_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.database_name = user[0]

                st.success(
                    "Login successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid username or password"
                )


    # NEW USER TAB
    with tab2:

        new_username = st.text_input(
            "New Username",
            key="new_username"
        )

        new_password = st.text_input(
            "New Password",
            type="password",
            key="new_password"
        )


        if st.button("Create Account"):

            if new_username and new_password:

                try:

                    add_user(
                        new_username,
                        new_password
                    )

                    st.success(
                        "Account created. You can login now."
                    )


                except Exception as e:

                    st.error(e)

            else:

                st.warning(
                    "Please enter username and password."
                )