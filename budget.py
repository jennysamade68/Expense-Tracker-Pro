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



def save_budget(database_name, amount):

    month = datetime.today().strftime(
        "%Y-%m"
    )


    conn = sqlite3.connect(
        database_name
    )

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        month TEXT NOT NULL UNIQUE,

        amount REAL NOT NULL

    )
    """)


    cursor.execute(
        """
        INSERT OR REPLACE INTO budget
        (month, amount)
        VALUES (?, ?)
        """,
        (
            month,
            amount
        )
    )


    conn.commit()

    conn.close()


def get_budget(database_name):

    month = datetime.today().strftime("%Y-%m")

    conn = sqlite3.connect(database_name)

    cursor = conn.cursor()

    # Create table if missing

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        month TEXT NOT NULL,

        amount REAL NOT NULL

    )
    """)


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