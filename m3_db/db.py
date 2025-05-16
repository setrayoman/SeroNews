# m3_db/m3_db.py

import sqlite3
from typing import List, Dict

DB_PATH = "data/articles.m3_db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            summary TEXT,
            published TEXT,
            source TEXT,
            parsed INTEGER DEFAULT 0,
            category TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_articles(articles: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for article in articles:
        try:
            c.execute('''
                INSERT OR IGNORE INTO articles 
                (title, link, summary, published, source) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article['link'],
                article['summary'],
                article['published'],
                article['source'],
            ))
        except Exception as e:
            print(f"Failed to insert article: {article['title']}\n{e}")
    conn.commit()
    conn.close()

def fetch_unparsed_articles() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE parsed = 0")
    rows = c.fetchall()
    conn.close()

    keys = ["id", "title", "link", "summary", "published", "source", "parsed", "category"]
    return [dict(zip(keys, row)) for row in rows]
