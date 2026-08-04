import sqlite3
import pandas as pd

from datetime import datetime



DATABASE_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT NOT NULL,
        merchant TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,

        description TEXT,
        payment_method TEXT,

        receipt_image TEXT,

        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_expense(
    date,
    merchant,
    category,
    amount,
    description="",
    payment_method="",
    receipt_image=""
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses
    (
        date,
        merchant,
        category,
        amount,
        description,
        payment_method,
        receipt_image,
        created_at
    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        date,
        merchant,
        category,
        amount,
        description,
        payment_method,
        receipt_image,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_expenses():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM expenses
    ORDER BY date DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def delete_expense(expense_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (expense_id,)
    )

    conn.commit()
    conn.close()


def update_expense(
    expense_id,
    date,
    merchant,
    category,
    amount,
    description,
    payment_method
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE expenses

    SET

    date=?,
    merchant=?,
    category=?,
    amount=?,
    description=?,
    payment_method=?

    WHERE id=?
    """,
    (
        date,
        merchant,
        category,
        amount,
        description,
        payment_method,
        expense_id
    ))

    conn.commit()
    conn.close()


def get_total_spending():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0


def get_category_summary():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        category,
        SUM(amount)

    FROM expenses

    GROUP BY category

    ORDER BY SUM(amount) DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_monthly_summary():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        substr(date,1,7),
        SUM(amount)

    FROM expenses

    GROUP BY substr(date,1,7)

    ORDER BY substr(date,1,7)
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def search_expenses(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *

    FROM expenses

    WHERE

    merchant LIKE ?
    OR category LIKE ?
    OR description LIKE ?

    ORDER BY date DESC
    """,
    (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    data = cursor.fetchall()

    conn.close()

    return data

def update_expense(
    expense_id,
    date,
    merchant,
    category,
    amount,
    description,
    payment_method
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE expenses

        SET
            date = ?,
            merchant = ?,
            category = ?,
            amount = ?,
            description = ?,
            payment_method = ?

        WHERE id = ?

        """,

        (
            date,
            merchant,
            category,
            amount,
            description,
            payment_method,
            expense_id
        )
    )


    conn.commit()

    conn.close()