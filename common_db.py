import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cases.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(cases)")
    columns = [c[1] for c in cur.fetchall()]

    if "source" not in columns:
        cur.execute("ALTER TABLE cases ADD COLUMN source TEXT")

    conn.commit()
    conn.close()


ensure_schema()


def url_exists(url: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM cases WHERE url = ? LIMIT 1", (url,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def title_exists(title: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM cases WHERE title = ? LIMIT 1", (title,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def save_article(article: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO cases (
            title,
            lead,
            url,
            published_at,
            collected_at,
            source
        )
        VALUES (
            :title,
            :lead,
            :url,
            :published_at,
            CURRENT_TIMESTAMP,
            :source
        )
        """,
        {
            "title": article.get("title"),
            "lead": article.get("lead"),
            "url": article.get("url"),
            "published_at": article.get("published_at"),
            "source": article.get("source"),
        }
    )

    conn.commit()
    conn.close()
# -------------------------
# Favorites 操作用関数
# -------------------------

def add_favorite(url: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO favorites (url, saved_at) VALUES (?, CURRENT_TIMESTAMP)",
        (url,)
    )
    conn.commit()
    conn.close()


def remove_favorite(url: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM favorites WHERE url = ?", (url,))
    conn.commit()
    conn.close()


def load_favorite_urls() -> list[str]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT url FROM favorites ORDER BY saved_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [row["url"] for row in rows]