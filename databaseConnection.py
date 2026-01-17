import sqlite3
from sqlite3 import Error
import datetime

# Database file
SQLITE_DB_FILE = "taxibooking.db"


def create_connection():
    """Create and return SQLite connection."""
    conn = None
    try:
        conn = sqlite3.connect(
            SQLITE_DB_FILE,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print("DB Connection error:", e)
        return None


def create_tables():
    """Create tables if they do not exist."""
    conn = create_connection()
    if not conn:
        print("Cannot create tables: DB connection failed.")
        return

    cursor = conn.cursor()
    try:
        # ADMIN
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
"""
        )

        # CUSTOMER
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    telephone TEXT,
    password TEXT
);
"""
        )

        # DRIVER
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS driver (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    license_number TEXT,
    password TEXT,
    available INTEGER DEFAULT 1
);
"""
        )

        # TRIP
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS trip (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    driver_id INTEGER,
    pickup TEXT,
    dropoff TEXT,
    pickup_date TEXT,
    pickup_time TEXT,
    dropoff_date TEXT NULL,
    dropoff_time TEXT NULL,
    fare REAL,
    status TEXT DEFAULT 'requested',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE SET NULL,
    FOREIGN KEY (driver_id) REFERENCES driver(id) ON DELETE SET NULL
);
"""
        )

        # PAYMENT
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER,
    amount REAL,
    method TEXT,
    status TEXT,
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trip(id) ON DELETE SET NULL
);
"""
        )

        # Default admin
        cursor.execute("SELECT COUNT(*) FROM admin;")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO admin (username, password) VALUES (?, ?);",
                ("admin", "admin123"),
            )

        conn.commit()
        print("Tables created/checked.")
    except Error as e:
        print("Error creating tables:", e)
    finally:
        conn.close()


def run_query(query, values=None, fetch=False, many=False):
    """
    Run a query.
    Uses '?' placeholders for SQLite.
    """
    conn = create_connection()
    if not conn:
        return None

    cur = conn.cursor()

    try:
        if many:
            cur.executemany(query, values or [])
        else:
            if isinstance(values, tuple) or isinstance(values, list):
                cur.execute(query, values)
            elif values is not None:
                cur.execute(query, (values,))
            else:
                cur.execute(query)

        if fetch:
            return cur.fetchall()

        conn.commit()

        if query.strip().upper().startswith("INSERT"):
            return cur.lastrowid

        return None
    except Error as e:
        conn.rollback()
        print(f"Query error (Query: {query[:50]}...):", e)
        return None
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    create_tables()
