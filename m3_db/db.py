# m3_db/m3_db.py

import sqlite3
from typing import List, Dict
import json

DB_PATH = "data/articles.db"

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
            category TEXT DEFAULT NULL,
            image_url TEXT
        )
    ''')
    # Table for parsed articles
    c.execute('''
        CREATE TABLE IF NOT EXISTS parsed_articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            source TEXT,
            author TEXT,
            published_at TEXT,
            fetched_at TEXT,
            content TEXT,
            summary TEXT,
            language TEXT,
            image_url TEXT,
            tags TEXT,
            related_stocks TEXT,
            metadata TEXT
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
                (title, link, summary, published, source, image_url) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article['link'],
                article['summary'],
                article['published'],
                article['source'],
                article["image_url"],
            ))
        except Exception as e:
            print(f"Failed to insert article: {article['title']}\n{e}")
            print(f"image_url: {article['image_url']}")
    conn.commit()
    conn.close()

def fetch_unparsed_articles() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE parsed = 0")
    rows = c.fetchall()
    conn.close()

    keys = ["id", "title", "link", "summary", "published", "source", "parsed", "category", "image_url"]
    return [dict(zip(keys, row)) for row in rows]

def save_parsed_articles(parsed_articles: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for article in parsed_articles:
        try:
            c.execute('''
                INSERT OR REPLACE INTO parsed_articles (
                    id, title, url, source, author, published_at, fetched_at,
                    content, summary, language, image_url, tags, related_stocks, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article["id"],
                article["title"],
                article["url"],
                article["source"],
                article["author"],
                article["published_at"],
                article["fetched_at"],
                article["content"],
                article["summary"],
                article["language"],
                article["image_url"],
                json.dumps(article["tags"]),
                json.dumps(article["related_stocks"]),
                json.dumps(article["metadata"])
            ))
        except Exception as e:
            print(f"Failed to insert parsed article: {article['title']}\n{e}")
    conn.commit()
    conn.close()

def mark_as_parsed(article_ids: List[int]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for article_id in article_ids:
        c.execute('UPDATE articles SET parsed = 1 WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
