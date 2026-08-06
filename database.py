import sqlite3
import os
import bcrypt

from datetime import datetime


DATABASE_NAME = "expenses.db"
USERS_DB = "databases/users.db"


# =========================
# EXPENSE DATABASE
# =========================

def get_connection():

    return sqlite3.connect(DATABASE_NAME)

# =========================
# MAIN DATABASE 
# =========================

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

# =========================
# USER DATABASE (add here)
# =========================

def create_user_database(username):

    db_path = f"databases/{username.lower()}.db"

    os.makedirs("databases", exist_ok=True)

    conn = sqlite3.connect(db_path)

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


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        month TEXT NOT NULL,

        amount REAL NOT NULL

    )
    """)


    conn.commit()

    conn.close()

    return db_path

# =========================
# USER DATABASE
# =========================

def get_users_connection():

    os.makedirs("databases", exist_ok=True)

    conn = sqlite3.connect(
        USERS_DB,
        timeout=10
    )

    return conn

def get_user_connection(database_name):

    conn = sqlite3.connect(
        database_name,
        timeout=10
    )

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

    return conn

def create_users_table():

    conn = get_users_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        database_name TEXT NOT NULL

    )
    """)

    conn.commit()
    conn.close()



def add_user(username, password):

    conn = get_users_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    database_name = f"databases/{username.lower()}.db"


    cursor.execute(
        """
        INSERT INTO users
        (username, password, database_name)
        VALUES (?, ?, ?)
        """,
        (
            username,
            hashed_password.decode("utf-8"),
            database_name
        )
    )

    conn.commit()
    conn.close()


    # Create user's expense database
    create_user_database(username)

def verify_user(username, password):

    conn = get_users_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password, database_name
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()


    if user:

        stored_password = user[0]

        database_name = user[1]   # <-- ADD THIS LINE


        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        ):

            return {
                "username": username,
                "database_name": database_name
            }


    return None

# =========================
# EXPENSE FUNCTIONS
# =========================

def save_expense(
    database_name,
    date,
    merchant,
    category,
    amount,
    description="",
    payment_method="",
    receipt_image=""
):

    conn = get_user_connection(database_name)
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



def get_expenses(database_name):

    conn = get_user_connection(database_name)
    
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