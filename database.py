import os
import sqlite3

DB_PATH = os.path.expanduser("~/crypto_alerts.db")

def init_db():
    """Initializes the tracking matrix schemas within local state storage."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL UNIQUE,
                target_price REAL NOT NULL,
                direction TEXT NOT NULL CHECK(direction IN ('above', 'below'))
            )
        """)
        conn.commit()

def set_alert(ticker: str, target_price: float, direction: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (ticker, target_price, direction)
            VALUES (?, ?, ?)
            ON CONFLICT(ticker) DO UPDATE SET
                target_price = excluded.target_price,
                direction = excluded.direction
        """, (ticker.lower(), target_price, direction))
        conn.commit()

def get_all_alerts():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ticker, target_price, direction FROM alerts")
        return cursor.fetchall()
