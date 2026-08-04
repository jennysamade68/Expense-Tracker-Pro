import streamlit as st
import pandas as pd

from database import save_expense


REQUIRED_COLUMNS = [
    "date",
    "merchant",
    "category",
    "amount"
]


def import_expense_file():

    st.subheader("📄 Import Excel / CSV")


    uploaded_file = st.file_uploader(
        "Upload expense file",
        type=[
            "csv",
            "xlsx"
        ]
    )


    if uploaded_file:


        # Read file

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_file
            )

        else:

            df = pd.read_excel(
                uploaded_file
            )


        st.write(
            "Preview:"
        )

        st.dataframe(
            df
        )


        # Check columns

        missing_columns = []

        for column in REQUIRED_COLUMNS:

            if column not in df.columns:

                missing_columns.append(
                    column
                )


        if missing_columns:

            st.error(
                f"Missing columns: {missing_columns}"
            )

            return


        if st.button(
            "📥 Import Expenses"
        ):


            imported = 0


            for _, row in df.iterrows():


                save_expense(

                    date=str(
                        row["date"]
                    ),

                    merchant=str(
                        row["merchant"]
                    ),

                    category=str(
                        row["category"]
                    ),

                    amount=float(
                        row["amount"]
                    ),

                    description=str(
                        row.get(
                            "description",
                            ""
                        )
                    ),

                    payment_method=str(
                        row.get(
                            "payment_method",
                            ""
                        )
                    )

                )


                imported += 1


            st.success(
                f"✅ {imported} expenses imported successfully!"
            )