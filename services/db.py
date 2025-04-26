# services/db.py
import sqlite3
from config import config


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(config.DB_PATH)


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            destination_chat_id INTEGER
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS last_message (
            chat_id INTEGER PRIMARY KEY,
            last_message TEXT
        )
        '''
    )
    conn.commit()
    conn.close()


def add_group(chat_id: int, dest_id: int) -> None:
    conn = get_connection()
    conn.execute(
        'INSERT OR IGNORE INTO groups (chat_id, destination_chat_id) VALUES (?, ?)',
        (chat_id, dest_id)
    )
    conn.commit()
    conn.close()


def list_groups() -> list[tuple[int, int]]:
    conn = get_connection()
    rows = conn.execute(
        'SELECT chat_id, destination_chat_id FROM groups'
    ).fetchall()
    conn.close()
    return rows


def get_last_message(chat_id: int) -> str | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT last_message FROM last_message WHERE chat_id = ?',
        (chat_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def update_last_message(chat_id: int, message: str) -> None:
    conn = get_connection()
    conn.execute(
        'INSERT OR REPLACE INTO last_message (chat_id, last_message) VALUES (?, ?)',
        (chat_id, message)
    )
    conn.commit()
    conn.close()