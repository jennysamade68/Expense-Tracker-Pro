import sqlite3
from datetime import datetime


DATABASE = "expenses.db"



def create_budget_table():

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budget
        (
            id INTEGER PRIMARY KEY,
            month TEXT,
            amount REAL
        )
        """
    )


    conn.commit()

    conn.close()



def save_budget(amount):

    month = datetime.today().strftime(
        "%Y-%m"
    )


    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM budget
        WHERE month=?
        """,
        (month,)
    )


    cursor.execute(
        """
        INSERT INTO budget
        (month, amount)
        VALUES (?,?)
        """,
        (
            month,
            amount
        )
    )


    conn.commit()

    conn.close()



def get_budget():

    month = datetime.today().strftime(
        "%Y-%m"
    )


    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT amount
        FROM budget
        WHERE month=?
        """,
        (month,)
    )


    result = cursor.fetchone()


    conn.close()


    if result:

        return result[0]


    return 0