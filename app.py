import streamlit as st


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="AI Expense Tracker Pro",
    page_icon="💰",
    layout="wide"
)

import os
import pandas as pd

from login import login_page

from database import (
    create_database,
    save_expense,
    get_expenses,
    delete_expense,
    update_expense,
    create_users_table,
    add_user
)


from budget import (
    create_budget_table,
    save_budget,
    get_budget
)

# =========================
# DATABASE INITIALIZATION
# =========================

create_database()
create_users_table()
create_budget_table()


# =========================
# LOGIN CHECK
# =========================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if not st.session_state.logged_in:

    login_page()

    st.stop()

# =========================
# SIDEBAR USER MENU
# =========================

with st.sidebar:

    st.markdown("---")

    st.write(
        f"👤 Logged in: {st.session_state.username}"
    )


    try:

        expenses = get_expenses(
            st.session_state.database_name
        )

        total_expenses = len(expenses)

        total_amount = sum(
            item[4] for item in expenses
        )


        st.write(
            f"🧾 Expenses: {total_expenses}"
        )

        st.write(
            f"💶 Total: €{total_amount:.2f}"
        )


    except Exception as e:

        st.write(
            "No data available"
        )


    # Budget

    try:

        from budget import get_budget


        monthly_budget = get_budget(
            st.session_state.database_name
        )


        if monthly_budget:

            remaining = monthly_budget - total_amount


            st.write(
                f"💰 Budget: €{monthly_budget:.2f}"
            )


            st.write(
                f"📉 Remaining: €{remaining:.2f}"
            )


        else:

            st.write(
                "💰 Budget: Not set"
            )


    except Exception as e:

        st.write(
            "💰 Budget: Not available"
        )


    st.markdown("---")


    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.session_state.username = None

        st.session_state.database_name = None

        st.session_state.page = None

        st.rerun()
        
 # =========================
# LOAD APP MODULES AFTER LOGIN
# =========================   

from receipt_image_processor import preprocess_receipt
from receipt_parser import parse_receipt
from ocr import read_receipt
from ai import analyze_receipt

from manual_entry import manual_expense_form
from import_data import import_expense_file

from ai_assistant import ask_ai
from smart_router import route_question

from dashboard import (
    total_spending,
    receipt_count,
    average_expense,
    current_month_spending,
    recent_expenses
)

from charts import (
    category_chart,
    monthly_chart,
    merchant_chart
)

from export import (
    get_expense_dataframe,
    export_excel,
    export_pdf
)
    
from budget import (
    create_budget_table,
    save_budget,
    get_budget
)


create_database()
create_users_table()
create_budget_table()

st.title("💰 AI Expense Tracker Pro")

st.write(
    "OCR + Local AI + Expense Dashboard"
)


# ==============================
# DASHBOARD CARDS
# ==============================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Total Spending",
    f"€{total_spending():.2f}"
)


c2.metric(
    "Receipts",
    receipt_count()
)


c3.metric(
    "Average",
    f"€{average_expense():.2f}"
)


c4.metric(
    "This Month",
    f"€{current_month_spending():.2f}"
)



# ==============================
# TABS
# ==============================


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "✍️ Manual Entry",
        "📷 Scan Receipt",
        "📄 Import",
        "📋 Expenses",
        "📥 Reports",
        "💰 Budget",
        "🤖 AI Assistant"        
    ]
)

# ==============================
# TAB 2
# RECEIPT SCANNER
# ==============================

with tab2:

    st.subheader(
        "📷 Scan Receipt"
    )


    # Camera capture

    camera_image = st.camera_input(
        "📷 Take a receipt photo"
    )


    # File upload

    uploaded_file = st.file_uploader(
        "📁 Upload receipt",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="receipt_upload"
    )


    receipt_file = None


    if camera_image:

        receipt_file = camera_image


    elif uploaded_file:

        receipt_file = uploaded_file



    if receipt_file:


        os.makedirs(
            "receipts",
            exist_ok=True
        )


        file_path = os.path.join(
            "receipts",
            receipt_file.name
        )


        with open(
            file_path,
            "wb"
        ) as f:

            f.write(
                receipt_file.getbuffer()
            )


        st.image(
            file_path,
            width=300
        )


        if st.button(
            "🤖 Analyze Receipt",
            key="analyze_receipt"
        ):


        # Image enhancement

            processed_file = preprocess_receipt(
                file_path
            )


            st.subheader(
                "✨ Enhanced Receipt"
            )


            st.image(
                processed_file,
                width=400
            )


            # OCR

            text = read_receipt(
                processed_file
            )


            st.text_area(
                "OCR Result",
                text,
                height=200
            )


            # Parse receipt

            expense = parse_receipt(
                text
            )


            # Use AI only if parser fails

            if (
                expense["amount"] == 0
                or
                expense["merchant"] == "Unknown"
            ):

                expense = analyze_receipt(
                    text
                )


            st.session_state.expense_result = expense

            st.session_state.receipt_path = file_path



    # Show result

    if "expense_result" in st.session_state:


        st.subheader(
            "🤖 Expense Result"
        )


        st.json(
            st.session_state.expense_result
        )


        if st.button(
            "💾 Save Receipt Expense",
            key="save_receipt"
        ):


            expense = st.session_state.expense_result


            save_expense(

    database_name=st.session_state.database_name,

    date=expense.get(
        "date",
        ""
    ),

    merchant=expense.get(
        "merchant",
        "Unknown"
    ),

    category=expense.get(
        "category",
        "Other"
    ),

    amount=float(
        expense.get(
            "amount",
            0
        )
    ),

    description=expense.get(
        "description",
        ""
    ),

    receipt_image=st.session_state.receipt_path

)


            st.success(
                "✅ Receipt saved!"
            )


            del st.session_state.expense_result


            st.rerun()

# ==============================
# TAB 1
# MANUAL ENTRY
# ==============================

with tab1:

    manual_expense_form()


# ==============================
# TAB 3
# IMPORT
# ==============================

with tab3:

    import_expense_file()



# ==============================
# TAB 4
# EXPENSE HISTORY
# ==============================

with tab4:

    st.subheader(
        "📋 Expense History"
    )


    expenses = get_expenses(
        st.session_state.database_name
)

    if expenses:


        df = pd.DataFrame(

            expenses,

            columns=[

                "ID",
                "Date",
                "Merchant",
                "Category",
                "Amount",
                "Description",
                "Payment",
                "Receipt",
                "Created"

            ]

        )


        # Clickable table
        st.info(
    "👆 Click on an expense row to view details and edit or delete it."
)

        event = st.dataframe(

            df,

            use_container_width=True,

            on_select="rerun",

            selection_mode="single-row"

        )


        # When user clicks a row

        if event.selection.rows:


            row = event.selection.rows[0]


            selected = df.iloc[row]


            st.divider()


            st.subheader(
                "Selected Expense"
            )


            st.write(
                f"**Merchant:** {selected['Merchant']}"
            )


            st.write(
                f"**Category:** {selected['Category']}"
            )


            st.write(
                f"**Amount:** €{selected['Amount']:.2f}"
            )


            st.write(
                f"**Date:** {selected['Date']}"
            )


            st.write(
                f"**Description:** {selected['Description']}"
            )


            # Receipt preview

            if selected["Receipt"]:


                if os.path.exists(
                    selected["Receipt"]
                ):

                    st.image(
                        selected["Receipt"],
                        width=300
                    )


            st.divider()


            col1, col2 = st.columns(2)


            # DELETE BUTTON

            with col1:

                if st.button(
                    "🗑 Delete Expense",
                    key="delete_selected"
                ):


                    delete_expense(
                        int(selected["ID"])
                    )


                    st.success(
                        "Expense deleted"
                    )


                    st.rerun()



            # EDIT BUTTON

            with col2:

                if st.button(
                    "✏️ Edit Expense",
                    key="edit_selected"
                ):


                    st.session_state.edit_expense = selected.to_dict()

                    st.rerun()



    else:

        st.info(
            "No expenses found"
        )
# ==============================
# EDIT EXPENSE FORM
# ==============================

if "edit_expense" in st.session_state:

    st.divider()

    st.subheader(
        "✏️ Edit Expense"
    )


    expense = st.session_state.edit_expense


    with st.form(
        "edit_expense_form"
    ):


        edit_date = st.text_input(
            "Date",
            value=str(expense["Date"])
        )


        edit_merchant = st.text_input(
            "Merchant",
            value=expense["Merchant"]
        )


        edit_category = st.text_input(
            "Category",
            value=expense["Category"]
        )


        edit_amount = st.number_input(
            "Amount (€)",
            value=float(expense["Amount"])
        )


        edit_description = st.text_area(
            "Description",
            value=str(expense["Description"])
        )


        edit_payment = st.text_input(
            "Payment Method",
            value=str(expense["Payment"])
        )


        save = st.form_submit_button(
            "💾 Save Changes"
        )


        if save:


            update_expense(

                expense_id=int(
                    expense["ID"]
                ),

                date=edit_date,

                merchant=edit_merchant,

                category=edit_category,

                amount=edit_amount,

                description=edit_description,

                payment_method=edit_payment

            )


            st.success(
                "✅ Expense updated successfully"
            )


            del st.session_state.edit_expense


            st.rerun()
# ==============================
# TAB 6
# BUDGET
# ==============================

with tab6:


    st.subheader(
        "💰 Monthly Budget"
    )


    budget = st.number_input(

        "Set Budget (€)",

        min_value=0.0,

        step=100.0

    )


    if st.button(
        "Save Budget",
        key="save_budget"
    ):

        save_budget(
            budget
        )

        st.success(
            "Budget saved"
        )


    current_budget = get_budget()


    spent = total_spending()


    remaining = current_budget - spent


    c1,c2,c3 = st.columns(3)


    c1.metric(
        "Budget",
        f"€{current_budget:.2f}"
    )


    c2.metric(
        "Spent",
        f"€{spent:.2f}"
    )


    c3.metric(
        "Remaining",
        f"€{remaining:.2f}"
    )


    if current_budget > 0:


        progress = spent / current_budget


        st.progress(
            min(
                progress,
                1.0
            )
        )


        if spent > current_budget:

            st.error(
                "⚠️ Budget exceeded"
            )

# ==============================
# TAB 5
# REPORT FILTERS
# ==============================

with tab5:


    st.subheader(
        "📥 Generate Reports"
    )


    df = get_expense_dataframe(
        st.session_state.database_name
)

    selected_month = st.selectbox(
         "📅 Select Month",
        [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
        ]
)

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    if selected_month != "All":

        df = df[
            df["Date"].dt.month_name() == selected_month
        ]


    if not df.empty:

        # Category filter

        categories = [
            "All"
        ] + list(
            df["Category"]
            .dropna()
            .unique()
        )


        category = st.selectbox(
            "Category",
            categories
        )


        if category != "All":

            df = df[
                df["Category"] == category
            ]


        st.write(
            f"Expenses found: {len(df)}"
        )


        if st.button(
            "⚙️ Generate Report",
            key="generate_report"
        ):

            excel = export_excel(
                df,
            selected_month
            )
             
            pdf = export_pdf(df, selected_month)


            st.session_state.excel_report = excel

            st.session_state.pdf_report = pdf


            st.success(
                "Reports created!"
            )



        if "excel_report" in st.session_state:


            with open(
                st.session_state.excel_report,
                "rb"
            ) as f:


                st.download_button(

                    "⬇️ Download Excel",

                    f,

                    file_name="expense_report.xlsx",

                    key="excel_download"

                )



        if "pdf_report" in st.session_state:


            with open(
                st.session_state.pdf_report,
                "rb"
            ) as f:


                st.download_button(

                    "⬇️ Download PDF",

                    f,

                    file_name="expense_report.pdf",

                    mime="application/pdf",

                    key="pdf_download"

                )


    else:

        st.info(
            "No expenses available"
        )
     
# ==============================
# CHARTS
# ==============================


st.divider()

st.header(
    "📊 Analytics"
)


chart = category_chart()

if chart:

    st.pyplot(
        chart
    )


chart = monthly_chart()

if chart:

    st.pyplot(
        chart
    )


chart = merchant_chart()

if chart:

    st.pyplot(
        chart
    )



# ==============================
# RECENT EXPENSES
# ==============================

st.divider()

st.header(
    "Recent Transactions"
)


st.dataframe(
    recent_expenses(),
    use_container_width=True
)
# ==============================
# TAB 7 - AI FINANCIAL ASSISTANT
# ==============================

with tab7:

    st.subheader(
        "🤖 AI Financial Assistant"
    )


    categories = {

        "💰 Spending": [

            "How much did I spend this month?",
            "How much did I spend last month?",
            "What is my biggest expense?"

        ],


        "📂 Categories": [

            "Which category costs me the most?",
            "How much did I spend on Food?",
            "How much did I spend on Shopping?"

        ],


        "🧾 Transactions": [

            "Show my last 5 expenses",
            "Show my last 10 expenses"

        ],


        "💳 Budget": [

            "Am I within my budget?",
            "How much budget is remaining?"

        ],


        "🤖 AI Advice": [

            "How can I reduce my spending?",
            "Give me saving advice",
            "Analyze my spending habits"

        ]

    }


    # Select category

    selected_category = st.selectbox(

        "Choose a category",

        categories.keys()

    )


    # Select question

    selected_question = st.selectbox(

        "Choose a question",

        categories[selected_category]

    )


    if st.button(

        "🚀 Ask",

        key="assistant_question"

    ):


        question = selected_question



        mode, result = route_question(
            question,
            st.session_state.database_name
)
       
        if mode == "database":


            st.success(

                result

            )


        else:


            with st.spinner(

                "🤖 AI is analyzing..."

            ):


                answer = ask_ai(

                    result

                )


            st.write(

                answer

            )

